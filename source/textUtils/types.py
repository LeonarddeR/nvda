# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter

from enum import Enum


class TextBoundaryBackend(Enum):
	"""Backend used by L{textInfos.offsets.OffsetsTextInfo} to calculate character and word boundaries.

	Set L{textInfos.offsets.OffsetsTextInfo.textBoundaryBackend} on a subclass to choose the backend.
	The default is L{UNISCRIBE}. Set to L{ICU} to opt in to Unicode Standard Annex #29
	compliant segmentation with locale-aware dictionary breaking.
	"""

	UNISCRIBE = "uniscribe"
	"""Use the Windows Uniscribe library via NVDAHelper (usp10 / ScriptBreak). Default backend."""

	ICU = "icu"
	"""Use the Windows ICU library (icu.dll / icuuc.dll).
	Provides Unicode Standard Annex #29 compliant segmentation with locale-aware
	dictionary breaking for Thai, Lao, Khmer, and CJK scripts.
	Available from Windows 10 version 1703. Falls back to UNISCRIBE automatically when unavailable.
	"""

	NATIVE = "native"
	"""Pure-Python fallback using simple alphanumeric boundary detection.
	Does not handle complex scripts or grapheme clusters.
	"""
