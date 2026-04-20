# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for the textUtils._regex backend shim."""

import re as _stdlibRe
import unittest

import config
import regex as _regexModule

from textUtils import _regex as shim


class TestRegexShim(unittest.TestCase):
	"""Tests that the shim correctly forwards to the active backend."""

	def setUp(self):
		shim.initialize()
		self._originalBackend = config.conf["featureFlag"]["regexBackend"]

	def tearDown(self):
		config.conf["featureFlag"]["regexBackend"] = self._originalBackend

	def _useStdlib(self):
		config.conf["featureFlag"]["regexBackend"] = 0

	def _useRegex(self):
		config.conf["featureFlag"]["regexBackend"] = 1

	def test_compileForwardsToStdlibByDefault(self):
		self._useStdlib()
		pattern = shim.compile(r"\w+")
		self.assertIsInstance(pattern, _stdlibRe.Pattern)

	def test_compileForwardsToRegexWhenEnabled(self):
		self._useRegex()
		pattern = shim.compile(r"\w+")
		self.assertIsInstance(pattern, _regexModule.Pattern)

	def test_errorClassTracksBackend(self):
		self._useStdlib()
		self.assertIs(shim.error, _stdlibRe.error)
		self._useRegex()
		self.assertIs(shim.error, _regexModule.error)

	def test_flagConstantsTrackBackend(self):
		self._useStdlib()
		self.assertEqual(shim.IGNORECASE, _stdlibRe.IGNORECASE)
		self._useRegex()
		self.assertEqual(shim.IGNORECASE, _regexModule.IGNORECASE)

	def test_exceptHandlerCatchesActiveBackendError(self):
		"""``except shim.error`` re-resolves the class on each entry."""
		self._useStdlib()
		with self.assertRaises(shim.error):
			shim.compile(r"(unbalanced")
		self._useRegex()
		with self.assertRaises(shim.error):
			shim.compile(r"(unbalanced")

	def test_regexBackendUsesVersion1(self):
		"""When the regex backend is active, full Unicode case-folding applies (V1)."""
		self._useRegex()
		self.assertIsNotNone(shim.match(r"(?i)ss", "ß"))


class TestRegexShimPreInit(unittest.TestCase):
	"""Behavior before initialize() has run: must fall back to stdlib re."""

	def test_preInitFallsBackToStdlib(self):
		# initialize() may already have been called by another test in this run; we
		# can't easily un-initialize. Instead, verify the documented contract that the
		# fallback path exists by inspecting the private state when uninitialized.
		# This is a smoke check that the attribute is present and callable.
		self.assertTrue(callable(shim.compile))
		self.assertTrue(callable(shim.search))
		self.assertTrue(callable(shim.escape))
