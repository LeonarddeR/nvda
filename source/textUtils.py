#textUtils.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""
Classes and utilities to deal with offsets variable width encodings, particularly utf_16.
"""

import encodings
import sys
import ctypes
from collections.abc import ByteString
from typing import Tuple

HIGH_SURROGATE_FIRST = u"\uD800"
HIGH_SURROGATE_LAST = u"\uDBFF"
LOW_SURROGATE_FIRST = u"\uDC00"
LOW_SURROGATE_LAST = u"\uDFFF"

class WideStringOffsetConverter:
	R"""
	Object that holds a string in both its decoded and its UTF-16 encoded form.
	The object allows for easy conversion between offsets in str type strings,
	and offsets in wide character (UTF-16) strings (that are aware of surrogate characters).
	This representation is used by all wide character strings in Windows (i.e. with characters of type L{ctypes.c_wchar}).

	In Python 3 strings, every offset in a string corresponds with one unicode codepoint.
	In UTF-16 encoded strings, 32-bit unicode characters (such as emoji)
	are encoded as one high surrogate and one low surrogate character.
	Therefore, they take not one, but two offsets in such a string.
	This behavior is equivalent to how Python 2 unicode strings behave,
	which are internally encoded as UTF-16.

	For example: 😂 takes one offset in a Python 3 string.
	However, in a Python 2 string or UTF-16 encoded wide string,
	this character internally consists of two characters: \ud83d and \ude02.
	"""

	_encoding: str = "utf_16_le"
	_bytesPerIndex: int = ctypes.sizeof(ctypes.c_wchar)

	def __init__(self, text: str):
		super().__init__()
		if not isinstance(text, str):
			raise TypeError("Value must be of type str")
		self.decoded: str = text
		self.encoded: bytes = text.encode(self._encoding, errors="surrogatepass")

	def __repr__(self):
		return "{}({})".format(self.__class__.__name__, repr(self.decoded))

	@property
	def wideStringLength(self) -> int:
		"""Returns the length of the string in its wide character (UTF-16) representation."""
		return len(self.encoded) // self._bytesPerIndex

	@property
	def strLength(self) -> int:
		"""Returns the length of the string in its pythonic string representation."""
		return len(self.decoded)

	def strToWideOffsets(
		self,
		strStart: int,
		strEnd: int,
		raiseOnError: bool =False
	) -> Tuple[int, int]:
		"""
		This method takes two offsets from the str representation
		of the string the object is initialized with, and converts them to wide character string offsets.
		@param strStart: The start offset in the str representation of the string.
		@param strEnd: The end offset in the str representation of the string.
			This offset is exclusive.
		@param raiseOnError: Raises an IndexError when one of the given offsets
			exceeds L{strLength} or is lower than zero.
			If C{False}, the out of range offset will be bounded to the range of the string.
		@raise ValueError: if strEnd < strStart
		"""
		# Optimisation, don't do anything special if offsets are collapsed at the start.
		if strStart == 0 and strEnd == 0:
			return (0, 0)
		if strEnd < strStart:
			raise ValueError(
				"strEnd=%d must be greater than or equal to strStart=%d"
				% (strEnd, strStart)
			)
		if strStart < 0 or strStart > self.strLength:
			if raiseOnError:
				raise IndexError("str start index out of range")
			strStart = max(0, min(strStart, self.strLength))
		if strEnd < 0 or strEnd > self.strLength:
			if raiseOnError:
				raise IndexError("str end index out of range")
			strEnd = max(0, min(strEnd, self.strLength))
		# If the original string contains surrogate characters, we want to preserve them
		if strStart == 0:
			wideStringStart: int = 0
		else:
			precedingBytes: bytes = self.decoded[:strStart].encode(self._encoding, errors="surrogatepass")
			wideStringStart= len(precedingBytes) // self._bytesPerIndex
		if strStart == strEnd:
			return (wideStringStart, wideStringStart)
		encodedRange: bytes = self.decoded[strStart:strEnd].encode(self._encoding, errors="surrogatepass")
		wideStringEnd: int = wideStringStart + (len(encodedRange) // self._bytesPerIndex)
		return (wideStringStart, wideStringEnd)

	def wideToStrOffsets(
		self,
		wideStringStart: int,
		wideStringEnd: int,
		raiseOnError: bool = False
	) -> Tuple[int, int]:
		r"""
		This method takes two offsets from the wide character representation
		of the string the object is initialized with, and converts them to str offsets.
		wideStringEnd is considered an exclusive offset.
		If either wideStringStart or wideStringEnd corresponds with an offset
		in the middel of a surrogate pair, it is yet counted as one offset in the string.
		For example, when L{decoded} is "😂", which is one offset in the str representation,
		this method returns (0, 1) in all of the following cases:
			* wideStringStart=0, wideStringEnd=1
			* wideStringStart=0, wideStringEnd=2
			* wideStringStart=1, wideStringEnd=2
		However, wideStringStart=1, wideStringEnd=1 results in (0, 0)
		@param wideStringStart: The start offset in the wide character representation of the string.
		@param wideStringEnd: The end offset in the wide character representation of the string.
			This offset is exclusive.
		@param raiseOnError: Raises an IndexError when one of the given offsets
			exceeds L{wideStringLength} or is lower than zero.
			If C{False}, the out of range offset will be bounded to the range of the string.
		@raise ValueError: if wideStringEnd < wideStringStart
		"""
		# Optimisation, don't do anything special if offsets are collapsed at the start.
		if wideStringStart == 0 and wideStringEnd == 0:
			return (0, 0)
		if wideStringEnd < wideStringStart:
			raise ValueError(
				"wideStringEnd=%d must be greater than or equal to wideStringStart=%d"
				% (wideStringEnd, wideStringStart)
			)
		if wideStringStart < 0 or wideStringStart > self.wideStringLength:
			if raiseOnError:
				raise IndexError("Wide string start index out of range")
			wideStringStart = max(0, min(wideStringStart, self.wideStringLength))
		if wideStringEnd < 0 or wideStringEnd > self.wideStringLength:
			if raiseOnError:
				raise IndexError("Wide string end index out of range")
			wideStringEnd = max(0, min(wideStringEnd, self.wideStringLength))
		bytesStart: int = wideStringStart * self._bytesPerIndex
		bytesEnd: int = wideStringEnd * self._bytesPerIndex
		precedingStr= self.encoded[:bytesStart].decode(self._encoding, errors="surrogatepass")
		strStart= len(precedingStr)
		if bytesStart == bytesEnd and bytesEnd <= (len(self.encoded) - self._bytesPerIndex):
			# Though we are trying to fetch str offsets for a single offset,
			# we need to make sure to avoid off by one errors caused by surrogates
			correctedBytesEnd = bytesEnd + self._bytesPerIndex
		else:
			correctedBytesEnd = bytesEnd
		decodedRange: str = self.encoded[bytesStart:correctedBytesEnd].decode(self._encoding, errors="surrogatepass")
		strEnd: int = strStart + len(decodedRange)
		# In the case where precedingStr ends with a high surrogate,
		# and decodedRange ends with a low surrogate character
		# They take one offset in the resulting string, so our offsets are off by one.
		if (
			precedingStr
			and HIGH_SURROGATE_FIRST <= precedingStr[-1] <= HIGH_SURROGATE_LAST
			and decodedRange
			and LOW_SURROGATE_FIRST <= decodedRange[0] <= LOW_SURROGATE_LAST
		):
			strStart -= 1
			strEnd -= 1
		if correctedBytesEnd > bytesEnd:
			# Compensate for the case where we stretched our offsets earlier
			strEnd -= (correctedBytesEnd - bytesEnd) // self._bytesPerIndex
		return (strStart, strEnd)
