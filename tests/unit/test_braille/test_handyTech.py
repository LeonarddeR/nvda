# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Unit tests for the Handy Tech braille display driver."""

import unittest
from brailleDisplayDrivers import handyTech


class Test_parseAtcInfo(unittest.TestCase):
	"""Tests for handyTech._parseAtcInfo."""

	def test_emptyPayload(self):
		"""Empty payload returns empty dict."""
		self.assertEqual(handyTech._parseAtcInfo(b"", 40), {})

	def test_noTouchPayload(self):
		"""Payload with byte0 == 0 (no touch) returns empty dict."""
		self.assertEqual(handyTech._parseAtcInfo(b"\x00\x50", 40), {})

	def test_singleCellHighNibble(self):
		"""Start index 1, data byte 0x50: high nibble 5, low nibble 0 -> {0: 5}."""
		# byte0 = 0x01 means 1-based start index 1, so 0-based index 0.
		# data byte 0x50: high nibble = 5 (pressure for cell 0), low nibble = 0 (no pressure for cell 1).
		result = handyTech._parseAtcInfo(b"\x01\x50", 40)
		self.assertEqual(result, {0: 5})

	def test_multiCellMap(self):
		"""Multiple cells with various pressures; verify exact dict and highest-pressure cell."""
		# byte0 = 0x01 -> 0-based start index 0
		# data byte 0xAB: high nibble = 0xA = 10 (cell 0), low nibble = 0xB = 11 (cell 1)
		# data byte 0x03: high nibble = 0x0 = 0 (cell 2, no touch), low nibble = 0x3 = 3 (cell 3)
		# data byte 0x70: high nibble = 0x7 = 7 (cell 4), low nibble = 0x0 = 0 (cell 5, no touch)
		result = handyTech._parseAtcInfo(b"\x01\xab\x03\x70", 40)
		self.assertEqual(result, {0: 10, 1: 11, 3: 3, 4: 7})
		# Cell 1 has the highest pressure (11)
		focalCell = max(result, key=result.get)
		self.assertEqual(focalCell, 1)

	def test_outOfRangeCellsExcluded(self):
		"""Cells at or beyond cellCount are excluded from the result."""
		# byte0 = 0x01 -> 0-based start index 0; cellCount = 2
		# data byte 0xAB: high nibble = 0xA = 10 (cell 0), low nibble = 0xB = 11 (cell 1)
		# data byte 0xCD: high nibble = 0xC = 12 (cell 2, out of range), low nibble = 0xD = 13 (cell 3)
		result = handyTech._parseAtcInfo(b"\x01\xab\xcd", 2)
		# Only cells 0 and 1 are within range (cellCount=2 means indices 0 and 1 are valid)
		self.assertEqual(result, {0: 10, 1: 11})
		self.assertNotIn(2, result)
		self.assertNotIn(3, result)

	def test_startOffsetNotAtZero(self):
		"""Start index > 1 places pressures at the correct 0-based offset."""
		# byte0 = 0x05 -> 0-based start index 4
		# data byte 0x37: high nibble = 3 (cell 4), low nibble = 7 (cell 5)
		result = handyTech._parseAtcInfo(b"\x05\x37", 40)
		self.assertEqual(result, {4: 3, 5: 7})

	def test_allZeroPressures(self):
		"""Payload with all-zero pressure nibbles returns empty dict."""
		# byte0 = 0x01 -> 0-based start index 0; data byte 0x00 has both nibbles = 0
		result = handyTech._parseAtcInfo(b"\x01\x00\x00", 40)
		self.assertEqual(result, {})
