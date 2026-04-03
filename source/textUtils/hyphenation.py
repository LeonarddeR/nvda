# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Utilities for hyphenation."""

from characterProcessing import LocaleDataMap
from pyphen import Pyphen, language_fallback


def _pyphenFactory(lang: str) -> Pyphen:
	"""Factory for Pyphen instances."""
	pyphenLang = language_fallback(lang)
	if not pyphenLang:
		raise LookupError(f"No Pyphen language found for locale '{lang}'")
	elif "_" in lang and "_" not in pyphenLang:
		raise LookupError(
			f"Pyphen resolved {lang!r} to {pyphenLang:r} but the original locale contains a region subtag. "
			"Fallbacks should be handled by LocaleDataMap instead"
		)
	return Pyphen(lang=pyphenLang)


_hypenationMap: LocaleDataMap[Pyphen] = LocaleDataMap(_pyphenFactory)


def getHyphenPositions(text: str, locale: str):
	"""Get the positions of hyphenation points in the given text for the given locale."""
	pyphen = _hypenationMap.fetchLocaleData(locale=locale)
	return pyphen.positions(text)
