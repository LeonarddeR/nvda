# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Internal regex backend shim.

Forwards attribute access to either stdlib :mod:`re` or the third-party :mod:`regex`
module, selected at every access via the ``regexBackend`` feature flag in user config.

Intended usage::

	from textUtils import _regex as re

	pattern = re.compile(r"\\w+", re.IGNORECASE)

Because module attributes are not cached after :pep:`562` ``__getattr__`` returns,
each ``re.compile(...)``/``re.IGNORECASE``/``re.error`` access re-resolves the active
backend. Toggling the feature flag therefore takes effect immediately for new
compilations; ``Pattern`` objects already compiled stay bound to the backend that
created them until NVDA is restarted.

Before :func:`initialize` runs (early bootstrap, unit tests outside startup) or if
config is unavailable, attribute access falls back to stdlib :mod:`re`.
"""

import re as _re


_regexModule = None


def initialize() -> None:
	"""Eagerly import the :mod:`regex` module and configure VERSION1 semantics.

	Call once after :func:`config.initialize` so that subsequent attribute access can
	resolve the ``regex`` backend without paying import cost on a hot path. Idempotent.
	"""
	global _regexModule
	if _regexModule is not None:
		return
	import regex

	regex.DEFAULT_VERSION = regex.VERSION1
	_regexModule = regex


def _getBackend():
	if _regexModule is None:
		return _re
	try:
		import config

		if config.conf["featureFlag"]["regexBackend"] == 1:
			return _regexModule
	except Exception:
		pass
	return _re


def __getattr__(name: str):
	return getattr(_getBackend(), name)
