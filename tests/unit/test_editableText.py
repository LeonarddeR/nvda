# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Babbage B.V., Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for typed word handling in NVDAObjects.behaviors.EditableTextBase."""

import unittest
from unittest.mock import Mock, patch

import config
import controlTypes
import eventHandler
import speech
import textInfos
from config.configFlags import ReportSpellingErrors, TypingEcho
from config.featureFlag import FeatureFlag
from config.featureFlagEnums import TypingEchoModeFlag
from NVDAObjects.behaviors import EditableTextBase

from .textProvider import BasicTextProvider


class EditableTextProvider(EditableTextBase, BasicTextProvider):
	"""An editable text object backed by a provided string, whose caret movement the test controls."""

	movedCaretOffset: int | None = None
	"""The caret offset after :meth:`_hasCaretMoved` waits, or ``None`` if the caret does not move."""

	hasCaretMovedCalls: int = 0
	"""The number of times :meth:`_hasCaretMoved` was called."""

	def _hasCaretMoved(self, bookmark, retryInterval=0.01, timeout=None, origWord=None):
		self.hasCaretMovedCalls += 1
		if self.movedCaretOffset is None:
			return (False, None)
		self.selectionOffsets = (self.movedCaretOffset, self.movedCaretOffset)
		return (True, self.makeTextInfo(textInfos.POSITION_CARET))


class ConsoleLikeProvider(EditableTextProvider):
	"""An editable text object whose caret movement detection does not use events."""

	caretMovementDetectionUsesEvents: bool = False


class BrokenTextProvider(EditableTextProvider):
	"""An editable text object whose text can't be read."""

	def makeTextInfo(self, position):
		raise RuntimeError("Text can't be read")


class TestGetTypedWord(unittest.TestCase):
	def setUp(self) -> None:
		self._originalTypingEchoMode = config.conf["keyboard"]["typingEchoMode"]
		self._originalSpeakTypedWords = config.conf["keyboard"]["speakTypedWords"]
		self._setTypingEchoMode(TypingEchoModeFlag.REAL_TEXT)
		config.conf["keyboard"]["speakTypedWords"] = TypingEcho.ALWAYS.value

	def tearDown(self) -> None:
		config.conf["keyboard"]["typingEchoMode"] = self._originalTypingEchoMode
		config.conf["keyboard"]["speakTypedWords"] = self._originalSpeakTypedWords

	def _setTypingEchoMode(self, value: TypingEchoModeFlag) -> None:
		config.conf["keyboard"]["typingEchoMode"] = FeatureFlag(
			value,
			behaviorOfDefault=TypingEchoModeFlag.REAL_TEXT,
		)

	def _typed(
		self,
		text: str,
		caret: int | None = None,
		movedTo: int | None = None,
		cls: type[EditableTextProvider] = EditableTextProvider,
	) -> EditableTextProvider:
		"""Creates an object in the state it has when NVDA handles a typed separator.

		:param text: The text of the object.
		:param caret: The caret offset, or ``None`` for the end of ``text``.
		:param movedTo: The caret offset after the caret moves, or ``None`` if it does not move.
		"""
		if caret is None:
			caret = len(text)
		obj = cls(text=text, selection=(caret, caret))
		obj.movedCaretOffset = movedTo
		return obj

	def test_wordSeparatorKeyIsNotIntercepted(self):
		for character in ("!", " ", "."):
			gesture = Mock(normalizedIdentifiers=[], isCharacter=True, character=character)
			self.assertIsNone(EditableTextProvider().getScript(gesture), repr(character))

	def test_predictedTextModeReturnsNone(self):
		self._setTypingEchoMode(TypingEchoModeFlag.PREDICTED_TEXT)
		self.assertIsNone(self._typed("ab ").getTypedWord(" "))

	def test_speakTypedWordsOffReturnsNone(self):
		config.conf["keyboard"]["speakTypedWords"] = TypingEcho.OFF.value
		self.assertIsNone(self._typed("ab ").getTypedWord(" "))

	def test_unreliableCaretEventsReturnsNone(self):
		self.assertIsNone(self._typed("ab ", cls=ConsoleLikeProvider).getTypedWord(" "))

	def test_readOnlyReturnsNone(self):
		obj = self._typed("ab ")
		obj.states = {controlTypes.State.READONLY}
		self.assertIsNone(obj.getTypedWord(" "))

	def test_textErrorReturnsNone(self):
		self.assertIsNone(self._typed("ab ", cls=BrokenTextProvider).getTypedWord(" "))

	def test_pendingTypedCharactersReturnsNone(self):
		with patch.object(eventHandler, "isPendingEvents", return_value=True):
			self.assertIsNone(self._typed("ab ").getTypedWord(" "))

	def test_insertedSeparator(self):
		obj = self._typed("ab ")
		self.assertEqual(obj.getTypedWord(" "), "ab")
		self.assertEqual(obj.hasCaretMovedCalls, 0)

	def test_caretInsideText(self):
		self.assertEqual(self._typed("ab cd", caret=3).getTypedWord(" "), "ab")

	def test_noBreakSpace(self):
		self.assertEqual(self._typed("ab\xa0").getTypedWord(" "), "ab")

	def test_lineBreak(self):
		self.assertEqual(self._typed("ab\r\n").getTypedWord("\r"), "ab")

	def test_lateSeparator(self):
		self.assertEqual(self._typed("ab ", caret=2, movedTo=3).getTypedWord(" "), "ab")

	def test_separatorNeverArrivesReturnsNone(self):
		self.assertIsNone(self._typed("ab").getTypedWord(" "))

	def test_typingAheadReturnsNone(self):
		self.assertIsNone(self._typed("ab c", caret=2, movedTo=4).getTypedWord(" "))

	def test_secondSeparatorReturnsNone(self):
		obj = self._typed("ab  ")
		self.assertIsNone(obj.getTypedWord(" "))
		self.assertEqual(obj.hasCaretMovedCalls, 0)
		self.assertIsNone(self._typed("foo. ").getTypedWord(" "))

	def test_dotEndsWord(self):
		self.assertEqual(self._typed("foo.").getTypedWord("."), "foo")

	def test_wordWithApostrophe(self):
		self.assertEqual(self._typed("won't ").getTypedWord(" "), "won't")

	def test_runWithoutSpaces(self):
		self.assertEqual(self._typed("สวัสดีครับ ").getTypedWord(" "), "สวัสดีครับ")

	def test_longWord(self):
		word = "a" * 100
		self.assertEqual(self._typed(f"{word} ").getTypedWord(" "), word)
		self.assertIsNone(self._typed(f"a{word} ").getTypedWord(" "))
		self.assertIsNone(self._typed(f"{word * 2} ").getTypedWord(" "))


class TestSpellingErrorCheck(unittest.TestCase):
	def setUp(self) -> None:
		self._originalReportSpellingErrors = config.conf["documentFormatting"]["reportSpellingErrors2"]
		self._originalAlert = config.conf["keyboard"]["alertForSpellingErrors"]
		config.conf["documentFormatting"]["reportSpellingErrors2"] = ReportSpellingErrors.SOUND.value
		config.conf["keyboard"]["alertForSpellingErrors"] = True
		patch.object(speech, "speakTypedCharacters").start()
		self.addCleanup(patch.stopall)
		self._obj = EditableTextProvider()
		self._check = patch.object(self._obj, "_reportErrorInPreviousWord").start()

	def tearDown(self) -> None:
		config.conf["documentFormatting"]["reportSpellingErrors2"] = self._originalReportSpellingErrors
		config.conf["keyboard"]["alertForSpellingErrors"] = self._originalAlert

	def test_wordEndsAtNonLetter(self):
		for ch in (" ", ".", "1", "’"):
			self._check.reset_mock()
			self._obj.event_typedCharacter(ch)
			self._check.assert_called_once_with()

	def test_wordContinuesAtLetterOrApostrophe(self):
		for ch in ("a", "'"):
			self._obj.event_typedCharacter(ch)
		self._check.assert_not_called()
