# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024-2026 NV Access Limited, Leonard de Ruijter, Shimmy0530
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the installer module."""

import os
import pathlib
import tempfile
import unittest
from typing import NamedTuple
from unittest.mock import ANY, MagicMock, PropertyMock, call, patch

import installer
import psutil
from gui import installerGui
from gui.message import DisplayableError
from parameterized import parameterized


class Test_tryCopyFile(unittest.TestCase):
	_sourcePath = r"C:\source.txt"
	_destPath = r"C:\destination.txt"
	_qualifiedSourcePath = rf"\\?\{_sourcePath}"
	_qualifiedDestPath = rf"\\?\{_destPath}"

	@patch("installer.time.sleep")
	@patch("installer.winBindings.kernel32.CopyFileEx", return_value=1)
	def test_successDoesNotRetry(self, copyFileMock: MagicMock, sleepMock: MagicMock):
		installer.tryCopyFile(self._sourcePath, self._destPath)

		copyFileMock.assert_called_once_with(
			self._qualifiedSourcePath,
			self._qualifiedDestPath,
			ANY,
			None,
			None,
			0,
		)
		sleepMock.assert_not_called()

	def test_onProgress_reportsBytesCopied(self):
		size = 3 << 20
		tempDir = self.enterContext(tempfile.TemporaryDirectory())
		_createFiles(tempDir, {"source.bin": size})
		reports: list[int] = []
		installer.tryCopyFile(
			os.path.join(tempDir, "source.bin"),
			os.path.join(tempDir, "dest.bin"),
			onProgress=reports.append,
		)
		self.assertEqual(os.path.getsize(os.path.join(tempDir, "dest.bin")), size)
		self.assertEqual(reports, sorted(reports))
		self.assertEqual(reports[-1], size)

	def test_temporaryFailuresAreRetried(self):
		with (
			patch(
				"installer.winBindings.kernel32.CopyFileEx",
				side_effect=(0, 0, 1),
			) as copyFileMock,
			patch("installer.ctypes.GetLastError", return_value=33),
			patch("installer.os.path.exists", return_value=False),
			patch("installer.time.sleep") as sleepMock,
		):
			installer.tryCopyFile(
				self._sourcePath,
				self._destPath,
				numRetries=3,
				retryInterval=0.25,
			)

		self.assertEqual(copyFileMock.call_count, 3)
		self.assertEqual(
			sleepMock.call_args_list,
			[call(0.25), call(0.25)],
		)

	def test_exhaustedRetriesRaiseOriginalError(self):
		with (
			patch(
				"installer.winBindings.kernel32.CopyFileEx",
				return_value=0,
			) as copyFileMock,
			patch("installer.ctypes.GetLastError", return_value=33),
			patch("installer.os.path.exists", return_value=False),
			patch("installer.time.sleep") as sleepMock,
			self.assertRaisesRegex(OSError, r"error 33 copying"),
		):
			installer.tryCopyFile(
				self._sourcePath,
				self._destPath,
				numRetries=3,
				retryInterval=0.25,
			)

		self.assertEqual(copyFileMock.call_count, 3)
		self.assertEqual(
			sleepMock.call_args_list,
			[call(0.25), call(0.25), call(0.25)],
		)

	def test_existingDestinationUsesOverwriteFallbackWithoutRetry(self):
		tempPath = r"C:\temporary.txt"
		with (
			patch(
				"installer.winBindings.kernel32.CopyFileEx",
				side_effect=(0, 1),
			) as copyFileMock,
			patch("installer.ctypes.GetLastError", return_value=5),
			patch("installer.os.path.exists", return_value=True),
			patch(
				"installer._createEmptyTempFileForDeletingFile",
				return_value=tempPath,
			) as createTempFileMock,
			patch("installer.os.replace") as replaceMock,
			patch("installer.winKernel.moveFileEx") as moveFileMock,
			patch("installer.time.sleep") as sleepMock,
		):
			installer.tryCopyFile(self._sourcePath, self._destPath)

		self.assertEqual(
			copyFileMock.call_args_list,
			[
				call(self._qualifiedSourcePath, self._qualifiedDestPath, ANY, None, None, 0),
				call(self._qualifiedSourcePath, self._qualifiedDestPath, ANY, None, None, 0),
			],
		)
		createTempFileMock.assert_called_once()
		replaceMock.assert_called_once_with(self._qualifiedDestPath, tempPath)
		moveFileMock.assert_called_once_with(
			tempPath,
			None,
			installer.winKernel.MOVEFILE_DELAY_UNTIL_REBOOT,
		)
		sleepMock.assert_not_called()


class Test_BatchDeletion(unittest.TestCase):
	"""Tests for deleting previous installation files safely in a batch for the installation process.
	If any file fails to be deleted, the entire operation should be aborted.
	This ensure installations don't end up in a partially uninstalled state.
	"""

	def setUp(self) -> None:
		self._originalTempDir = tempfile.mkdtemp()
		self._sampleFiles = [
			"file1.txt",
			"file2.txt",
			"file3.txt",
		]
		for file in self._sampleFiles:
			pathlib.Path(self._originalTempDir, file).touch(exist_ok=False)

	def tearDown(self) -> None:
		for file in self._sampleFiles:
			f = pathlib.Path(self._originalTempDir, file)
			if f.exists():
				f.unlink()

	def test_deleteFilesSuccess(self):
		installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)
		for file in self._sampleFiles:
			self.assertFalse(pathlib.Path(self._originalTempDir, file).exists())

	def test_deleteFilesFailure(self):
		with self.assertRaises(installer.RetriableFailure):  # noqa: SIM117
			with open(pathlib.Path(self._originalTempDir, self._sampleFiles[1]), "r"):
				installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)

		# Assert files are back where they started
		for file in self._sampleFiles:
			self.assertTrue(pathlib.Path(self._originalTempDir, file).exists())

	def test_deleteNonExistantFilesSuccess(self):
		# Delete all expected files
		for file in self._sampleFiles:
			pathlib.Path(self._originalTempDir, file).unlink()

		installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)
		for file in self._sampleFiles:
			self.assertFalse(pathlib.Path(self._originalTempDir, file).exists())

	def test_deleteNonExistantFileSuccess(self):
		# Delete 1 file
		pathlib.Path(self._originalTempDir, self._sampleFiles[1]).unlink()

		installer._deleteFileGroupOrFail(self._originalTempDir, self._sampleFiles)
		for file in self._sampleFiles:
			self.assertFalse(pathlib.Path(self._originalTempDir, file).exists())


class Test_terminateRunningNVDA(unittest.TestCase):
	"""Tests for finding and ending copies of NVDA which run from the installation folder."""

	_installDir = "C:\\Program Files\\NVDA"
	_installDirX86 = "C:\\Program Files (x86)\\NVDA"

	@staticmethod
	def _fakeProcess(pid: int, exe: str | None) -> MagicMock:
		"""Create a stand-in for a process as returned by :func:`psutil.process_iter` with exe."""
		process = MagicMock(spec=psutil.Process)
		process.pid = pid
		process.info = {"exe": exe}
		return process

	@parameterized.expand(
		(
			("nvda", "C:\\Program Files\\NVDA\\nvda.exe", True),
			("slave", "C:\\Program Files\\NVDA\\nvda_slave.exe", True),
			("differentCase", "c:\\program files\\nvda\\NVDA.EXE", True),
			("x86Dir", "C:\\Program Files (x86)\\NVDA\\nvda.exe", True),
			("otherExe", "C:\\Program Files\\NVDA\\notepad.exe", False),
			("subfolder", "C:\\Program Files\\NVDA\\lib\\nvda.exe", False),
			("otherFolder", "C:\\Temp\\launcher\\nvda.exe", False),
			("unknown", None, False),
		),
	)
	def test_getRunningNVDAProcesses_matchesPath(self, _name: str, imagePath: str | None, expected: bool):
		"""The NVDA executables are found when they run directly from an installation folder.
		Other executables, subfolders and other folders are not found.
		"""
		with patch("installer.psutil.process_iter", return_value=iter([self._fakeProcess(100, imagePath)])):
			found = list(installer._getRunningNVDAProcesses([self._installDir, self._installDirX86]))
		self.assertEqual(bool(found), expected)

	def test_getRunningNVDAProcesses_skipsCurrentProcess(self):
		"""The current process is never found."""
		process = self._fakeProcess(os.getpid(), f"{self._installDir}\\nvda.exe")
		with patch("installer.psutil.process_iter", return_value=iter([process])):
			found = list(installer._getRunningNVDAProcesses([self._installDir]))
		self.assertEqual(found, [])

	def test_waitForRunningNVDAProcesses(self):
		"""A copy that exits during the wait is not returned, a copy that keeps running is."""
		exiting = self._fakeProcess(100, f"{self._installDir}\\nvda.exe")
		exiting.is_running.side_effect = [True, False]
		staying = self._fakeProcess(200, f"{self._installDir}\\nvda.exe")
		staying.is_running.return_value = True
		with (
			patch("installer._getRunningNVDAProcesses", return_value=iter([exiting, staying])),
			patch("installer.time.monotonic", side_effect=[0, 1, 4]),
			patch("installer.time.sleep"),
		):
			remaining = installer._waitForRunningNVDAProcesses([self._installDir], timeout=3)
		self.assertEqual(remaining, [staying])

	def test_waitForRunningNVDAProcesses_noneRunning(self):
		"""Without running copies, nothing is waited for."""
		with (
			patch("installer._getRunningNVDAProcesses", return_value=iter([])),
			patch("installer.time.sleep") as sleepMock,
		):
			self.assertEqual(installer._waitForRunningNVDAProcesses([self._installDir]), [])
		sleepMock.assert_not_called()

	def test_terminateProcesses(self):
		"""Every copy is ended. A copy that can't be ended doesn't stop the others, and isn't waited for."""
		failing = self._fakeProcess(100, f"{self._installDir}\\nvda.exe")
		failing.kill.side_effect = psutil.AccessDenied(100)
		ending = self._fakeProcess(200, f"{self._installDir}\\nvda.exe")
		with patch("installer.psutil.wait_procs", return_value=([ending], [])) as waitProcsMock:
			installer._terminateProcesses([failing, ending])
		ending.kill.assert_called_once_with()
		waitProcsMock.assert_called_once_with([ending], timeout=2)


class Test_doInstallTerminateRunningNVDA(unittest.TestCase):
	"""Tests for asking whether to end running copies of NVDA before installing."""

	def setUp(self):
		self.progressDialogMock = self.enterContext(patch("gui.installerGui._DeterminateProgressDialog"))
		self.errorMock = self.enterContext(patch("gui.installerGui._showInstallationFailedError"))
		self.enterContext(patch("gui.installerGui._isOtherNVDARunning", return_value=True))
		self.isUserAnAdminMock = self.enterContext(
			patch("gui.installerGui.shell32.IsUserAnAdmin", return_value=False),
		)
		self.execElevatedMock = self.enterContext(
			patch("gui.installerGui.systemUtils.execElevated", return_value=1),
		)

	@parameterized.expand(((False, "0"), (True, "1")))
	def test_passesTerminateFlagToSlave(self, isOtherNVDARunning: bool, expected: str):
		"""After the user agrees, the elevated slave is told to end the running copies."""
		with (
			patch("gui.installerGui._isOtherNVDARunning", return_value=isOtherNVDARunning),
			patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=True),
		):
			installerGui.doInstall(isUpdate=True)
		self.execElevatedMock.assert_called_once_with(
			installerGui.config.SLAVE_FILENAME,
			["install", "1", "0", expected, "0"],
			wait=True,
			handleAlreadyElevated=True,
		)

	def test_noFailsInstallation(self):
		"""Answering No closes the progress dialog, shows the installation failed error and doesn't install."""
		with patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=False):
			installerGui.doInstall(isUpdate=True)
		self.progressDialogMock.return_value.done.assert_called_once_with()
		self.errorMock.assert_called_once_with()
		self.execElevatedMock.assert_not_called()

	@parameterized.expand((("freshInstall", False, False), ("silent", True, True)))
	def test_neverAsks(self, _name: str, isUpdate: bool, silent: bool):
		"""Fresh and silent installations never ask and never end running copies."""
		with patch("gui.installerGui._confirmTerminateRunningNVDA") as confirmMock:
			installerGui.doInstall(isUpdate=isUpdate, silent=silent)
		confirmMock.assert_not_called()
		self.progressDialogMock.return_value.setStep.assert_called_once_with(installer._InstallStep.ELEVATE)
		self.assertEqual(self.execElevatedMock.call_args.args[1][3], "0")

	def test_reportsWaitAndElevateSteps(self):
		"""The progress dialog reports the wait step while looking for running copies, then the elevate step."""
		with patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=True):
			installerGui.doInstall(isUpdate=True)
		self.assertEqual(
			self.progressDialogMock.return_value.setStep.call_args_list,
			[call(installer._InstallStep.WAIT_FOR_RUNNING_COPIES), call(installer._InstallStep.ELEVATE)],
		)

	def test_alreadyElevated_skipsElevateStep(self):
		"""When NVDA already runs as administrator, the progress dialog doesn't report the elevate step."""
		self.isUserAnAdminMock.return_value = True
		with patch("gui.installerGui._confirmTerminateRunningNVDA", return_value=True):
			installerGui.doInstall(isUpdate=True)
		self.progressDialogMock.return_value.setStep.assert_called_once_with(
			installer._InstallStep.WAIT_FOR_RUNNING_COPIES,
		)


class _ShouldWarnBeforeUpdateFactors(NamedTuple):
	remoteEnabled: bool
	isConnectedAsFollower: bool
	isUserAnAdmin: bool
	expectedReturn: bool = False


class testFollowerWarning(unittest.TestCase):
	@parameterized.expand(
		(
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=False,
				isUserAnAdmin=False,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=False,
				isUserAnAdmin=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=True,
				isUserAnAdmin=False,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=False,
				isConnectedAsFollower=True,
				isUserAnAdmin=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=False,
				isUserAnAdmin=False,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=False,
				isUserAnAdmin=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=True,
				isUserAnAdmin=False,
				expectedReturn=True,
			),
			_ShouldWarnBeforeUpdateFactors(
				remoteEnabled=True,
				isConnectedAsFollower=True,
				isUserAnAdmin=True,
			),
		),
	)
	def test_shouldWarnBeforeUpdate(
		self,
		remoteEnabled: bool,
		isConnectedAsFollower: bool,
		isUserAnAdmin: bool,
		expectedReturn: bool,
	):
		with (
			patch("winBindings.shell32.IsUserAnAdmin", return_value=isUserAnAdmin),
			patch(
				"_remoteClient.client.RemoteClient",
				isConnectedAsFollower=isConnectedAsFollower,
			) as patchedRemoteClient,
			patch.dict(
				"_remoteClient.__dict__",
				_remoteClient=patchedRemoteClient if remoteEnabled else None,
			),
		):
			self.assertEqual(installerGui._shouldWarnBeforeUpdate(), expectedReturn)


class Test_comparePreviousInstall(unittest.TestCase):
	def test_freshInstall_whenNoInstallDirsExist(self):
		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value="C:\\Program Files\\NVDA",
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value="C:\\Program Files (x86)\\NVDA",
			),
			patch("installer.os.path.isdir", return_value=False),
			patch("installer.fileUtils.getFileVersionInfo") as getVersionMock,
		):
			result = installer._comparePreviousInstall()
			self.assertEqual(result, installer.ComparisonState.FRESH_INSTALL)
			getVersionMock.assert_not_called()

	def test_unknown_whenOldVersionLookupFails_inInstallDir(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				raise OSError("locked")
			self.fail("Current version lookup should not occur when old version lookup fails.")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value="C:\\Program Files (x86)\\NVDA",
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenOldVersionLookupFails_inX86InstallDir(self):
		installDir = "C:\\Program Files\\NVDA"
		installDirX86 = "C:\\Program Files (x86)\\NVDA"
		oldSlavePathX86 = str(pathlib.Path(installDirX86) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDirX86

		def _getVersion(path: str, field: str):
			if path == oldSlavePathX86:
				raise RuntimeError("bad version metadata")
			self.fail("Current version lookup should not occur when old version lookup fails.")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=installDirX86,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenCurrentVersionLookupFails(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2025.1.0"}
			if path == "nvda_slave.exe":
				raise OSError("missing current executable version")
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenVersionParsingFails(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": None}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_unknown_whenPreviousVersionContainsPrereleaseTag(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2026.1.beta1"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UNKNOWN)

	def test_downgrade_whenPreviousInstallIsNewer(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2026.1.0"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.DOWNGRADE)

	def test_upgrade_whenPreviousInstallIsOlder(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2024.4.0"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UPGRADE)

	def test_reinstall_whenVersionsAreEqual(self):
		installDir = "C:\\Program Files\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path == installDir

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2025.1.0"}
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=None,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.REINSTALL)

	def test_prefersPrimaryInstallDir_whenBothPrimaryAndX86Exist(self):
		installDir = "C:\\Program Files\\NVDA"
		installDirX86 = "C:\\Program Files (x86)\\NVDA"
		oldSlavePath = str(pathlib.Path(installDir) / "nvda_slave.exe")
		oldSlavePathX86 = str(pathlib.Path(installDirX86) / "nvda_slave.exe")

		def _isdir(path: str) -> bool:
			return path in (installDir, installDirX86)

		def _getVersion(path: str, field: str):
			if path == oldSlavePath:
				return {"FileVersion": "2024.4.0"}
			if path == oldSlavePathX86:
				self.fail("x86 install path should not be used when primary install dir exists.")
			if path == "nvda_slave.exe":
				return {"FileVersion": "2025.1.0"}
			self.fail(f"Unexpected path: {path}")

		with (
			patch.object(
				installer.WritePaths.__class__,
				"installDir",
				new_callable=PropertyMock,
				return_value=installDir,
			),
			patch.object(
				installer.WritePaths.__class__,
				"_installDirX86",
				new_callable=PropertyMock,
				return_value=installDirX86,
			),
			patch("installer.os.path.isdir", side_effect=_isdir),
			patch(
				"installer.fileUtils.getFileVersionInfo",
				side_effect=_getVersion,
			),
		):
			self.assertEqual(installer._comparePreviousInstall(), installer.ComparisonState.UPGRADE)


class Test_validatePortableDirectory(unittest.TestCase):
	"""Tests for the destination directory check in the Create Portable NVDA dialog (#20159)."""

	def test_emptyDirectory_raises(self):
		with self.assertRaises(DisplayableError) as cm:
			installerGui._validatePortableDirectory("")
		self.assertIn("Please specify a directory", cm.exception.displayMessage)

	@parameterized.expand(
		[
			("bareDrive", "D:", "D:"),
			("lowercaseBareDrive", "c:", "c:"),
			("driveRelativeFolder", "D:folder", "D:"),
		],
	)
	def test_driveWithoutBackslash_raisesDriveMessage(self, _name: str, path: str, drive: str):
		with self.assertRaises(DisplayableError) as cm:
			installerGui._validatePortableDirectory(path)
		message = cm.exception.displayMessage
		self.assertIn(f"use {drive}\\ for the root of the drive", message)
		self.assertIn(f"Current path: {path}.", message)

	@parameterized.expand(
		[
			("relativeFolder", "folder"),
			("rootedWithoutDrive", "\\folder"),
		],
	)
	def test_pathWithoutDrive_raisesGeneralMessage(self, _name: str, path: str):
		with self.assertRaises(DisplayableError) as cm:
			installerGui._validatePortableDirectory(path)
		message = cm.exception.displayMessage
		self.assertIn("(e.g. C:\\)", message)
		self.assertNotIn("The drive letter must be followed by a backslash", message)

	@parameterized.expand(
		[
			("driveRoot", "D:\\", "D:\\"),
			("driveFolder", "D:\\portable\\NVDA", "D:\\portable\\NVDA"),
			("uncShare", "\\\\server\\share\\NVDA", "\\\\server\\share\\NVDA"),
		],
	)
	def test_absolutePath_returnsPath(self, _name: str, path: str, expected: str):
		self.assertEqual(installerGui._validatePortableDirectory(path), expected)

	def test_systemVariable_isExpanded(self):
		with patch.dict(os.environ, {"NVDA_TEST_PORTABLE_DIR": "D:\\portable"}):
			self.assertEqual(
				installerGui._validatePortableDirectory("%NVDA_TEST_PORTABLE_DIR%\\NVDA"),
				"D:\\portable\\NVDA",
			)


def _createFiles(root: str, sizes: dict[str, int]) -> None:
	"""Create files of the given sizes below a directory, with their parent directories."""
	for relPath, size in sizes.items():
		path = pathlib.Path(root, relPath)
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(b"x" * size)


class Test_walkProgramFiles(unittest.TestCase):
	def setUp(self) -> None:
		self._tempDir = self.enterContext(tempfile.TemporaryDirectory())
		_createFiles(
			self._tempDir,
			{
				"nvda.exe": 1,
				"nvda_slave.exe": 2,
				"userConfig/nvda.ini": 3,
				"systemConfig/nvda.ini": 4,
				"lib/nvda.exe": 5,
				"lib/userConfig/file.txt": 6,
			},
		)
		pathlib.Path(self._tempDir, "emptyDir").mkdir()

	def test_skipsConfigDirectoriesAndNvdaExeOnlyAtTopLevel(self):
		self.assertEqual(
			dict(installer._walkProgramFiles(self._tempDir)),
			{
				".": {"nvda_slave.exe": 2},
				"lib": {"nvda.exe": 5},
				os.path.join("lib", "userConfig"): {"file.txt": 6},
				"emptyDir": {},
			},
		)


class Test_copyFiles(unittest.TestCase):
	"""Tests for the byte progress of copying the program files and the user configuration."""

	def setUp(self) -> None:
		self._sourceDir = self.enterContext(tempfile.TemporaryDirectory())
		self._destDir = self.enterContext(tempfile.TemporaryDirectory())
		self._onProgress = MagicMock()

	def _assertByteProgress(self, total: int) -> None:
		"""Assert that progress was reported in bytes, never going down, up to the given total."""
		reports = [c.args for c in self._onProgress.call_args_list]
		self.assertTrue(reports)
		self.assertEqual({reportTotal for _done, reportTotal in reports}, {total})
		done = [d for d, _total in reports]
		self.assertEqual(done, sorted(done))
		self.assertEqual(done[-1], total)

	def test_copyProgramFiles_reportsBytes(self):
		_createFiles(self._sourceDir, {"nvda.exe": 7, "nvda_slave.exe": 3, "lib/nvdaHelperRemote.dll": 5})
		with patch("installer.globalVars.appDir", self._sourceDir):
			installer.copyProgramFiles(self._destDir, self._onProgress)
		self._assertByteProgress(8)
		self.assertTrue(os.path.isfile(os.path.join(self._destDir, "lib", "nvdaHelperRemote.dll")))

	def test_copyUserConfig_reportsBytes(self):
		_createFiles(self._sourceDir, {"nvda.ini": 3, "profiles/profile.ini": 5})
		with patch.object(
			installer.WritePaths.__class__,
			"configDir",
			new_callable=PropertyMock,
			return_value=self._sourceDir,
		):
			installer.copyUserConfig(self._destDir, self._onProgress)
		self._assertByteProgress(8)
		self.assertTrue(os.path.isfile(os.path.join(self._destDir, "profiles", "profile.ini")))


class Test_createPortableCopy(unittest.TestCase):
	"""Tests for the progress reported while creating a portable copy."""

	def setUp(self) -> None:
		sourceDir = self.enterContext(tempfile.TemporaryDirectory())
		configDir = self.enterContext(tempfile.TemporaryDirectory())
		self._destDir = self.enterContext(tempfile.TemporaryDirectory())
		_createFiles(
			sourceDir,
			{"nvda_noUIAccess.exe": 10, "nvda_slave.exe": 10, "lib/nvdaHelperRemote.dll": 10},
		)
		_createFiles(configDir, {"nvda.ini": 90})
		self.enterContext(patch("installer.globalVars.appDir", sourceDir))
		self.enterContext(
			patch.object(
				installer.WritePaths.__class__,
				"configDir",
				new_callable=PropertyMock,
				return_value=configDir,
			),
		)
		self._reports: list[tuple[installer._PortableCopyStep, int]] = []

	def _createPortableCopy(self, shouldCopyUserConfig: bool) -> dict[installer._PortableCopyStep, int]:
		"""Create a portable copy and return the percentage at which each reported step started, in order."""
		installer.createPortableCopy(
			self._destDir,
			shouldCopyUserConfig,
			progressCallback=lambda step, percentage: self._reports.append((step, percentage)),
		)
		stepStarts: dict[installer._PortableCopyStep, int] = {}
		for step, percentage in self._reports:
			stepStarts.setdefault(step, percentage)
		return stepStarts

	def test_reportsStepsWithCopyRangeSharedByBytes(self):
		Step = installer._PortableCopyStep
		copyStart = Step.COPY_FILES.startPercentage
		copyEnd = Step.REMOVE_OLD_FILES.startPercentage
		self.assertEqual(
			list(self._createPortableCopy(shouldCopyUserConfig=True).items()),
			[
				(Step.REMOVE_PREVIOUS, Step.REMOVE_PREVIOUS.startPercentage),
				(Step.COPY_FILES, copyStart),
				# 30 bytes of program files and 90 bytes of configuration share the copy range.
				(Step.COPY_USER_CONFIG, int(copyStart + (copyEnd - copyStart) * 30 / 120)),
				(Step.REMOVE_OLD_FILES, copyEnd),
			],
		)

	def test_withoutUserConfig_skipsConfigStep(self):
		Step = installer._PortableCopyStep
		self.assertEqual(
			list(self._createPortableCopy(shouldCopyUserConfig=False)),
			[Step.REMOVE_PREVIOUS, Step.COPY_FILES, Step.REMOVE_OLD_FILES],
		)
		self.assertIn((Step.COPY_FILES, Step.REMOVE_OLD_FILES.startPercentage), self._reports)


class Test_createInstallProgressTracker(unittest.TestCase):
	def _stepStart(self, step: installer._InstallStep, userConfigSize: int) -> int:
		"""Start a step on a new install tracker with 300 bytes of program files, returning its percentage."""
		reports: list[tuple[installer._InstallStep, int]] = []
		tracker = installer._createInstallProgressTracker(
			lambda step, percentage: reports.append((step, percentage)),
			programFilesSize=300,
			userConfigSize=userConfigSize,
		)
		tracker.startStep(step)
		return reports[-1][1]

	def test_withoutUserConfig_keepsStaticRanges(self):
		for step in installer._InstallStep:
			with self.subTest(step=step):
				self.assertEqual(self._stepStart(step, userConfigSize=0), step.startPercentage)

	def test_userConfigSize_sharesCopyRange(self):
		Step = installer._InstallStep
		sharedWidth = (
			Step.REMOVE_OLD_FILES.startPercentage
			- Step.COPY_FILES.startPercentage
			+ 100
			- Step.COPY_USER_CONFIG.startPercentage
		)
		# The steps between copying files and copying the configuration keep their widths.
		betweenWidth = Step.COPY_USER_CONFIG.startPercentage - Step.REMOVE_OLD_FILES.startPercentage
		self.assertEqual(
			self._stepStart(Step.COPY_USER_CONFIG, userConfigSize=600),
			int(Step.COPY_FILES.startPercentage + sharedWidth * 300 / 900 + betweenWidth),
		)


class Test_doInstallCopyConfig(unittest.TestCase):
	def test_passesConfigSizeAndReportsConfigStep(self):
		with (
			patch("gui.installerGui._DeterminateProgressDialog") as dialogMock,
			patch("gui.installerGui.shell32.IsUserAnAdmin", return_value=True),
			patch("gui.installerGui.systemUtils.execElevated", return_value=0) as execElevatedMock,
			patch("gui.installerGui._canPortableConfigBeCopied", return_value=True),
			patch("gui.installerGui.config.getInstalledUserConfigPath", return_value="C:\\config"),
			patch("installer._getUserConfigSize", return_value=600),
			patch("installer._getProgramFilesSize", return_value=300),
			patch("gui.installerGui.systemUtils.ExecAndPump") as execAndPumpMock,
			patch("gui.installerGui._showPostInstallDialog"),
		):
			installerGui.doInstall(copyPortableConfig=True)
		self.assertEqual(execElevatedMock.call_args.args[1][4], "600")
		dialogMock.return_value.setStep.assert_called_once_with(installer._InstallStep.COPY_USER_CONFIG, ANY)
		execAndPumpMock.assert_called_once_with(installer.copyUserConfig, "C:\\config", ANY)


class Test_doCreatePortable(unittest.TestCase):
	def test_passesDialogSetStepAsProgressCallback(self):
		with (
			patch("gui.installerGui._DeterminateProgressDialog") as dialogMock,
			patch("gui.installerGui.systemUtils.ExecAndPump") as execAndPumpMock,
			patch("gui.installerGui.gui.messageBox"),
		):
			installerGui.doCreatePortable("D:\\portable\\NVDA", warnForNonEmptyDirectory=False)
		execAndPumpMock.assert_called_once_with(
			installer.createPortableCopy,
			"D:\\portable\\NVDA",
			False,
			progressCallback=dialogMock.return_value.setStep,
		)
		dialogMock.return_value.done.assert_called_once_with()
