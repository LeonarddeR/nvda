# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Babbage B.V., Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the editableText module, in particular announcing typed words from real text."""

import unittest
from unittest.mock import Mock, patch

import config
from config.configFlags import TypingEcho
from config.featureFlag import FeatureFlag
from config.featureFlagEnums import TypingEchoModeFlag
from NVDAObjects.behaviors import EditableTextBase
import textInfos
from textUtils import (
	clampWordToForcedSeparators,
	isForcedWordSeparator,
)
from textInfos.offsets import Offsets
from textUtils.segFlag import WordSegFlag

from speech import speech as speechModule
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
	consoles where the caret lags. Such objects are excluded from real-text typing echo."""

	caretMovementDetectionUsesEvents: bool = False


class UniscribeEditableTextProvider(EditableTextProvider):
	"""An editable text object whose word segmentation is pinned to uniscribe, so it glues words
	across dots like Notepad does."""

	TextInfo = UniscribeTextInfo


class TestHasUnitBeenTyped(unittest.TestCase):
	def setUp(self) -> None:
		self._originalTypingEchoMode = config.conf["keyboard"]["typingEchoMode"]
		self._setRealText()

	def tearDown(self) -> None:
		config.conf["keyboard"]["typingEchoMode"] = self._originalTypingEchoMode

	def _setTypingEchoMode(self, value: TypingEchoModeFlag) -> None:
		config.conf["keyboard"]["typingEchoMode"] = FeatureFlag(
			value,
			behaviorOfDefault=TypingEchoModeFlag.PREDICTED_TEXT,
		)

	def _setRealText(self) -> None:
		self._setTypingEchoMode(TypingEchoModeFlag.REAL_TEXT)

	def _bookmarkAt(self, obj: EditableTextProvider, offset: int):
		return obj.makeTextInfo(Offsets(offset, offset)).bookmark

	def _infoAt(self, obj: EditableTextProvider, offset: int) -> textInfos.TextInfo:
		return obj.makeTextInfo(Offsets(offset, offset))

	def test_predictedTextModeReturnsNone(self):
		"""When the mode is predicted text, no unit is derived from the document."""
		self._setTypingEchoMode(TypingEchoModeFlag.PREDICTED_TEXT)
		obj = EditableTextProvider(text="ab cd", selection=(3, 3))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 2)
		obj.fakeCaretInfo = self._infoAt(obj, 3)
		self.assertEqual(obj.hasUnitBeenTyped(textInfos.UNIT_WORD, " "), (None, None))

	def test_unreliableCaretEventsReturnsNone(self):
		"""An object with unreliable caret events (e.g. a console) never uses the document text."""
		obj = ConsoleLikeProvider(text="ab cd", selection=(3, 3))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 2)
		obj.fakeCaretInfo = self._infoAt(obj, 3)
		self.assertEqual(obj.hasUnitBeenTyped(textInfos.UNIT_WORD, " "), (None, None))

	def test_noCachedBookmarkReturnsNone(self):
		"""Without a cached caret bookmark, no caret movement can be detected."""
		obj = EditableTextProvider(text="ab cd", selection=(3, 3))
		obj._cachedCaretBookmark = None
		obj.fakeCaretInfo = self._infoAt(obj, 3)
		self.assertEqual(obj.hasUnitBeenTyped(textInfos.UNIT_WORD, " "), (None, None))

	def test_caretDidNotMoveReturnsNone(self):
		"""If the caret did not move, no unit is announced."""
		obj = EditableTextProvider(text="ab cd", selection=(2, 2))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 2)
		obj.fakeCaretInfo = None  # _hasCaretMoved will report no movement.
		self.assertEqual(obj.hasUnitBeenTyped(textInfos.UNIT_WORD, " "), (None, None))

	def test_unsupportedUnitRaises(self):
		"""Only UNIT_WORD is supported; other units raise NotImplementedError."""
		obj = EditableTextProvider(text="ab cd", selection=(3, 3))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 2)
		obj.fakeCaretInfo = self._infoAt(obj, 3)
		with self.assertRaises(NotImplementedError):
			obj.hasUnitBeenTyped(textInfos.UNIT_CHARACTER, " ")

	def test_wordCompletedBySpace(self):
		"""Typing a space after a word yields that word from the document text."""
		# "ab" has just been completed by typing a space; the caret is now after the space.
		obj = EditableTextProvider(text="ab cd", selection=(3, 3))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 2)
		obj.fakeCaretInfo = self._infoAt(obj, 3)
		wordFound, typedWord = obj.hasUnitBeenTyped(textInfos.UNIT_WORD, " ")
		self.assertIs(wordFound, True)
		self.assertEqual(typedWord.strip(), "ab")

	def test_caretStillWithinWord(self):
		"""Typing a word-internal separator (apostrophe) reports no unit boundary."""
		# The caret is within the contraction "won't"; the apostrophe does not complete the word.
		obj = EditableTextProvider(text="wont", selection=(3, 3))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 3)
		obj.fakeCaretInfo = self._infoAt(obj, 3)
		self.assertEqual(obj.hasUnitBeenTyped(textInfos.UNIT_WORD, "'"), (False, None))

	def test_dotForcesBoundaryWhenUniscribeGluesWord(self):
		"""A dot ends the typed word even when the application glues "foo.bar" into one word."""
		# Uniscribe glues "foo.bar"; the caret sits after the just-typed dot (offset 4).
		obj = UniscribeEditableTextProvider(text="foo.bar", selection=(4, 4))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 3)
		obj.fakeCaretInfo = self._infoAt(obj, 4)
		wordFound, typedWord = obj.hasUnitBeenTyped(textInfos.UNIT_WORD, ".")
		self.assertIs(wordFound, True)
		self.assertEqual(typedWord, "foo")

	def test_dotSeparatorClampsGluedSecondWord(self):
		"""When a glued "foo.bar" is completed by a space, only the final run "bar" is announced."""
		obj = UniscribeEditableTextProvider(text="foo.bar ", selection=(8, 8))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 7)
		obj.fakeCaretInfo = self._infoAt(obj, 8)
		wordFound, typedWord = obj.hasUnitBeenTyped(textInfos.UNIT_WORD, " ")
		self.assertIs(wordFound, True)
		self.assertEqual(typedWord, "bar")

	def test_commaForcesBoundary(self):
		"""The forced boundary is category-based, not a hardcoded dot: a comma behaves like a dot."""
		obj = UniscribeEditableTextProvider(text="foo,bar", selection=(4, 4))
		obj._cachedCaretBookmark = self._bookmarkAt(obj, 3)
		obj.fakeCaretInfo = self._infoAt(obj, 4)
		wordFound, typedWord = obj.hasUnitBeenTyped(textInfos.UNIT_WORD, ",")
		self.assertIs(wordFound, True)
		self.assertEqual(typedWord, "foo")


class TestForcedWordSeparatorHelpers(unittest.TestCase):
	"""Tests for the pure helpers that classify forced word separators and clamp a word to them."""

	def test_isForcedWordSeparator(self):
		for ch in ".,:/ ":
			self.assertTrue(isForcedWordSeparator(ch), f"{ch!r} should force a boundary")
		for ch in "aZ9" + "'’":
			self.assertFalse(isForcedWordSeparator(ch), f"{ch!r} should be word-internal")

	def test_clampWordToForcedSeparators(self):
		self.assertEqual(clampWordToForcedSeparators("foo."), (0, 3))
		self.assertEqual(clampWordToForcedSeparators("foo.bar"), (4, 7))
		self.assertEqual(clampWordToForcedSeparators("ab "), (0, 2))
		self.assertEqual(clampWordToForcedSeparators("won't"), (0, 5))
		# Only separators / spaces: start == end signals no real word.
		start, end = clampWordToForcedSeparators(".")
		self.assertEqual(start, end)
		start, end = clampWordToForcedSeparators("  ")
		self.assertEqual(start, end)


class TestSpeakPreviousWord(unittest.TestCase):
	"""Tests for speech.speakPreviousWord, which chooses between the predicted keystroke buffer
	and the real document text when announcing a completed word."""

	def setUp(self) -> None:
		self._originalSpeakTypedWords = config.conf["keyboard"]["speakTypedWords"]
		# Always announce typed words, so the word-echo path is exercised.
		config.conf["keyboard"]["speakTypedWords"] = TypingEcho.ALWAYS.value
		speechModule.clearTypedWordBuffer()
		# Patch the speech and API surface used by speakPreviousWord.
		self._speakText = patch.object(speechModule, "speakText").start()
		self._getCaretObject = patch.object(speechModule.api, "getCaretObject").start()
		self._isTypingProtected = patch.object(
			speechModule.api,
			"isTypingProtected",
			return_value=False,
		).start()
		self.addCleanup(patch.stopall)

	def tearDown(self) -> None:
		speechModule.clearTypedWordBuffer()
		config.conf["keyboard"]["speakTypedWords"] = self._originalSpeakTypedWords

	def _setBuffer(self, text: str) -> None:
		speechModule.clearTypedWordBuffer()
		speechModule._curWordChars.extend(text)

	def _makeCaretObject(self, wordResult) -> EditableTextProvider:
		obj = EditableTextProvider(text="")
		obj.states = set()
		obj.hasUnitBeenTyped = Mock(return_value=wordResult)
		self._getCaretObject.return_value = obj
		return obj

	def test_fallsBackToBufferWhenNoWordFromDocument(self):
		"""When the document yields no word (None), the predicted buffer is spoken."""
		self._setBuffer("hello")
		self._makeCaretObject((None, None))
		speechModule.speakPreviousWord(" ")
		self._speakText.assert_called_once_with("hello")
		self.assertEqual(speechModule._curWordChars, [])

	def test_speaksDocumentWordWhenFound(self):
		"""When the document yields a word (True), that word is spoken instead of the buffer."""
		self._setBuffer("helo")  # Buffer differs from the real word to prove the source.
		self._makeCaretObject((True, "hello"))
		speechModule.speakPreviousWord(" ")
		self._speakText.assert_called_once_with("hello")
		self.assertEqual(speechModule._curWordChars, [])

	def test_stillWithinWordKeepsBuffering(self):
		"""When still within a word (False), the separator is buffered and nothing is spoken."""
		self._setBuffer("won")
		self._makeCaretObject((False, None))
		speechModule.speakPreviousWord("'")
		self._speakText.assert_not_called()
		# The separator is appended so the whole word can be announced once completed.
		self.assertEqual(speechModule._curWordChars, list("won'"))

	def test_protectedTypingSkipsDocumentAndEcho(self):
		"""While typing is protected, the document is never consulted and nothing is spoken."""
		self._isTypingProtected.return_value = True
		self._setBuffer("****")
		obj = self._makeCaretObject((True, "secret"))
		speechModule.speakPreviousWord(" ")
		obj.hasUnitBeenTyped.assert_not_called()
		self._speakText.assert_not_called()
		self.assertEqual(speechModule._curWordChars, [])
