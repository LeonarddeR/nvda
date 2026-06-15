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

	def test_split_dispatch_native_yields_codepoints(self):
		import textUtils

		out = list(textUtils.splitAtCharacterBoundaries("ab", charSegFlag=CharSegFlag.NONE))
		self.assertEqual(out, ["a", "b"])

	def test_split_dispatch_icu_uses_icu_module(self):
		import textUtils
		from unittest.mock import patch

		with patch("textUtils.icu.splitAtCharacterBoundaries", return_value=iter(["x"])) as m:
			out = list(
				textUtils.splitAtCharacterBoundaries("x", language="en", charSegFlag=CharSegFlag.ICU),
			)
		m.assert_called_once_with("x", "en")
		self.assertEqual(out, ["x"])

	def test_split_dispatch_auto_prefers_icu_when_available(self):
		import textUtils
		from unittest.mock import patch

		with (
			patch("winBindings.icu.ICU_AVAILABLE", True),
			patch("textUtils.icu.splitAtCharacterBoundaries", return_value=iter(["x"])) as m,
		):
			out = list(textUtils.splitAtCharacterBoundaries("x", language="en", charSegFlag=CharSegFlag.AUTO))
		m.assert_called_once_with("x", "en")
		self.assertEqual(out, ["x"])

	def test_split_dispatch_auto_falls_back_to_uniscribe_when_icu_unavailable(self):
		import textUtils
		from unittest.mock import patch

		with (
			patch("winBindings.icu.ICU_AVAILABLE", False),
			patch("textUtils.uniscribe.splitAtCharacterBoundaries", return_value=iter(["x"])) as m,
		):
			out = list(textUtils.splitAtCharacterBoundaries("x", charSegFlag=CharSegFlag.AUTO))
		m.assert_called_once_with("x")
		self.assertEqual(out, ["x"])

	def test_split_dispatch_default_honours_config(self):
		import textUtils
		from unittest.mock import patch

		# With no charSegFlag, the configured character segmentation standard is used.
		with patch("textUtils.getConfiguredCharSegFlag", return_value=CharSegFlag.NONE) as cfg:
			out = list(textUtils.splitAtCharacterBoundaries("ab"))
		cfg.assert_called_once()
		self.assertEqual(out, ["a", "b"])
