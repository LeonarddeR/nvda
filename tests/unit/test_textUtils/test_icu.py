# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter

"""Unit tests for the ICU text boundary utilities in textUtils.icu."""

import unittest

from winBindings.icu import ICU_AVAILABLE
from textUtils.icu import (
	calculateCharacterOffsets,
	calculateWordOffsets,
	splitAtCharacterBoundaries,
)

skipIfNoICU = unittest.skipUnless(ICU_AVAILABLE, "ICU library not available on this system")

FACE_PALM = "\U0001f926"  # 🤦 — non-BMP, two UTF-16 code units


@skipIfNoICU
class TestSplitAtCharacterBoundariesEnglish(unittest.TestCase):
	"""splitAtCharacterBoundaries with English (Latin) text."""

	def test_ascii(self):
		self.assertEqual(list(splitAtCharacterBoundaries("hello")), ["h", "e", "l", "l", "o"])

	def test_empty(self):
		self.assertEqual(list(splitAtCharacterBoundaries("")), [])

	def test_single_char(self):
		self.assertEqual(list(splitAtCharacterBoundaries("a")), ["a"])

	def test_with_space(self):
		self.assertEqual(
			list(splitAtCharacterBoundaries("hi there")),
			["h", "i", " ", "t", "h", "e", "r", "e"],
		)

	def test_combining_acute(self):
		# 'e' + COMBINING ACUTE ACCENT is one grapheme cluster.
		text = "caf\u00e9"  # café — U+00E9 is a precomposed form, one cluster each
		self.assertEqual(list(splitAtCharacterBoundaries(text)), ["c", "a", "f", "\u00e9"])

	def test_combining_decomposed(self):
		# Decomposed: 'e' + U+0301 (combining acute) must be one grapheme cluster.
		text = "cafe\u0301"
		clusters = list(splitAtCharacterBoundaries(text))
		self.assertEqual(clusters, ["c", "a", "f", "e\u0301"])

	def test_surrogate_pair_emoji(self):
		# 🤦 is U+1F926 — two UTF-16 code units (surrogate pair); must be one cluster.
		self.assertEqual(list(splitAtCharacterBoundaries(FACE_PALM)), [FACE_PALM])

	def test_emoji_mixed_with_ascii(self):
		text = "a" + FACE_PALM + "b"
		self.assertEqual(list(splitAtCharacterBoundaries(text)), ["a", FACE_PALM, "b"])

	def test_multiple_emoji(self):
		SMILE = "\U0001f60a"  # 😊
		text = FACE_PALM + SMILE
		self.assertEqual(list(splitAtCharacterBoundaries(text)), [FACE_PALM, SMILE])

	def test_language_parameter_accepted(self):
		# The language parameter must not raise and must produce the same result for ASCII.
		result_none = list(splitAtCharacterBoundaries("hello"))
		result_en = list(splitAtCharacterBoundaries("hello", language="en"))
		self.assertEqual(result_none, result_en)


@skipIfNoICU
class TestSplitAtCharacterBoundariesHebrew(unittest.TestCase):
	"""splitAtCharacterBoundaries with Hebrew text."""

	def test_basic_hebrew(self):
		# "שלום" — four Hebrew letters, each a standalone grapheme cluster.
		text = "\u05e9\u05dc\u05d5\u05dd"  # שלום
		self.assertEqual(
			list(splitAtCharacterBoundaries(text)),
			["\u05e9", "\u05dc", "\u05d5", "\u05dd"],
		)

	def test_hebrew_with_combining_vowel(self):
		# SHIN (U+05E9) + SHIN DOT (U+05C1, Nonspacing_Mark) → one grapheme cluster.
		text = "\u05e9\u05c1"
		clusters = list(splitAtCharacterBoundaries(text))
		self.assertEqual(clusters, ["\u05e9\u05c1"])

	def test_hebrew_word_with_nikud(self):
		# שָׁלוֹם — shin+shin-dot, lamed, vav+holam, final-mem; clusters vary by vowel attachment.
		# SHIN U+05E9, SHIN DOT U+05C1, LAMED U+05DC, VAV U+05D5, HOLAM U+05B9, FINAL MEM U+05DD
		shin_with_dot = "\u05e9\u05c1"
		lamed = "\u05dc"
		vav_with_holam = "\u05d5\u05b9"
		final_mem = "\u05dd"
		text = shin_with_dot + lamed + vav_with_holam + final_mem
		clusters = list(splitAtCharacterBoundaries(text))
		self.assertEqual(clusters, [shin_with_dot, lamed, vav_with_holam, final_mem])

	def test_hebrew_sentence(self):
		# "שלום עולם" — "hello world" in Hebrew, separated by a space.
		shalom = "\u05e9\u05dc\u05d5\u05dd"
		olam = "\u05e2\u05d5\u05dc\u05dd"
		text = shalom + " " + olam
		clusters = list(splitAtCharacterBoundaries(text))
		expected = list(shalom) + [" "] + list(olam)
		self.assertEqual(clusters, expected)

	def test_language_he_accepted(self):
		text = "\u05e9\u05dc\u05d5\u05dd"  # שלום
		result_none = list(splitAtCharacterBoundaries(text))
		result_he = list(splitAtCharacterBoundaries(text, language="he"))
		self.assertEqual(result_none, result_he)


@skipIfNoICU
class TestCalculateCharacterOffsetsEnglish(unittest.TestCase):
	"""calculateCharacterOffsets with English (Latin) text."""

	def test_simple_ascii_each_offset(self):
		text = "abc"
		self.assertEqual(calculateCharacterOffsets(text, 0), (0, 1))
		self.assertEqual(calculateCharacterOffsets(text, 1), (1, 2))
		self.assertEqual(calculateCharacterOffsets(text, 2), (2, 3))

	def test_emoji_first_surrogate(self):
		# 🤦abc: emoji occupies UTF-16 offsets 0–1; 'a' at 2, 'b' at 3, 'c' at 4.
		text = FACE_PALM + "abc"
		self.assertEqual(calculateCharacterOffsets(text, 0), (0, 2))

	def test_emoji_second_surrogate(self):
		# Offset 1 is the low surrogate of the emoji — still part of the same cluster.
		text = FACE_PALM + "abc"
		self.assertEqual(calculateCharacterOffsets(text, 1), (0, 2))

	def test_character_after_emoji(self):
		text = FACE_PALM + "abc"
		self.assertEqual(calculateCharacterOffsets(text, 2), (2, 3))
		self.assertEqual(calculateCharacterOffsets(text, 3), (3, 4))
		self.assertEqual(calculateCharacterOffsets(text, 4), (4, 5))

	def test_combining_decomposed(self):
		# "e\u0301" is two UTF-16 code units but one grapheme cluster → (0, 2).
		text = "e\u0301x"
		self.assertEqual(calculateCharacterOffsets(text, 0), (0, 2))
		self.assertEqual(calculateCharacterOffsets(text, 1), (0, 2))
		self.assertEqual(calculateCharacterOffsets(text, 2), (2, 3))

	def test_beyond_end_returns_clamped(self):
		# offset >= textLength: function returns (offset, offset + 1) directly.
		text = "abc"
		self.assertEqual(calculateCharacterOffsets(text, 3), (3, 4))


@skipIfNoICU
class TestCalculateCharacterOffsetsHebrew(unittest.TestCase):
	"""calculateCharacterOffsets with Hebrew text."""

	def test_basic_hebrew_letters(self):
		# שלום — four BMP Hebrew letters, each one UTF-16 code unit.
		text = "\u05e9\u05dc\u05d5\u05dd"
		self.assertEqual(calculateCharacterOffsets(text, 0), (0, 1))
		self.assertEqual(calculateCharacterOffsets(text, 1), (1, 2))
		self.assertEqual(calculateCharacterOffsets(text, 2), (2, 3))
		self.assertEqual(calculateCharacterOffsets(text, 3), (3, 4))

	def test_hebrew_letter_with_combining_vowel(self):
		# SHIN (0) + SHIN DOT (1) are one grapheme cluster → offsets (0, 2) for both.
		text = "\u05e9\u05c1\u05dc"  # שׁל
		self.assertEqual(calculateCharacterOffsets(text, 0), (0, 2))
		self.assertEqual(calculateCharacterOffsets(text, 1), (0, 2))
		self.assertEqual(calculateCharacterOffsets(text, 2), (2, 3))


@skipIfNoICU
class TestCalculateWordOffsetsEnglish(unittest.TestCase):
	"""calculateWordOffsets with English text."""

	def test_first_word(self):
		# Trailing space is included in the word segment.
		text = "hello world"
		self.assertEqual(calculateWordOffsets(text, 0), (0, 6))

	def test_mid_first_word(self):
		text = "hello world"
		self.assertEqual(calculateWordOffsets(text, 2), (0, 6))

	def test_space_between_words(self):
		# Space is attached to the preceding word, so querying at the space
		# returns the same segment as querying inside "hello".
		text = "hello world"
		self.assertEqual(calculateWordOffsets(text, 5), (0, 6))

	def test_second_word(self):
		# No trailing space after "world" (end of string).
		text = "hello world"
		self.assertEqual(calculateWordOffsets(text, 6), (6, 11))

	def test_mid_second_word(self):
		text = "hello world"
		self.assertEqual(calculateWordOffsets(text, 8), (6, 11))

	def test_single_word(self):
		text = "hello"
		self.assertEqual(calculateWordOffsets(text, 0), (0, 5))
		self.assertEqual(calculateWordOffsets(text, 4), (0, 5))

	def test_language_en_accepted(self):
		text = "hello world"
		result_none = calculateWordOffsets(text, 0)
		result_en = calculateWordOffsets(text, 0, language="en")
		self.assertEqual(result_none, result_en)

	def test_word_with_emoji(self):
		# 🤦abc: 🤦 is a non-word boundary character (emoji, 2 UTF-16 units), "abc" is the word.
		text = FACE_PALM + "abc"
		# "abc" starts at UTF-16 offset 2.
		self.assertEqual(calculateWordOffsets(text, 2), (2, 5))
		self.assertEqual(calculateWordOffsets(text, 4), (2, 5))


@skipIfNoICU
class TestCalculateWordOffsetsHebrew(unittest.TestCase):
	"""calculateWordOffsets with Hebrew text."""

	def test_first_word(self):
		# "שלום עולם" — shalom (0-3), space (4), olam (5-8). Trailing space included.
		text = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"
		self.assertEqual(calculateWordOffsets(text, 0), (0, 5))

	def test_mid_first_word(self):
		text = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"
		self.assertEqual(calculateWordOffsets(text, 2), (0, 5))

	def test_space_between_words(self):
		# Space at offset 4 is attached to the preceding word "שלום".
		text = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"
		self.assertEqual(calculateWordOffsets(text, 4), (0, 5))

	def test_second_word(self):
		text = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"
		self.assertEqual(calculateWordOffsets(text, 5), (5, 9))

	def test_mid_second_word(self):
		text = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"
		self.assertEqual(calculateWordOffsets(text, 7), (5, 9))

	def test_language_he_accepted(self):
		text = "\u05e9\u05dc\u05d5\u05dd \u05e2\u05d5\u05dc\u05dd"
		result_none = calculateWordOffsets(text, 0)
		result_he = calculateWordOffsets(text, 0, language="he")
		self.assertEqual(result_none, result_he)

	def test_single_hebrew_word(self):
		text = "\u05e9\u05dc\u05d5\u05dd"  # שלום
		self.assertEqual(calculateWordOffsets(text, 0), (0, 4))
		self.assertEqual(calculateWordOffsets(text, 3), (0, 4))
