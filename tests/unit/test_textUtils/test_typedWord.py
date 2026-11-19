# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the typed word utilities in the textUtils module."""

import unittest

from textUtils import getWordBeforeSeparator, isForcedWordSeparator


class TestTypedWord(unittest.TestCase):
	def test_isForcedWordSeparator(self):
		for ch in ".,:/ ":
			self.assertTrue(isForcedWordSeparator(ch), f"{ch!r} should force a boundary")
		for ch in "aZ9'’":
			self.assertFalse(isForcedWordSeparator(ch), f"{ch!r} should be word-internal")


class TestGetWordBeforeSeparator(unittest.TestCase):
	def test_space(self):
		self.assertEqual(getWordBeforeSeparator("foo bar ", " "), "bar")

	def test_punctuation(self):
		self.assertEqual(getWordBeforeSeparator("foo.", "."), "foo")
		self.assertEqual(getWordBeforeSeparator("foo,", ","), "foo")

	def test_noBreakSpaceMatchesSpace(self):
		self.assertEqual(getWordBeforeSeparator("foo\xa0", " "), "foo")

	def test_lineBreakIsOneSeparator(self):
		for text in ("foo\r\n", "foo\r", "foo\n"):
			self.assertEqual(getWordBeforeSeparator(text, "\r"), "foo", repr(text))

	def test_missingSeparatorReturnsNone(self):
		self.assertIsNone(getWordBeforeSeparator("foo", " "))
		self.assertIsNone(getWordBeforeSeparator("", " "))

	def test_otherSeparatorReturnsNone(self):
		self.assertIsNone(getWordBeforeSeparator("foo ", "."))
		self.assertIsNone(getWordBeforeSeparator("foo.", " "))

	def test_noWordBeforeSeparator(self):
		self.assertEqual(getWordBeforeSeparator("foo  ", " "), "")
		self.assertEqual(getWordBeforeSeparator("foo. ", " "), "")
		self.assertEqual(getWordBeforeSeparator(" ", " "), "")

	def test_wordWithApostrophe(self):
		self.assertEqual(getWordBeforeSeparator("won't ", " "), "won't")
		self.assertEqual(getWordBeforeSeparator("o'clock ", " "), "o'clock")

	def test_quotedWord(self):
		self.assertEqual(getWordBeforeSeparator("say 'hello' ", " "), "'hello'")

	def test_runWithoutSpaces(self):
		self.assertEqual(getWordBeforeSeparator("สวัสดีครับ ", " "), "สวัสดีครับ")

	def test_wordWithCombiningMark(self):
		self.assertEqual(getWordBeforeSeparator("café ", " "), "café")
