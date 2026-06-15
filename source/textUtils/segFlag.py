# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from enum import IntFlag

# shared bit masks (explicit powers of two)
_AUTO: int = 1 << 0
_UNISCRIBE: int = 1 << 1
_CHINESE: int = 1 << 2
_ICU: int = 1 << 3


class CharSegFlag(IntFlag):
	"""Character-level segmentation flags."""

	NONE = 0
	AUTO = _AUTO
	UNISCRIBE = _UNISCRIBE
	ICU = _ICU


class WordSegFlag(IntFlag):
	"""Word-level segmentation flags."""

	NONE = 0
	AUTO = _AUTO
	UNISCRIBE = _UNISCRIBE
	CHINESE = _CHINESE
	ICU = _ICU


def resolveCharSegFlag(charSegFlag: CharSegFlag) -> CharSegFlag:
	"""Resolve L{CharSegFlag.AUTO} to a concrete backend.

	AUTO prefers ICU when the Windows ICU library is available, falling back to Uniscribe.
	Any non-AUTO flag is returned unchanged.
	"""
	if charSegFlag == CharSegFlag.AUTO:
		from winBindings.icu import ICU_AVAILABLE

		return CharSegFlag.ICU if ICU_AVAILABLE else CharSegFlag.UNISCRIBE
	return charSegFlag
