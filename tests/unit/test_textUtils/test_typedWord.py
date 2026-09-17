# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the typed word utilities in the textUtils module."""

import unittest

from textUtils import getLastTypedWord, isForcedWordSeparator


class TestTypedWord(unittest.TestCase):
	def test_isForcedWordSeparator(self):
		for ch in ".,:/ ":
			self.assertTrue(isForcedWordSeparator(ch), f"{ch!r} should force a boundary")
		for ch in "aZ9'’":
			self.assertFalse(isForcedWordSeparator(ch), f"{ch!r} should be word-internal")

	def test_getLastTypedWord(self):
		self.assertEqual(getLastTypedWord("foo."), "foo")
		self.assertEqual(getLastTypedWord("foo.bar"), "bar")
		self.assertEqual(getLastTypedWord("ab "), "ab")
		self.assertEqual(getLastTypedWord("won't"), "won't")
		self.assertEqual(getLastTypedWord("."), "")
		self.assertEqual(getLastTypedWord("  "), "")
