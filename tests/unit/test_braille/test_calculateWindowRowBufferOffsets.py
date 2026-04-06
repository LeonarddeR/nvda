# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2026 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the _calculateWindowRowBufferOffsets function in the braille module."""

import unittest

import braille
import config
from config.configFlags import BrailleTextWrap


def _getDisplayDimensions(dimensions: braille.DisplayDimensions) -> braille.DisplayDimensions:
	"""Used to build a braille handler with particular dimensions."""
	return braille.DisplayDimensions(
		numRows=2,
		numCols=20,
	)


class TestCalculate(unittest.TestCase):
	def setUp(self):
		braille.filter_displayDimensions.register(_getDisplayDimensions)

	def tearDown(self):
		braille.filter_displayDimensions.unregister(_getDisplayDimensions)
		config.conf["braille"]["textWrap"] = BrailleTextWrap.OFF.value

	def test_noCells(self):
		"""Check that, if list of braille cells is empty, offsets will be (0, 0)."""
		braille.handler.buffer.brailleCells = []
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 0)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_firstPosition(self):
		"""Checks that first offset is equal to start parameter."""
		braille.handler.buffer.brailleCells = [1] * braille.handler.displaySize
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		braille.handler.buffer._calculateWindowRowBufferOffsets(1)
		expectedOffsets = [(1, 21), (21, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_end(self):
		"""Check that last row offset won't be greater than length of list of braille cells."""
		braille.handler.buffer.brailleCells = [1] * (braille.handler.displaySize - 10)
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 30)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		braille.handler.buffer.brailleCells = [1] * braille.handler.displaySize
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_wordWrapFirstRowWithSpace(self):
		"""Check that the first row will be truncated if it contains a space, only if text wrap is set to word boundaries."""
		config.conf["braille"]["textWrap"] = BrailleTextWrap.WORD_BOUNDARIES.value
		cells = [1] * (braille.handler.displayDimensions.numCols - 5)
		cells.append(0)
		cells.extend([1] * (braille.handler.displayDimensions.numCols + 4))
		braille.handler.buffer.brailleCells = cells
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 16), (16, 36)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		config.conf["braille"]["textWrap"] = BrailleTextWrap.OFF.value
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)

	def test_wordWrapSecondRowStartsWithSpace(self):
		"""Check that the first row won't be truncated if the next row starts with a space, even if word wrap is True."""
		config.conf["braille"]["textWrap"] = BrailleTextWrap.WORD_BOUNDARIES.value
		cells = [1] * braille.handler.displayDimensions.numCols
		cells.append(0)
		cells.extend([1] * (braille.handler.displayDimensions.numCols - 1))
		braille.handler.buffer.brailleCells = cells
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		expectedOffsets = [(0, 20), (20, 40)]
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
		config.conf["braille"]["textWrap"] = BrailleTextWrap.OFF.value
		braille.handler.buffer._calculateWindowRowBufferOffsets(0)
		self.assertEqual(braille.handler.buffer._windowRowBufferOffsets, expectedOffsets)
