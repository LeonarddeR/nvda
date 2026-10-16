# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Progress reporting for operations that consist of several steps."""

from collections.abc import Callable, Mapping


class ProgressTracker:
	"""Turns the progress within the steps of an operation into an overall percentage.

	The callback receives the current step and the overall percentage.
	It is only called when one of them changes.
	The percentage never decreases.
	"""

	def __init__(
		self,
		shares: Mapping[int, int],
		callback: Callable[[int, int], None] | None,
	):
		"""
		:param shares: The share of the overall progress for each step, in the order the steps run.
		:param callback: Called with the current step and the overall percentage, or ``None`` to report nothing.
		"""
		total = sum(shares.values())
		self._callback = callback
		self._ranges: dict[int, tuple[float, float]] = {}
		start = 0
		for step, share in shares.items():
			self._ranges[step] = (start * 100 / total, (start + share) * 100 / total)
			start += share
		self._step: int
		self._lastReport: tuple[int | None, int] = (None, 0)

	def startStep(self, step: int) -> None:
		"""Report that the given step has started.

		:param step: One of the steps given to the constructor.
		"""
		self._step = step
		self._report(self._ranges[step][0])

	def stepProgress(self, done: int, total: int) -> None:
		"""Report progress within the current step.

		:param done: The number of units of work done in the current step.
		:param total: The total number of units of work in the current step.
		"""
		start, end = self._ranges[self._step]
		fraction = min(done / total, 1.0) if total > 0 else 1.0
		self._report(start + (end - start) * fraction)

	def _report(self, percentage: float) -> None:
		report = (self._step, max(int(percentage), self._lastReport[1]))
		if report == self._lastReport:
			return
		self._lastReport = report
		if self._callback is not None:
			self._callback(*report)
