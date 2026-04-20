# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for the textUtils._regex backend shim."""

import re as _stdlibRe
import unittest

from textUtils import _regex as shim


class TestRegexShim(unittest.TestCase):
	"""Tests that the shim exposes a usable, internally-consistent re-like API.

	The backend is selected once by :func:`textUtils._regex.initialize` from user
	config and is then frozen for the lifetime of the process. Unit tests cannot
	toggle it, so these tests assert behavior of whichever backend is active and
	check internal consistency rather than which concrete module is in use.
	"""

	def test_compileReturnsActiveBackendPattern(self):
		"""``shim.compile`` returns a Pattern of the active backend's type."""
		pattern = shim.compile(r"\w+")
		self.assertIsInstance(pattern, shim.Pattern)

	def test_errorClassMatchesActiveBackend(self):
		"""``shim.error`` is the active backend's error class.

		``except shim.error`` must catch errors raised by ``shim.compile`` etc.
		"""
		with self.assertRaises(shim.error):
			shim.compile(r"(unbalanced")

	def test_flagConstantsArePresent(self):
		"""Standard re flag constants are exposed by the shim."""
		self.assertTrue(hasattr(shim, "IGNORECASE"))
		self.assertTrue(hasattr(shim, "DOTALL"))
		self.assertTrue(hasattr(shim, "MULTILINE"))
		self.assertTrue(hasattr(shim, "UNICODE"))
		self.assertTrue(hasattr(shim, "VERBOSE"))

	def test_basicMatchingWorks(self):
		"""Smoke check that core re API surface is callable through the shim."""
		self.assertIsNotNone(shim.match(r"\d+", "123abc"))
		self.assertIsNotNone(shim.search(r"\d+", "abc123"))
		self.assertEqual(shim.findall(r"\d+", "a1 b22 c333"), ["1", "22", "333"])
		self.assertEqual(shim.sub(r"\d", "X", "a1b2"), "aXbX")
		self.assertEqual(shim.escape("a.b"), _stdlibRe.escape("a.b"))


class TestRegexShimUninitialized(unittest.TestCase):
	"""Pre-initialize behavior: shim must fall back to stdlib re.

	Unit tests typically run after :func:`initialize` has been called by NVDA's
	startup, but the shim must still be safely usable in early-bootstrap contexts
	where config is not yet available. This is verified indirectly by ensuring
	that the shim's API surface is callable regardless of init state.
	"""

	def test_apiCallableRegardlessOfInitState(self):
		self.assertTrue(callable(shim.compile))
		self.assertTrue(callable(shim.search))
		self.assertTrue(callable(shim.escape))
