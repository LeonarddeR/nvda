# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the utils._progress module."""

import unittest

from utils._progress import ProgressTracker


class Test_ProgressTracker(unittest.TestCase):
	def _createTracker(self, shares: dict[int, int]) -> tuple[ProgressTracker, list[tuple[int, int]]]:
		reports: list[tuple[int, int]] = []
		tracker = ProgressTracker(shares, lambda step, percentage: reports.append((step, percentage)))
		return tracker, reports

	def test_startStep_reportsStartOfStep(self):
		tracker, reports = self._createTracker({1: 20, 2: 80})
		tracker.startStep(1)
		tracker.startStep(2)
		self.assertEqual(reports, [(1, 0), (2, 20)])

	def test_stepProgress_scalesWithinShareOfStep(self):
		tracker, reports = self._createTracker({1: 20, 2: 80})
		tracker.startStep(2)
		tracker.stepProgress(1, 2)
		tracker.stepProgress(2, 2)
		self.assertEqual(reports, [(2, 20), (2, 60), (2, 100)])

	def test_shares_areScaledToHundred(self):
		tracker, reports = self._createTracker({1: 1, 2: 3})
		tracker.startStep(2)
		tracker.stepProgress(1, 3)
		self.assertEqual(reports, [(2, 25), (2, 50)])

	def test_unchangedReports_areSkipped(self):
		tracker, reports = self._createTracker({1: 100})
		tracker.startStep(1)
		for done in range(1, 6):
			tracker.stepProgress(done, 1000)
		self.assertEqual(reports, [(1, 0)])

	def test_percentage_neverDecreases(self):
		tracker, reports = self._createTracker({1: 50, 2: 50})
		tracker.startStep(2)
		tracker.stepProgress(1, 2)
		tracker.startStep(1)
		self.assertEqual(reports, [(2, 50), (2, 75), (1, 75)])

	def test_stepProgress_withoutTotal_completesStep(self):
		tracker, reports = self._createTracker({1: 50, 2: 50})
		tracker.startStep(1)
		tracker.stepProgress(0, 0)
		self.assertEqual(reports, [(1, 0), (1, 50)])

	def test_stepProgress_beyondTotal_staysWithinStep(self):
		tracker, reports = self._createTracker({1: 50, 2: 50})
		tracker.startStep(1)
		tracker.stepProgress(3, 2)
		self.assertEqual(reports, [(1, 0), (1, 50)])

	def test_stepProgress_withoutStartedStep_raises(self):
		tracker, _reports = self._createTracker({1: 100})
		with self.assertRaises(RuntimeError):
			tracker.stepProgress(1, 2)

	def test_withoutCallback_reportsNothing(self):
		tracker = ProgressTracker({1: 100}, None)
		tracker.startStep(1)
		tracker.stepProgress(1, 1)

	def test_withoutShares_raises(self):
		with self.assertRaises(ValueError):
			ProgressTracker({}, None)
