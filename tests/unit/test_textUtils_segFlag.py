# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Unit tests for the textUtils.segFlag module."""

import unittest

from textUtils.segFlag import CharSegFlag, WordSegFlag


class TestSegFlagIcu(unittest.TestCase):
	def test_icu_member_on_both_flags(self):
		self.assertTrue(hasattr(CharSegFlag, "ICU"))
		self.assertTrue(hasattr(WordSegFlag, "ICU"))

	def test_icu_distinct_bit(self):
		for other in (CharSegFlag.AUTO, CharSegFlag.UNISCRIBE):
			self.assertNotEqual(CharSegFlag.ICU & other, CharSegFlag.ICU)
		for other in (WordSegFlag.AUTO, WordSegFlag.UNISCRIBE, WordSegFlag.CHINESE):
			self.assertNotEqual(WordSegFlag.ICU & other, WordSegFlag.ICU)
