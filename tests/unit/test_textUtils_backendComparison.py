# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter

"""Comparison tests between the Uniscribe and ICU word boundary backends.

These tests document where the two backends agree and where they diverge,
using the same inputs on both sides.  Tests that require ICU are skipped
when the ICU library is not present on the system.

Word-offset comparisons are done by constructing a WordSegmenter with the
appropriate WordSegFlag and calling getSegmentForOffset.
"""

import unittest

import textUtils
from winBindings.icu import ICU_AVAILABLE
from textUtils._wordSeg.wordSegmenter import WordSegmenter
from textUtils.segFlag import WordSegFlag


skipIfNoICU = unittest.skipUnless(ICU_AVAILABLE, "ICU library not available on this system")

# Encoding used for all WordSegmenter calls — matches what NVDA uses internally.
_ENCODING = textUtils.WCHAR_ENCODING


def _icuWordOffsets(text: str, offset: int, language: str | None = None) -> tuple[int, int] | None:
	"""Get word offsets via the ICU backend (UTF-16 offsets)."""
	return WordSegmenter(text, _ENCODING, WordSegFlag.ICU, language).getSegmentForOffset(offset)


def _uniscribeWordOffsets(text: str, offset: int) -> tuple[int, int] | None:
	"""Get word offsets via the Uniscribe backend (UTF-16 offsets)."""
	return WordSegmenter(text, _ENCODING, WordSegFlag.UNISCRIBE).getSegmentForOffset(offset)


# ---------------------------------------------------------------------------
# calculateWordOffsets — agreement on plain Latin / Hebrew text
# ---------------------------------------------------------------------------


@skipIfNoICU
class TestWordOffsetsEnglish(unittest.TestCase):
	"""Word offset comparison for English text.

	Both backends include trailing whitespace as part of the preceding word.
	NVDA's Uniscribe implementation (textUtils.cpp) does this natively;
	the ICU implementation mirrors that behaviour explicitly.
	"""

	TEXT = "hello world"

	def _assertSameWordOffsets(self, offset: int) -> tuple[int, int] | None:
		icu_result = _icuWordOffsets(self.TEXT, offset)
		uni_result = _uniscribeWordOffsets(self.TEXT, offset)
		self.assertEqual(
			icu_result,
			uni_result,
			f"Backends disagree on word offsets for {self.TEXT!r} at offset {offset}: "
			f"ICU={icu_result!r} Uniscribe={uni_result!r}",
		)
		return icu_result

	def test_first_word(self):
		# Both backends: "hello " — trailing space included.
		result = self._assertSameWordOffsets(0)
		self.assertEqual(result, (0, 6))

	def test_mid_first_word(self):
		result = self._assertSameWordOffsets(2)
		self.assertEqual(result, (0, 6))

	def test_space(self):
		# Both backends: querying at the space returns the preceding word+space.
		result = self._assertSameWordOffsets(5)
		self.assertEqual(result, (0, 6))

	def test_second_word(self):
		# Both backends: "world" — no trailing space at end of string.
		result = self._assertSameWordOffsets(6)
		self.assertEqual(result, (6, 11))

	def test_mid_second_word(self):
		result = self._assertSameWordOffsets(8)
		self.assertEqual(result, (6, 11))


@skipIfNoICU
class TestWordOffsetsHebrew(unittest.TestCase):
	"""Word offset comparison for Hebrew text — שלום עולם (hello world)."""

	TEXT = "שלום עולם"

	def _assertSameWordOffsets(self, offset: int) -> tuple[int, int] | None:
		icu_result = _icuWordOffsets(self.TEXT, offset)
		uni_result = _uniscribeWordOffsets(self.TEXT, offset)
		self.assertEqual(
			icu_result,
			uni_result,
			f"Backends disagree on word offsets for {self.TEXT!r} at offset {offset}: "
			f"ICU={icu_result!r} Uniscribe={uni_result!r}",
		)
		return icu_result

	def test_first_word(self):
		# Both backends: "שלום " — trailing space included, offsets (0, 5).
		result = self._assertSameWordOffsets(0)
		self.assertEqual(result, (0, 5))

	def test_mid_first_word(self):
		result = self._assertSameWordOffsets(2)
		self.assertEqual(result, (0, 5))

	def test_space(self):
		# Both backends: querying at offset 4 (space) returns the preceding word+space.
		result = self._assertSameWordOffsets(4)
		self.assertEqual(result, (0, 5))

	def test_second_word(self):
		# Both backends: "עולם" — no trailing space.
		result = self._assertSameWordOffsets(5)
		self.assertEqual(result, (5, 9))


# ---------------------------------------------------------------------------
# Complex-script cases — backends legitimately diverge here.
#
# Uniscribe uses Windows Script Processor (ScriptBreak) for word boundaries,
# which does not have built-in support for Thai/Khmer/Lao word segmentation
# and falls back to character-level boundaries.  ICU uses LDML-based rules
# with dictionary segmentation for these scripts, so it returns proper word
# segments that cross multiple code points.
#
# For these scripts we only assert that ICU returns a sensible non-None
# result; we do NOT assert parity with Uniscribe.
# ---------------------------------------------------------------------------


@skipIfNoICU
class TestWordOffsetsComplexScript(unittest.TestCase):
	"""ICU returns sensible word segments for complex scripts where Uniscribe diverges."""

	def _assertIcuReturnsSegment(self, text: str, offset: int) -> None:
		result = _icuWordOffsets(text, offset)
		self.assertIsNotNone(
			result,
			f"ICU returned None for {text!r} at offset {offset}",
		)
		start, end = result
		self.assertLessEqual(start, offset)
		self.assertGreater(end, offset)

	def test_thai_word_at_start(self):
		# "สวัสดี" (sawàtdee, a Thai greeting).
		# ICU should return a segment that starts at 0 and spans at least one syllable.
		text = "สวัสดี"
		self._assertIcuReturnsSegment(text, 0)

	def test_thai_sentence(self):
		# "ฉันชื่อ" — "my name is" — three Thai syllables.
		text = "ฉันชื่อ"
		self._assertIcuReturnsSegment(text, 0)
