# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for ICU sentence segmentation.

Covers the low-level ``textUtils.icu.calculateSentenceOffsets`` primitive and the
``OffsetsTextInfo._getSentenceOffsets`` integration, including the iteration/tiling
invariant that ``move``/``expand`` rely on.  Tests that require ICU are skipped when
the ICU library is not present on the system.
"""

import unittest

import textInfos
from textInfos.offsets import Offsets
from textUtils import icu
from winBindings.icu import ICU_AVAILABLE

from ..textProvider import BasicTextInfo, BasicTextProvider


skipIfNoICU = unittest.skipUnless(ICU_AVAILABLE, "ICU library not available on this system")


class _BlockParagraphTextInfo(BasicTextInfo):
	"""A TextInfo whose paragraphs are blocks separated by a blank line ("\\n\\n").

	The base BasicTextInfo splits paragraphs by line (any single newline), which would
	produce an empty paragraph between blocks.  Browse mode's real
	VirtualBufferTextInfo._getParagraphOffsets returns block-level bounds instead.  This
	fixture mimics that so the iteration tests exercise block-paragraph crossing rather
	than line splitting (test text is ASCII, so str offsets == UTF-16 offsets).
	"""

	def _getParagraphOffsets(self, offset):
		text = self._getStoryText()
		start = text.rfind("\n\n", 0, offset)
		start = 0 if start < 0 else start + 2
		end = text.find("\n\n", offset)
		end = len(text) if end < 0 else end + 2
		return (start, end)


class _BlockParagraphProvider(BasicTextProvider):
	TextInfo = _BlockParagraphTextInfo


@skipIfNoICU
class TestCalculateSentenceOffsets(unittest.TestCase):
	"""Low-level UAX#29 sentence boundary tests (UTF-16 code-unit offsets, root locale)."""

	def test_english_two_sentences(self):
		"""Trailing space after the terminator is attached to the preceding sentence (UAX#29)."""
		text = "Hello world. Goodbye now."
		self.assertEqual(icu.calculateSentenceOffsets(text, 0), (0, 13))
		# Mid-sentence offsets resolve to the same sentence.
		self.assertEqual(icu.calculateSentenceOffsets(text, 5), (0, 13))
		self.assertEqual(icu.calculateSentenceOffsets(text, 12), (0, 13))
		self.assertEqual(icu.calculateSentenceOffsets(text, 13), (13, 25))

	def test_japanese_ideographic_full_stop(self):
		"""U+3002 (。) is Sentence_Break=STerm, so Japanese segments without a locale."""
		text = "これは日本語です。次の文です。"
		self.assertEqual(icu.calculateSentenceOffsets(text, 0), (0, 9))
		self.assertEqual(icu.calculateSentenceOffsets(text, 9), (9, 15))

	def test_abbreviation_splits_under_root_locale(self):
		"""Documents the deliberate root-locale tradeoff: no abbreviation tailoring.

		"Dr." ends a sentence under the root locale (a locale-aware follow-up could
		suppress this).  Locking this in guards the documented v1 behaviour.
		"""
		text = "Dr. Smith went home."
		self.assertEqual(icu.calculateSentenceOffsets(text, 0), (0, 4))
		self.assertEqual(icu.calculateSentenceOffsets(text, 4), (4, 20))

	def test_surrogate_pair_offsets(self):
		"""Offsets are UTF-16 code-unit indexed; a surrogate pair counts as two units."""
		# H i sp [🤦 = 2 units] sp t h e r e . sp B y e sp n o w .
		text = "Hi \U0001f926 there. Bye now."
		# First sentence spans the surrogate pair and ends after the space at UTF-16 offset 13.
		self.assertEqual(icu.calculateSentenceOffsets(text, 0), (0, 13))
		# An offset inside the surrogate pair still resolves to the containing sentence.
		self.assertEqual(icu.calculateSentenceOffsets(text, 4), (0, 13))
		self.assertEqual(icu.calculateSentenceOffsets(text, 13), (13, 21))

	def test_offset_past_end_fast_path(self):
		"""An offset at/past the end returns a single-unit span (matches word behaviour)."""
		self.assertEqual(icu.calculateSentenceOffsets("abc", 5), (5, 6))

	def test_offset_containment(self):
		"""For every in-range offset, start <= offset < end (the tiling precondition)."""
		text = "One. Two! Three? Four."
		length = len(text.encode("utf-16-le")) // 2
		for offset in range(length):
			start, end = icu.calculateSentenceOffsets(text, offset)
			self.assertTrue(
				start <= offset < end,
				f"offset {offset} not contained in ({start}, {end}) for {text!r}",
			)


@skipIfNoICU
class TestSentenceIterationTiling(unittest.TestCase):
	"""The iteration invariant: move(UNIT_SENTENCE) walks sentences gap-free without stalling.

	BasicTextInfo has no native paragraph support, so _getParagraphOffsets falls back to
	line offsets (newline splitting); a text with no newline is a single paragraph, and a
	text with a newline exercises the paragraph-boundary crossing.
	"""

	def _collectSentences(self, obj, length: int, direction: int) -> list[tuple[int, int]]:
		"""Enumerate sentence spans by expanding then moving in ``direction`` until the walk stops.

		:param obj: A text provider to navigate.
		:param length: UTF-16 length of the story text (bounds the loop and seeds the reverse walk).
		:param direction: 1 to walk forward from the start, -1 to walk backward from the end.
		:return: Sentence spans in document order (the backward walk is reversed before returning).
		"""
		startPos = 0 if direction > 0 else max(0, length - 1)
		info = obj.makeTextInfo(Offsets(startPos, startPos))
		info.expand(textInfos.UNIT_SENTENCE)
		spans = []
		# Bound the loop defensively so a regression stalls the test rather than hangs it.
		for _ in range(length + 2):
			spans.append((info._startOffset, info._endOffset))
			if info.move(textInfos.UNIT_SENTENCE, direction) == 0:
				break
			info.expand(textInfos.UNIT_SENTENCE)
		if direction < 0:
			spans.reverse()
		return spans

	def _assertTiles(self, spans: list[tuple[int, int]], length: int):
		"""Assert the spans tile [0, length) gap-free, in order, with no overlaps."""
		self.assertEqual(spans[0][0], 0, f"first sentence does not start at 0: {spans}")
		self.assertEqual(spans[-1][1], length, f"last sentence does not reach {length}: {spans}")
		for (_, prevEnd), (nextStart, _) in zip(spans, spans[1:]):
			self.assertEqual(prevEnd, nextStart, f"gap/overlap between sentences: {spans}")

	def test_single_paragraph_tiles_both_directions(self):
		text = "Hello world. Goodbye now. The third one."
		length = len(text)  # all-ASCII, so str length == UTF-16 length
		obj = BasicTextProvider(text=text)
		forward = self._collectSentences(obj, length, 1)
		self._assertTiles(forward, length)
		# Three terminators => three sentences.
		self.assertEqual(len(forward), 3)
		# Backward navigation (alt+upArrow) visits the same sentences in the same order.
		backward = self._collectSentences(obj, length, -1)
		self.assertEqual(backward, forward)

	def test_crosses_block_paragraph_boundary_both_directions(self):
		"""With block-paragraph semantics, the walk must cross the blank-line boundary.

		This mirrors browse mode, whose block-level paragraph offsets differ from the base
		line splitting.  (move(UNIT_PARAGRAPH) already relies on the same boundary re-query
		in browse mode today, so the production VBuf offsets are exercised there; here we
		prove the sentence walk itself crosses correctly for both directions.)
		"""
		text = "One. Two.\n\nThree. Four."
		length = len(text)
		blockStart = text.index("\n\n") + 2  # start of the second block paragraph
		obj = _BlockParagraphProvider(text=text)
		forward = self._collectSentences(obj, length, 1)
		self._assertTiles(forward, length)
		# A sentence boundary lands exactly on the second paragraph's start (the walk crossed).
		self.assertIn(blockStart, [start for start, _ in forward])
		backward = self._collectSentences(obj, length, -1)
		self.assertEqual(backward, forward)
		self.assertIn(blockStart, [start for start, _ in backward])


@skipIfNoICU
class TestSentenceOffsetsWithoutIcu(unittest.TestCase):
	"""When ICU is unavailable, _getSentenceOffsets degrades to NotImplementedError."""

	def test_not_implemented_when_icu_unavailable(self):
		from unittest.mock import patch

		obj = BasicTextProvider(text="Hello world. Goodbye now.")
		info = obj.makeTextInfo(Offsets(0, 0))
		with patch.object(icu, "ICU_AVAILABLE", False):
			with self.assertRaises(NotImplementedError):
				info._getSentenceOffsets(0)
