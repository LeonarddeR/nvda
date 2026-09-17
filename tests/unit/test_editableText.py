# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Babbage B.V., Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for announcing typed words from real text in NVDAObjects.behaviors.EditableTextBase."""

import unittest
from unittest.mock import Mock

import config
import controlTypes
import textInfos
from config.configFlags import TypingEcho
from config.featureFlag import FeatureFlag
from config.featureFlagEnums import TypingEchoModeFlag
from NVDAObjects.behaviors import EditableTextBase
from textInfos.offsets import Offsets
from textUtils.segFlag import WordSegFlag

from .textProvider import BasicTextInfo, BasicTextProvider


class UniscribeTextInfo(BasicTextInfo):
	"""A TextInfo whose word segmentation is pinned to uniscribe, mirroring Win32 edit controls
	(Notepad) which glue e.g. ``foo.bar`` into a single word unit
	(see :class:`NVDAObjects.window.edit.EditTextInfo`)."""

	wordSegFlag = WordSegFlag.UNISCRIBE


class EditableTextProvider(EditableTextBase, BasicTextProvider):
	"""An editable text object backed by a provided string, whose caret-move detection can be
	controlled by the test via :attr:`fakeCaretInfo`."""

	fakeCaretInfo: textInfos.TextInfo | None = None
	"""If set, :meth:`_hasCaretMoved` pretends the caret moved to this TextInfo.

	If ``None``, it pretends the caret did not move.
	"""

	def _hasCaretMoved(self, bookmark, retryInterval=0.01, timeout=None, origWord=None):
		if self.fakeCaretInfo is None:
			return (False, None)
		return (True, self.fakeCaretInfo)


class ConsoleLikeProvider(EditableTextProvider):
	"""An editable text object whose caret events are unreliable, mirroring controls such as
	consoles where the caret lags."""

	caretMovementDetectionUsesEvents: bool = False


class UniscribeEditableTextProvider(EditableTextProvider):
	"""An editable text object whose word segmentation is pinned to uniscribe, so it glues words
	across dots like Notepad does."""

	TextInfo = UniscribeTextInfo


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
			behaviorOfDefault=TypingEchoModeFlag.PREDICTED_TEXT,
		)

	def _typed(
		self,
		text: str,
		before: int | None,
		after: int | None,
		cls: type[EditableTextProvider] = EditableTextProvider,
	) -> EditableTextProvider:
		"""Creates an object in the state it has just after a character was typed.

		:param text: The text of the object after typing.
		:param before: The caret offset cached before typing, ``None`` for no cached bookmark.
		:param after: The caret offset after typing, ``None`` if the caret did not move.
		"""
		obj = cls(text=text)
		if before is not None:
			obj._cachedCaretBookmark = obj.makeTextInfo(Offsets(before, before)).bookmark
		if after is not None:
			obj.fakeCaretInfo = obj.makeTextInfo(Offsets(after, after))
		return obj

	def _getCharacterScript(self, character: str | None):
		gesture = Mock(normalizedIdentifiers=[], isCharacter=True, character=character)
		return EditableTextProvider().getScript(gesture)

	def test_wordSeparatorKeyIsIntercepted(self):
		for character in (".", " ", "^"):
			self.assertIsNotNone(self._getCharacterScript(character), f"{character!r}")

	def test_wordCharacterKeyIsNotIntercepted(self):
		for character in ("a", "9", "'", None):
			self.assertIsNone(self._getCharacterScript(character), f"{character!r}")

	def test_wordSeparatorKeyIsNotInterceptedInPredictedTextMode(self):
		self._setTypingEchoMode(TypingEchoModeFlag.PREDICTED_TEXT)
		self.assertIsNone(self._getCharacterScript("."))

	def test_predictedTextModeReturnsNone(self):
		self._setTypingEchoMode(TypingEchoModeFlag.PREDICTED_TEXT)
		self.assertIsNone(self._typed("ab cd", 2, 3).getTypedWord())

	def test_speakTypedWordsOffReturnsNone(self):
		config.conf["keyboard"]["speakTypedWords"] = TypingEcho.OFF.value
		self.assertIsNone(self._typed("ab cd", 2, 3).getTypedWord())

	def test_unreliableCaretEventsReturnsNone(self):
		self.assertIsNone(self._typed("ab cd", 2, 3, cls=ConsoleLikeProvider).getTypedWord())

	def test_readOnlyReturnsNone(self):
		obj = self._typed("ab cd", 2, 3)
		obj.states = {controlTypes.State.READONLY}
		self.assertIsNone(obj.getTypedWord())

	def test_noCachedBookmarkReturnsNone(self):
		self.assertIsNone(self._typed("ab cd", None, 3).getTypedWord())

	def test_caretDidNotMoveReturnsNone(self):
		self.assertIsNone(self._typed("ab cd", 2, None).getTypedWord())

	def test_onlySeparatorsReturnsNone(self):
		self.assertIsNone(self._typed("  ", 1, 2).getTypedWord())

	def test_cachedBookmarkIsConsumed(self):
		obj = self._typed("ab cd", 2, 3)
		obj.getTypedWord()
		self.assertIsNone(obj._cachedCaretBookmark)

	def test_wordCompletedBySpace(self):
		self.assertEqual(self._typed("ab cd", 2, 3).getTypedWord(), "ab")

	def test_wordWithApostrophe(self):
		self.assertEqual(self._typed("won't ", 5, 6).getTypedWord(), "won't")

	def test_dotForcesBoundaryWhenUniscribeGluesWord(self):
		obj = self._typed("foo.bar", 3, 4, cls=UniscribeEditableTextProvider)
		self.assertEqual(obj.getTypedWord(), "foo")

	def test_dotSeparatorClampsGluedSecondWord(self):
		obj = self._typed("foo.bar ", 7, 8, cls=UniscribeEditableTextProvider)
		self.assertEqual(obj.getTypedWord(), "bar")

	def test_commaForcesBoundary(self):
		obj = self._typed("foo,bar", 3, 4, cls=UniscribeEditableTextProvider)
		self.assertEqual(obj.getTypedWord(), "foo")
