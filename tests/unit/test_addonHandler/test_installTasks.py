# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Unit tests for add-on installTasks lifecycle hooks (onInstall/onUninstall/onEnable/onDisable)."""

import os
import tempfile
import types
import unittest
from unittest.mock import patch

import addonAPIVersion
import addonHandler
from addonStore.models.status import AddonStateCategory


# A lastTestedNVDAVersion that keeps a test add-on compatible with the running NVDA.
_COMPATIBLE_LAST_TESTED = ".".join(str(part) for part in addonAPIVersion.BACK_COMPAT_TO)
# A minimumNVDAVersion far in the future, making a test add-on incompatible.
_INCOMPATIBLE_MINIMUM = "9999.1.0"

_MANIFEST_TEMPLATE = """name = {name}
summary = "Test add-on {name}"
author = "Test"
version = {version}
minimumNVDAVersion = {minimum}
lastTestedNVDAVersion = {lastTested}
"""


def _writeAddon(
	parentDir: str,
	installTasksSource: str,
	name: str = "testAddon",
	version: str = "1.0",
	minimum: str = "0.0.0",
	lastTested: str = _COMPATIBLE_LAST_TESTED,
) -> str:
	"""Create an add-on directory containing a manifest and an installTasks module.

	:param parentDir: Directory in which to create the add-on directory.
	:param installTasksSource: Python source for the add-on's ``installTasks.py``.
	:param name: The add-on name written to the manifest.
	:param version: The add-on version written to the manifest.
	:param minimum: The minimumNVDAVersion written to the manifest.
	:param lastTested: The lastTestedNVDAVersion written to the manifest.
	:return: The path to the created add-on directory.
	"""
	addonPath = os.path.join(parentDir, name)
	os.makedirs(addonPath)
	with open(os.path.join(addonPath, addonHandler.MANIFEST_FILENAME), "wt", encoding="utf-8") as f:
		f.write(
			_MANIFEST_TEMPLATE.format(
				name=name,
				version=version,
				minimum=minimum,
				lastTested=lastTested,
			),
		)
	with open(os.path.join(addonPath, "installTasks.py"), "wt", encoding="utf-8") as f:
		f.write(installTasksSource)
	return addonPath


# An installTasks module that records every call and the keyword arguments it received,
# while declaring the full new signatures.
_RECORDING_INSTALL_TASKS = """
receivedCalls = []


def onInstall(previousVersion=None):
	receivedCalls.append(("onInstall", {"previousVersion": previousVersion}))


def onUninstall(isUpdating=False):
	receivedCalls.append(("onUninstall", {"isUpdating": isUpdating}))


def onEnable(isInstall=False):
	receivedCalls.append(("onEnable", {"isInstall": isInstall}))


def onDisable(isRemove=False):
	receivedCalls.append(("onDisable", {"isRemove": isRemove}))
"""

# An installTasks module whose onDisable raises, used to verify task independence.
_RAISING_ON_DISABLE_INSTALL_TASKS = """
receivedCalls = []


def onDisable(isRemove=False):
	receivedCalls.append(("onDisable", {"isRemove": isRemove}))
	raise RuntimeError("onDisable failure")


def onUninstall(isUpdating=False):
	receivedCalls.append(("onUninstall", {"isUpdating": isUpdating}))
"""

# A legacy installTasks module whose tasks take no arguments at all.
_LEGACY_INSTALL_TASKS = """
receivedCalls = []


def onInstall():
	receivedCalls.append(("onInstall", {}))


def onUninstall():
	receivedCalls.append(("onUninstall", {}))
"""


class TestRunInstallTaskKwargs(unittest.TestCase):
	"""runInstallTask must pass new keyword arguments only to tasks that declare them."""

	def setUp(self) -> None:
		self.tempDir = tempfile.TemporaryDirectory()
		self.addedAddons: list[addonHandler.Addon] = []

	def tearDown(self) -> None:
		for addon in self.addedAddons:
			addon._cleanupAddonImports()
		self.tempDir.cleanup()

	def _makeAddon(self, source: str, **kwargs) -> addonHandler.Addon:
		addon = addonHandler.Addon(_writeAddon(self.tempDir.name, source, **kwargs))
		self.addedAddons.append(addon)
		return addon

	def test_legacyZeroArgTaskIgnoresNewKwargs(self):
		"""A legacy onInstall()/onUninstall() with no parameters is called without the new kwargs."""
		addon = self._makeAddon(_LEGACY_INSTALL_TASKS, name="legacyAddon")
		addon.runInstallTask("onInstall", previousVersion="0.9")
		addon.runInstallTask("onUninstall", isUpdating=True)
		self.assertEqual(
			addon._installTasksModule.receivedCalls,
			[("onInstall", {}), ("onUninstall", {})],
		)

	def test_declaredKwargsArePassed(self):
		"""Tasks declaring the new parameters receive their values."""
		addon = self._makeAddon(_RECORDING_INSTALL_TASKS, name="recordingAddon")
		addon.runInstallTask("onInstall", previousVersion="0.9")
		addon.runInstallTask("onUninstall", isUpdating=True)
		addon.runInstallTask("onEnable", isInstall=True)
		addon.runInstallTask("onDisable", isRemove=True)
		self.assertEqual(
			addon._installTasksModule.receivedCalls,
			[
				("onInstall", {"previousVersion": "0.9"}),
				("onUninstall", {"isUpdating": True}),
				("onEnable", {"isInstall": True}),
				("onDisable", {"isRemove": True}),
			],
		)


class TestCompleteRemoveHooks(unittest.TestCase):
	"""completeRemove fires onDisable(isRemove=True) before onUninstall(isUpdating=...)."""

	def setUp(self) -> None:
		self.tempDir = tempfile.TemporaryDirectory()
		# Use a fresh, isolated state and prevent disk writes.
		self.statePatcher = patch.object(addonHandler, "state", addonHandler.AddonsState())
		self.statePatcher.start()
		self.savePatcher = patch.object(addonHandler.state, "save")
		self.savePatcher.start()

	def tearDown(self) -> None:
		self.savePatcher.stop()
		self.statePatcher.stop()
		self.tempDir.cleanup()

	def _makeAddon(self, name: str) -> addonHandler.Addon:
		return addonHandler.Addon(_writeAddon(self.tempDir.name, _RECORDING_INSTALL_TASKS, name=name))

	def test_removalFiresDisableThenUninstall(self):
		addon = self._makeAddon("removeMe")
		addon.completeRemove(isUpdating=False)
		self.assertEqual(
			addon._installTasksModule.receivedCalls,
			[("onDisable", {"isRemove": True}), ("onUninstall", {"isUpdating": False})],
		)

	def test_updateRemovalPropagatesIsUpdating(self):
		addon = self._makeAddon("updateMe")
		addon.completeRemove(isUpdating=True)
		self.assertEqual(
			addon._installTasksModule.receivedCalls,
			[("onDisable", {"isRemove": True}), ("onUninstall", {"isUpdating": True})],
		)

	def test_noUninstallTaskSkipsHooks(self):
		"""When runUninstallTask is False (rollback of a failed install), no hooks run."""
		addon = self._makeAddon("rollbackMe")
		addon.completeRemove(runUninstallTask=False)
		self.assertIsNone(getattr(addon, "_installTasksModule", None))

	def test_uninstallRunsEvenIfDisableRaises(self):
		"""A failure in onDisable is logged but does not prevent onUninstall from running."""
		addon = addonHandler.Addon(
			_writeAddon(self.tempDir.name, _RAISING_ON_DISABLE_INSTALL_TASKS, name="raisingDisable"),
		)
		addon.completeRemove(isUpdating=False)
		self.assertEqual(
			addon._installTasksModule.receivedCalls,
			[("onDisable", {"isRemove": True}), ("onUninstall", {"isUpdating": False})],
		)


class TestGetInstalledAddonVersion(unittest.TestCase):
	"""_getInstalledAddonVersion finds the version of an existing same-name add-on."""

	@staticmethod
	def _fakeAddon(name: str, version: str, path: str) -> types.SimpleNamespace:
		return types.SimpleNamespace(name=name, version=version, path=path)

	def test_returnsPreviousVersionExcludingGivenPath(self):
		oldAddon = self._fakeAddon("foo", "1.0", r"C:\addons\foo")
		newAddon = self._fakeAddon("foo", "2.0", r"C:\addons\foo.pendingInstall")
		with patch.object(addonHandler, "getAvailableAddons", return_value=[oldAddon, newAddon]):
			self.assertEqual(
				addonHandler._getInstalledAddonVersion("foo", excludePath=newAddon.path),
				"1.0",
			)

	def test_returnsNoneForFreshInstall(self):
		newAddon = self._fakeAddon("foo", "2.0", r"C:\addons\foo.pendingInstall")
		with patch.object(addonHandler, "getAvailableAddons", return_value=[newAddon]):
			self.assertIsNone(addonHandler._getInstalledAddonVersion("foo", excludePath=newAddon.path))

	def test_returnsNoneWhenNameAbsent(self):
		other = self._fakeAddon("bar", "1.0", r"C:\addons\bar")
		with patch.object(addonHandler, "getAvailableAddons", return_value=[other]):
			self.assertIsNone(addonHandler._getInstalledAddonVersion("foo", excludePath=None))


class TestRunEnableDisableTasks(unittest.TestCase):
	"""_runEnableDisableTasks fires onEnable/onDisable for the right transitions only."""

	def setUp(self) -> None:
		self.tempDir = tempfile.TemporaryDirectory()
		self.addons: list[addonHandler.Addon] = []
		self.statePatcher = patch.object(addonHandler, "state", addonHandler.AddonsState())
		self.statePatcher.start()

	def tearDown(self) -> None:
		for addon in self.addons:
			addon._cleanupAddonImports()
		self.statePatcher.stop()
		self.tempDir.cleanup()

	def _makeAddon(self, name: str, *, compatible: bool = True) -> addonHandler.Addon:
		# An incompatible add-on declares a future minimum (and matching lastTested, so the
		# manifest itself stays valid: minimumNVDAVersion <= lastTestedNVDAVersion).
		minimum = "0.0.0" if compatible else _INCOMPATIBLE_MINIMUM
		lastTested = _COMPATIBLE_LAST_TESTED if compatible else _INCOMPATIBLE_MINIMUM
		addon = addonHandler.Addon(
			_writeAddon(
				self.tempDir.name,
				_RECORDING_INSTALL_TASKS,
				name=name,
				minimum=minimum,
				lastTested=lastTested,
			),
		)
		self.addons.append(addon)
		return addon

	def _run(self, *, pendingInstall=(), pendingEnable=(), pendingDisable=()) -> None:
		with patch.object(addonHandler, "getAvailableAddons", return_value=list(self.addons)):
			addonHandler._runEnableDisableTasks(
				set(pendingInstall),
				set(pendingEnable),
				set(pendingDisable),
			)

	def _calls(self, addon: addonHandler.Addon):
		module = getattr(addon, "_installTasksModule", None)
		return None if module is None else module.receivedCalls

	def test_freshInstallFiresOnEnableIsInstallTrue(self):
		addon = self._makeAddon("freshInstall")
		self._run(pendingInstall=["freshInstall"])
		self.assertEqual(self._calls(addon), [("onEnable", {"isInstall": True})])

	def test_userEnableFiresOnEnableIsInstallFalse(self):
		addon = self._makeAddon("reEnabled")
		self._run(pendingEnable=["reEnabled"])
		self.assertEqual(self._calls(addon), [("onEnable", {"isInstall": False})])

	def test_userDisableFiresOnDisableIsRemoveFalse(self):
		addon = self._makeAddon("disabledByUser")
		addonHandler.state[AddonStateCategory.DISABLED].add("disabledByUser")
		self._run(pendingDisable=["disabledByUser"])
		self.assertEqual(self._calls(addon), [("onDisable", {"isRemove": False})])

	def test_steadyAddonFiresNothing(self):
		"""An enabled add-on not involved in any transition gets no hook (transition-only)."""
		addon = self._makeAddon("steady")
		self._run()
		self.assertIsNone(self._calls(addon))

	def test_incompatibleAutoDisabledAddonFiresNothing(self):
		"""An add-on auto-disabled due to incompatibility is deferred (no onDisable here)."""
		addon = self._makeAddon("incompatDisabled", compatible=False)
		addonHandler.state[AddonStateCategory.DISABLED].add("incompatDisabled")
		self._run(pendingDisable=["incompatDisabled"])
		self.assertIsNone(self._calls(addon))

	def test_blockedAddonFiresNothing(self):
		addon = self._makeAddon("blockedAddon")
		addonHandler.state[AddonStateCategory.BLOCKED].add("blockedAddon")
		self._run(pendingEnable=["blockedAddon"])
		self.assertIsNone(self._calls(addon))
