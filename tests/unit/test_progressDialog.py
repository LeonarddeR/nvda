# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for :class:`gui._DeterminateProgressDialog`."""

import threading
import types
import unittest
from typing import Self
from unittest.mock import Mock

import gui
from utils.displayString import DisplayStringIntEnum


class _Steps(DisplayStringIntEnum):
	FIRST = 1

	@property
	def _displayStringLabels(self) -> dict[Self, str]:
		return {_Steps.FIRST: "First step"}


class Test_remoteProgress(unittest.TestCase):
	def tearDown(self) -> None:
		gui._DeterminateProgressDialog._remoteProgressReceiver = None

	def test_receiveRemoteProgress_registersDialogOnlyWhileActive(self):
		dialog = Mock()
		with gui._DeterminateProgressDialog.receiveRemoteProgress(dialog, _Steps):
			self.assertEqual(gui._DeterminateProgressDialog._remoteProgressReceiver, (dialog, _Steps))
		self.assertIsNone(gui._DeterminateProgressDialog._remoteProgressReceiver)

	def test_receiveRemoteProgress_unregistersDialogOnError(self):
		dialog = Mock()
		with (
			self.assertRaises(RuntimeError),
			gui._DeterminateProgressDialog.receiveRemoteProgress(dialog, _Steps),
		):
			raise RuntimeError
		self.assertIsNone(gui._DeterminateProgressDialog._remoteProgressReceiver)

	def test_knownStep_setsProgressWithDisplayString(self):
		dialog = Mock()
		gui._DeterminateProgressDialog._remoteProgressReceiver = (dialog, _Steps)
		gui._DeterminateProgressDialog._handleRemoteProgress(1, 42)
		dialog.setProgress.assert_called_once_with(42, "First step")

	def test_unknownStep_isIgnored(self):
		dialog = Mock()
		gui._DeterminateProgressDialog._remoteProgressReceiver = (dialog, _Steps)
		gui._DeterminateProgressDialog._handleRemoteProgress(2, 42)
		dialog.setProgress.assert_not_called()

	def test_withoutReceiver_isIgnored(self):
		gui._DeterminateProgressDialog._handleRemoteProgress(1, 42)


class Test_setProgress(unittest.TestCase):
	def setUp(self) -> None:
		self._dialog = types.SimpleNamespace(_pendingLock=threading.Lock(), _pending=None)

	def _setProgress(self, percentage: int, message: str | None = None) -> None:
		gui._DeterminateProgressDialog.setProgress(self._dialog, percentage, message)

	def test_percentage_isClampedBelowHundred(self):
		self._setProgress(150)
		self.assertEqual(self._dialog._pending, (99, None))
		self._setProgress(-5)
		self.assertEqual(self._dialog._pending, (0, None))

	def test_pendingMessage_isKeptWhenNoNewMessage(self):
		self._setProgress(10, "Copying")
		self._setProgress(11)
		self.assertEqual(self._dialog._pending, (11, "Copying"))

	def test_newMessage_replacesPendingMessage(self):
		self._setProgress(10, "Copying")
		self._setProgress(11, "Registering")
		self.assertEqual(self._dialog._pending, (11, "Registering"))
