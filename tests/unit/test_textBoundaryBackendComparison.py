# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter

"""Comparison tests between the Uniscribe and ICU text boundary backends.

These tests document where the two backends agree and where they diverge,
using the same inputs on both sides.  Tests that require ICU are skipped
when the ICU library is not present on the system.
"""

import unittest

from textInfos.offsets import Offsets, TextBoundaryBackend
from winBindings.icu import ICU_AVAILABLE
from textUtils.icu import splitAtCharacterBoundaries as icu_splitChars
from textUtils.uniscribe import splitAtCharacterBoundaries as uniscribe_splitChars
from .textProvider import BasicTextInfo, BasicTextProvider


skipIfNoICU = unittest.skipUnless(ICU_AVAILABLE, "ICU library not available on this system")

FACE_PALM = "\U0001f926"  # 🤦 — two UTF-16 code units


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _ICUTextInfo(BasicTextInfo):
	textBoundaryBackend = TextBoundaryBackend.ICU


class _UniscribeTextInfo(BasicTextInfo):
	textBoundaryBackend = TextBoundaryBackend.UNISCRIBE


class _ICUTextProvider(BasicTextProvider):
	TextInfo = _ICUTextInfo


class _UniscribeTextProvider(BasicTextProvider):
	TextInfo = _UniscribeTextInfo


def _charOffsets(provider: BasicTextProvider, storyOffset: int):
	ti = provider.makeTextInfo(Offsets(storyOffset, storyOffset))
	return ti._getCharacterOffsets(storyOffset)


def _wordOffsets(provider: BasicTextProvider, storyOffset: int):
	ti = provider.makeTextInfo(Offsets(storyOffset, storyOffset))
	return ti._getWordOffsets(storyOffset)


# ---------------------------------------------------------------------------
# splitAtCharacterBoundaries
# ---------------------------------------------------------------------------


@skipIfNoICU
class TestSplitCharsAgreement(unittest.TestCase):
	"""Cases where ICU and Uniscribe produce identical grapheme cluster splits."""

	def _assertSame(self, text):
		icu = list(icu_splitChars(text))
		uni = list(uniscribe_splitChars(text))
		self.assertEqual(icu, uni, f"Backends disagree on {text!r}: ICU={icu!r} Uniscribe={uni!r}")

	def test_empty(self):
		self._assertSame("")

	def test_ascii(self):
		self._assertSame("hello")

	def test_ascii_with_space(self):
		self._assertSame("hello world")

	def test_hebrew(self):
		self._assertSame("\u05e9\u05dc\u05d5\u05dd")  # שלום

	def test_surrogate_pair_emoji(self):
		# Both backends must treat a surrogate pair as one grapheme cluster.
		self._assertSame(FACE_PALM)

	def test_emoji_mixed_ascii(self):
		self._assertSame("a" + FACE_PALM + "b")

	def test_combining_decomposed_latin(self):
		# e + COMBINING ACUTE ACCENT must be one cluster in both backends.
		self._assertSame("e\u0301")

	def test_hebrew_with_combining_vowel(self):
		# SHIN + SHIN DOT must be one cluster in both backends.
		self._assertSame("\u05e9\u05c1")


# ---------------------------------------------------------------------------
# calculateCharacterOffsets
# ---------------------------------------------------------------------------


@skipIfNoICU
class TestCharacterOffsetsAgreement(unittest.TestCase):
	"""Cases where ICU and Uniscribe return the same character offsets."""

	def _assertSameCharOffsets(self, text, offset):
		icu_obj = _ICUTextProvider(text=text)
		uni_obj = _UniscribeTextProvider(text=text)
		icu_result = _charOffsets(icu_obj, offset)
		uni_result = _charOffsets(uni_obj, offset)
		self.assertEqual(
			icu_result,
			uni_result,
			f"Backends disagree on char offsets for {text!r} at offset {offset}: "
			f"ICU={icu_result!r} Uniscribe={uni_result!r}",
		)

	def test_ascii_each_char(self):
		for i in range(3):
			self._assertSameCharOffsets("abc", i)

	def test_hebrew_each_char(self):
		text = "\u05e9\u05dc\u05d5\u05dd"  # שלום
		for i in range(len(text)):
			self._assertSameCharOffsets(text, i)

	def test_surrogate_pair_first_unit(self):
		# Both backends should treat offset 0 (high surrogate) as part of the emoji cluster.
		self._assertSameCharOffsets(FACE_PALM + "a", 0)

	def test_surrogate_pair_second_unit(self):
		# Both backends should treat offset 1 (low surrogate) as part of the emoji cluster.
		self._assertSameCharOffsets(FACE_PALM + "a", 1)

	def test_char_after_surrogate_pair(self):
		self._assertSameCharOffsets(FACE_PALM + "a", 2)


@skipIfNoICU
class TestCharacterOffsetsDivergence(unittest.TestCase):
	"""Cases where ICU and Uniscribe MAY return different character offsets.

	These tests document the actual behaviour of each backend rather than
	asserting equality, so they serve as a living specification.
	"""

	def test_combining_decomposed_latin_offset0(self):
		# "e\u0301" — e + COMBINING ACUTE ACCENT.
		# ICU: one grapheme cluster → (0, 2).
		# Uniscribe: depends on ScriptBreak locale rules; typically also (0, 2).
		text = "e\u0301x"
		icu_obj = _ICUTextProvider(text=text)
		uni_obj = _UniscribeTextProvider(text=text)
		icu_result = _charOffsets(icu_obj, 0)
		uni_result = _charOffsets(uni_obj, 0)
		# Both should agree that 'e' and its combining mark are one cluster.
		self.assertEqual(icu_result, (0, 2), f"ICU gave unexpected result: {icu_result!r}")
		self.assertEqual(uni_result, (0, 2), f"Uniscribe gave unexpected result: {uni_result!r}")


# ---------------------------------------------------------------------------
# calculateWordOffsets — the main area of divergence
# ---------------------------------------------------------------------------


@skipIfNoICU
class TestWordOffsetsEnglish(unittest.TestCase):
	"""Word offset comparison for English text.

	The key difference: Uniscribe includes trailing whitespace as part of the
	preceding word, while ICU treats each whitespace run as its own segment.
	"""

	TEXT = "hello world"

	def setUp(self):
		self.icu = _ICUTextProvider(text=self.TEXT)
		self.uni = _UniscribeTextProvider(text=self.TEXT)

	def test_first_word_icu(self):
		# ICU: "hello" only, no trailing space.
		self.assertEqual(_wordOffsets(self.icu, 0), (0, 5))

	def test_first_word_uniscribe(self):
		# Uniscribe: "hello " — includes the trailing space.
		self.assertEqual(_wordOffsets(self.uni, 0), (0, 6))

	def test_space_icu(self):
		# ICU: space is its own non-word segment.
		self.assertEqual(_wordOffsets(self.icu, 5), (5, 6))

	def test_space_uniscribe(self):
		# Uniscribe: space is absorbed into the preceding word; asking at the space
		# offset returns the preceding word+space segment "hello ".
		self.assertEqual(_wordOffsets(self.uni, 5), (0, 6))

	def test_second_word_agreement(self):
		# Both agree that offset 6 is inside "world".
		icu_result = _wordOffsets(self.icu, 6)
		uni_result = _wordOffsets(self.uni, 6)
		self.assertEqual(icu_result, (6, 11))
		self.assertEqual(uni_result, (6, 11))

	def test_mid_second_word_agreement(self):
		icu_result = _wordOffsets(self.icu, 8)
		uni_result = _wordOffsets(self.uni, 8)
		self.assertEqual(icu_result, uni_result)
		self.assertEqual(icu_result, (6, 11))


@skipIfNoICU
class TestWordOffsetsHebrew(unittest.TestCase):
	"""Word offset comparison for Hebrew text — שלום עולם (hello world)."""

	TEXT = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"

	def setUp(self):
		self.icu = _ICUTextProvider(text=self.TEXT)
		self.uni = _UniscribeTextProvider(text=self.TEXT)

	def test_first_word_icu(self):
		# ICU: "שלום" only, UTF-16 offsets (0, 4).
		self.assertEqual(_wordOffsets(self.icu, 0), (0, 4))

	def test_first_word_uniscribe(self):
		# Uniscribe: "שלום " — includes trailing space, (0, 5).
		self.assertEqual(_wordOffsets(self.uni, 0), (0, 5))

	def test_space_icu(self):
		self.assertEqual(_wordOffsets(self.icu, 4), (4, 5))

	def test_space_uniscribe(self):
		# Uniscribe: space is absorbed into the preceding word; asking at the space
		# offset returns the preceding word+space segment "שלום ".
		self.assertEqual(_wordOffsets(self.uni, 4), (0, 5))

	def test_second_word_agreement(self):
		icu_result = _wordOffsets(self.icu, 5)
		uni_result = _wordOffsets(self.uni, 5)
		self.assertEqual(icu_result, (5, 9))
		self.assertEqual(uni_result, (5, 9))
