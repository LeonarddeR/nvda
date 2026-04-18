# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ICU-based text boundary utilities using the Windows built-in ICU library.

Requires Windows 10 version 1703 (Creators Update) or later.
BreakIterator instances are cached per thread per locale to avoid repeated allocation cost.
ICU holds a reference to the text buffer; each cache entry therefore stores both the
iterator handle and the buffer so neither is freed prematurely.
"""

import ctypes
import functools
import threading
from typing import Generator

import winBindings.icu as _icu
from logHandler import log


@functools.lru_cache(maxsize=32)
def _resolveLocale(language: str | None) -> bytes:
	"""Convert an optional NVDA language code to a null-terminated ICU locale byte string.

	When no language is provided, ICU's root locale (empty string) is used.
	NVDA locale codes such as "ru_RU" are compatible with ICU locale IDs.
	"""
	return (language or "").encode("ascii", errors="ignore")


class _IteratorCache(threading.local):
	"""Per-thread cache for ICU BreakIterator handles.

	Each thread gets its own iterator instances because ubrk_* functions
	are not thread-safe.  Buffers are kept alive per (kind, locale) key
	because ICU holds a pointer to the text rather than copying it.
	"""

	def __init__(self):
		self._handles: dict[tuple[int, bytes], int] = {}
		self._buffers: dict[tuple[int, bytes], ctypes.Array] = {}

	def get(self, kind: int, locale: bytes, text: str) -> int:
		"""Return a BreakIterator bound to *text*, opening one if necessary.

		@param kind: One of the UBRK_* constants from winBindings.icu.
		@param locale: ICU locale byte string (from _resolveLocale).
		@param text: Python str to analyze.
		@return: Opaque iterator handle (int) suitable for passing to ubrk_* functions.
		@raise RuntimeError: If ICU reports an error opening or rebinding the iterator.
		"""
		key = (kind, locale)
		buf = ctypes.create_unicode_buffer(text)
		textLength = len(buf) - 1
		status = _icu.UErrorCode(0)

		bi = self._handles.get(key)
		if bi is None:
			bi = _icu.ubrk_open(kind, locale, buf, textLength, ctypes.byref(status))
			if _icu.U_FAILURE(status.value) or not bi:
				raise RuntimeError(f"ubrk_open failed with status {status.value}")
			self._handles[key] = bi
		else:
			_icu.ubrk_setText(bi, buf, textLength, ctypes.byref(status))
			if _icu.U_FAILURE(status.value):
				raise RuntimeError(f"ubrk_setText failed with status {status.value}")

		self._buffers[key] = buf  # keep buf alive while ICU references it
		return bi


_iteratorCache = _IteratorCache()


def splitAtCharacterBoundaries(
	text: str,
	language: str | None = None,
) -> Generator[str, None, None]:
	"""Split text into user-perceived characters (grapheme clusters) using ICU.

	Correctly handles surrogate pairs, combining character sequences, and other
	multi-codepoint grapheme clusters, with locale-aware behaviour where relevant.

	@param text: The text to split.
	@param language: Optional NVDA language code (e.g. "en", "ru_RU"). When None,
	    ICU's root locale is used.
	"""
	if not text:
		return
	locale = _resolveLocale(language)
	try:
		bi = _iteratorCache.get(_icu.UBRK_CHARACTER, locale, text)
	except RuntimeError:
		log.debugWarning("ICU character break iterator failed", exc_info=True)
		return

	# ICU positions are UTF-16 code unit indices.  Encode the original text to
	# UTF-16-LE for slicing so we avoid accessing ctypes buffer internals.
	utf16_bytes = text.encode("utf-16-le", errors="surrogatepass")

	pos = _icu.ubrk_first(bi)
	while True:
		nextPos = _icu.ubrk_next(bi)
		if nextPos == _icu.UBRK_DONE:
			break
		yield utf16_bytes[pos * 2 : nextPos * 2].decode("utf-16-le", errors="surrogatepass")
		pos = nextPos


def calculateCharacterOffsets(
	text: str,
	offset: int,
	language: str | None = None,
) -> tuple[int, int] | None:
	"""Calculate the UTF-16 start and end offsets of the character at the given offset.

	@param text: The line text as a Python str.
	@param offset: UTF-16 code unit offset within text at which to find the boundary.
	@param language: Optional NVDA language code for locale-aware segmentation.
	@return: (startOffset, endOffset) as UTF-16 code unit indices (endOffset exclusive),
	    or None if the ICU call failed.
	"""
	textLength = len(text.encode("utf-16-le", errors="surrogatepass")) // 2
	if offset >= textLength:
		return (offset, offset + 1)
	locale = _resolveLocale(language)
	try:
		bi = _iteratorCache.get(_icu.UBRK_CHARACTER, locale, text)
	except RuntimeError:
		log.debugWarning("ICU character break iterator failed", exc_info=True)
		return None

	# ubrk_preceding(offset + 1) yields the largest boundary <= offset.
	start = _icu.ubrk_preceding(bi, offset + 1)
	if start == _icu.UBRK_DONE:
		start = 0
	end = _icu.ubrk_following(bi, offset)
	if end == _icu.UBRK_DONE:
		end = textLength
	return (start, end)


def calculateWordOffsets(
	text: str,
	offset: int,
	language: str | None = None,
) -> tuple[int, int] | None:
	"""Calculate the UTF-16 start and end offsets of the word at the given offset.

	Word boundaries follow Unicode Standard Annex #29 with locale-aware dictionary
	segmentation for scripts such as Thai, Lao, Khmer, and CJK ideographs, where
	words are not separated by spaces.

	Each whitespace or punctuation run between words is its own segment, unlike the
	Uniscribe implementation which attached trailing whitespace to the preceding word.

	@param text: The line text as a Python str.
	@param offset: UTF-16 code unit offset within text at which to find the boundary.
	@param language: Optional NVDA language code for locale-aware segmentation.
	@return: (startOffset, endOffset) as UTF-16 code unit indices (endOffset exclusive),
	    or None if the ICU call failed.
	"""
	textLength = len(text.encode("utf-16-le", errors="surrogatepass")) // 2
	if offset >= textLength:
		return (offset, offset + 1)
	locale = _resolveLocale(language)
	try:
		bi = _iteratorCache.get(_icu.UBRK_WORD, locale, text)
	except RuntimeError:
		log.debugWarning("ICU word break iterator failed", exc_info=True)
		return None

	# ubrk_preceding(offset + 1) yields the largest boundary <= offset,
	# giving the start of the segment that contains offset.
	start = _icu.ubrk_preceding(bi, offset + 1)
	if start == _icu.UBRK_DONE:
		start = 0
	end = _icu.ubrk_following(bi, offset)
	if end == _icu.UBRK_DONE:
		end = textLength
	return (start, end)
