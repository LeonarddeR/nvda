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
