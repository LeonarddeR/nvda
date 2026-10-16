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
		if total <= 0:
			raise ValueError(f"Shares must add up to more than 0, got {total}")
		self._callback = callback
		self._starts: dict[int, float] = {}
		self._shares: dict[int, float] = {}
		start = 0
		for step, share in shares.items():
			self._starts[step] = start * 100 / total
			self._shares[step] = share * 100 / total
			start += share
		self._step: int | None = None
		self._lastReport: tuple[int, int] | None = None

	def startStep(self, step: int) -> None:
		"""Report that the given step has started.

		:param step: One of the steps given to the constructor.
		"""
		self._step = step
		self._report(self._starts[step])

	def stepProgress(self, done: int, total: int) -> None:
		"""Report progress within the current step.

		:param done: The number of units of work done in the current step.
		:param total: The total number of units of work in the current step.
		"""
		if self._step is None:
			raise RuntimeError("No step has been started")
		fraction = min(done / total, 1.0) if total > 0 else 1.0
		self._report(self._starts[self._step] + self._shares[self._step] * fraction)

	def _report(self, percentage: float) -> None:
		percentage = int(percentage)
		if self._lastReport is not None:
			percentage = max(percentage, self._lastReport[1])
		report = (self._step, percentage)
		if report == self._lastReport:
			return
		self._lastReport = report
		if self._callback is not None:
			self._callback(*report)
