# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Progress reporting for operations that consist of several steps."""

from abc import abstractmethod
from collections.abc import Callable, Mapping
from typing import Self

from utils.displayString import DisplayStringIntEnum


class ProgressStep(DisplayStringIntEnum):
	"""A step of an operation that consists of several steps.

	Subclasses define their members in the order the steps run.
	"""

	@property
	@abstractmethod
	def _startPercentages(self) -> dict[Self, int]:
		"""The overall percentage at which each step starts."""

	@property
	def startPercentage(self) -> int:
		"""The overall percentage at which this step starts.
		The step ends where the next step starts, or at 100 for the last step.
		"""
		return self._startPercentages[self]


class ProgressTracker:
	"""Turns the progress within the steps of an operation into an overall percentage.

	The callback receives the current step and the overall percentage.
	It is only called when one of them changes.
	The percentage never decreases.
	"""

	def __init__(
		self,
		steps: type[ProgressStep],
		callback: Callable[[ProgressStep, int], None] | None,
		sizes: Mapping[ProgressStep, int] | None = None,
	):
		"""
		:param steps: The steps of the operation.
		:param callback: Called with the current step and the overall percentage, or ``None`` to report nothing.
		:param sizes: The amount of work in some steps, or ``None`` to use the start percentages only.
			These steps share the range from the start of the first to the end of the last of them,
			in proportion to their sizes.
			Steps between them keep the width of their range.
			A step of size 0 gets an empty range.
		"""
		self._callback = callback
		members = list(steps)
		self._ranges: dict[ProgressStep, tuple[float, float]] = {
			step: (step.startPercentage, nextStep.startPercentage if nextStep is not None else 100)
			for step, nextStep in zip(members, [*members[1:], None])
		}
		totalSize = sum(sizes.values()) if sizes else 0
		if totalSize > 0:
			sizedSteps = [step for step in members if step in sizes]
			sharedWidth = sum(self._ranges[step][1] - self._ranges[step][0] for step in sizedSteps)
			position = self._ranges[sizedSteps[0]][0]
			for step in members[members.index(sizedSteps[0]) : members.index(sizedSteps[-1]) + 1]:
				start, end = self._ranges[step]
				width = sharedWidth * sizes[step] / totalSize if step in sizes else end - start
				self._ranges[step] = (position, position + width)
				position += width
		self._step: ProgressStep
		self._lastReport: tuple[ProgressStep | None, int] = (None, 0)

	def startStep(self, step: ProgressStep) -> None:
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
