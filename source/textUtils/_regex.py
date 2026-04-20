# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Internal regex backend shim.

Forwards attribute access to either stdlib :mod:`re` or the third-party :mod:`regex`
module. The backend is chosen once by :func:`initialize` from the ``regexBackend``
feature flag in user config and is then frozen for the lifetime of the process.
Changes to the setting therefore require an NVDA restart.

Intended usage::

	from textUtils import _regex as re

	pattern = re.compile(r"\\w+", re.IGNORECASE)

Before :func:`initialize` runs (early bootstrap, unit tests outside startup),
attribute access falls back to stdlib :mod:`re`.
"""

import re as _re


_backend = _re


def initialize() -> None:
	"""Resolve the regex backend from user config and freeze it for this process.

	Call once after :func:`config.initialize`. Subsequent calls are ignored.
	"""
	global _backend
	if _backend is not _re:
		return
	import config

	if config.conf["featureFlag"]["regexBackend"] != 1:
		return
	import regex

	regex.DEFAULT_VERSION = regex.VERSION1
	_backend = regex


def __getattr__(name: str):
	return getattr(_backend, name)
