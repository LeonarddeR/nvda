# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ctypes bindings for the Windows built-in ICU library.

ICU has been built into Windows since Windows 10 version 1703 (Creators Update).
The combined icu.dll is available from Windows 10 version 1903 (May 2019 Update).
Only the C APIs are exposed; no C++ APIs are available due to ABI instability.

See: https://learn.microsoft.com/windows/win32/intl/international-components-for-unicode--icu-
"""

import ctypes
from ctypes import c_int32, c_void_p, c_char_p, c_wchar_p, POINTER

# Try the combined icu.dll (Windows 10 1903+) first, then icuuc.dll (Windows 10 1703+).
# ubrk_* functions are part of the "common" library, present in both.
_lib: ctypes.WinDLL | None = None
for _dllName in ("icu.dll", "icuuc.dll"):
	try:
		_lib = ctypes.WinDLL(_dllName)
		break
	except OSError:
		pass

#: True if an ICU library was successfully loaded.
ICU_AVAILABLE: bool = _lib is not None

# UBreakIteratorType constants
UBRK_CHARACTER: int = 0
UBRK_WORD: int = 1
UBRK_LINE: int = 2
UBRK_SENTENCE: int = 3

# ubrk_getRuleStatus return values for UBRK_WORD iterators.
# Values in [UBRK_WORD_NONE, UBRK_WORD_NONE_LIMIT) indicate a non-word boundary
# (whitespace or punctuation between words).
# Values >= UBRK_WORD_LETTER indicate an actual word boundary.
UBRK_WORD_NONE: int = 0
UBRK_WORD_NONE_LIMIT: int = 100
UBRK_WORD_NUMBER: int = 100
UBRK_WORD_NUMBER_LIMIT: int = 200
UBRK_WORD_LETTER: int = 200
UBRK_WORD_LETTER_LIMIT: int = 300
UBRK_WORD_KANA: int = 300
UBRK_WORD_KANA_LIMIT: int = 400
UBRK_WORD_IDEO: int = 400
UBRK_WORD_IDEO_LIMIT: int = 500

#: Returned by iterator functions when there are no more boundaries.
UBRK_DONE: int = -1

# UErrorCode is a signed 32-bit integer. U_ZERO_ERROR = 0; errors are > 0.
UErrorCode = c_int32


def U_FAILURE(code: int) -> bool:
	"""Return True if the given UErrorCode indicates an error."""
	return code > 0


if ICU_AVAILABLE:
	assert _lib is not None

	# ubrk_open: create a new break iterator.
	# type: UBreakIteratorType (int32)
	# locale: null-terminated UTF-8 locale ID, or NULL for default
	# text: UTF-16 text to analyze (c_wchar_p on Windows)
	# textLength: number of UTF-16 code units, or -1 for NUL-terminated
	# status: in/out UErrorCode
	# returns: opaque UBreakIterator* handle
	ubrk_open = _lib.ubrk_open
	ubrk_open.restype = c_void_p
	ubrk_open.argtypes = (c_int32, c_char_p, c_wchar_p, c_int32, POINTER(UErrorCode))

	# ubrk_close: free a break iterator.
	ubrk_close = _lib.ubrk_close
	ubrk_close.restype = None
	ubrk_close.argtypes = (c_void_p,)

	# ubrk_setText: rebind an existing iterator to new text without reallocating.
	# ICU holds a reference to the text buffer; caller must keep it alive.
	ubrk_setText = _lib.ubrk_setText
	ubrk_setText.restype = None
	ubrk_setText.argtypes = (c_void_p, c_wchar_p, c_int32, POINTER(UErrorCode))

	# ubrk_first: move to the first boundary (start of text) and return its position.
	ubrk_first = _lib.ubrk_first
	ubrk_first.restype = c_int32
	ubrk_first.argtypes = (c_void_p,)

	# ubrk_next: advance to the next boundary and return its position.
	# Returns UBRK_DONE when past the end of the text.
	ubrk_next = _lib.ubrk_next
	ubrk_next.restype = c_int32
	ubrk_next.argtypes = (c_void_p,)

	# ubrk_preceding: return the largest boundary position strictly less than offset.
	# Sets the iterator to that position.
	ubrk_preceding = _lib.ubrk_preceding
	ubrk_preceding.restype = c_int32
	ubrk_preceding.argtypes = (c_void_p, c_int32)

	# ubrk_following: return the smallest boundary position strictly greater than offset.
	# Sets the iterator to that position. Returns UBRK_DONE if past the end.
	ubrk_following = _lib.ubrk_following
	ubrk_following.restype = c_int32
	ubrk_following.argtypes = (c_void_p, c_int32)

	# ubrk_getRuleStatus: return the rule status tag for the most recently returned boundary.
	# For UBRK_WORD iterators, values < UBRK_WORD_NONE_LIMIT indicate non-word boundaries.
	ubrk_getRuleStatus = _lib.ubrk_getRuleStatus
	ubrk_getRuleStatus.restype = c_int32
	ubrk_getRuleStatus.argtypes = (c_void_p,)
