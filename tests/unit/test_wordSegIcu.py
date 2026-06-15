# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025-2026 NV Access Limited, Wang Chong

"""Unit tests for ICU word segmentation strategy."""

import unittest
from unittest.mock import patch

from textUtils._wordSeg import wordSegStrategy


class TestIcuStrategy(unittest.TestCase):
	def test_base_accepts_language(self):
		strat = wordSegStrategy.UniscribeWordSegmentationStrategy("hi", None, language="en")
		self.assertEqual(strat.language, "en")

	def test_icu_strategy_getSegmentForOffset_calls_primitive(self):
		text = "hello world"
		with patch("textUtils.icu.calculateWordOffsets", return_value=(0, 6)) as mockCalc:
			strat = wordSegStrategy.IcuWordSegmentationStrategy(text, None, language="en")
			result = strat.getSegmentForOffset(2)
		mockCalc.assert_called_once_with(text, 2, "en")
		self.assertEqual(result, (0, 6))

	def test_icu_segmentedText_returns_text_unchanged(self):
		strat = wordSegStrategy.IcuWordSegmentationStrategy("hello", None)
		self.assertEqual(strat.segmentedText(), "hello")

	def test_segmenter_forwards_language(self):
		from textUtils._wordSeg.wordSegmenter import WordSegmenter
		from textUtils.segFlag import WordSegFlag

		seg = WordSegmenter("hello", None, WordSegFlag.UNISCRIBE, language="en")
		self.assertEqual(seg.strategy.language, "en")

	def test_explicit_icu_flag_selects_icu_when_available(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with patch.object(wordSegmenter, "_ICU_AVAILABLE", True):
			seg = wordSegmenter.WordSegmenter("hello", None, WordSegFlag.ICU)
		self.assertIsInstance(seg.strategy, wordSegStrategy.IcuWordSegmentationStrategy)

	def test_explicit_icu_flag_falls_back_when_unavailable(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with patch.object(wordSegmenter, "_ICU_AVAILABLE", False):
			seg = wordSegmenter.WordSegmenter("hello", None, WordSegFlag.ICU)
		self.assertIsInstance(seg.strategy, wordSegStrategy.UniscribeWordSegmentationStrategy)

	def test_auto_selects_icu_for_thai(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		thai = "สวัสดีครับ"
		with (
			patch.object(wordSegmenter, "_ICU_AVAILABLE", True),
			patch.object(
				wordSegStrategy.ChineseWordSegmentationStrategy,
				"_lib",
				None,
			),
		):
			seg = wordSegmenter.WordSegmenter(thai, None, WordSegFlag.AUTO)
		self.assertIsInstance(seg.strategy, wordSegStrategy.IcuWordSegmentationStrategy)

	def test_auto_keeps_uniscribe_for_latin(self):
		from textUtils._wordSeg import wordSegmenter
		from textUtils.segFlag import WordSegFlag

		with (
			patch.object(wordSegmenter, "_ICU_AVAILABLE", True),
			patch.object(
				wordSegStrategy.ChineseWordSegmentationStrategy,
				"_lib",
				None,
			),
		):
			seg = wordSegmenter.WordSegmenter("hello world", None, WordSegFlag.AUTO)
		self.assertIsInstance(seg.strategy, wordSegStrategy.UniscribeWordSegmentationStrategy)

	def test_word_navigation_unit_flag_has_icu(self):
		from config.featureFlagEnums import WordNavigationUnitFlag

		self.assertTrue(hasattr(WordNavigationUnitFlag, "ICU"))
		self.assertTrue(WordNavigationUnitFlag.ICU.displayString)
