# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Utilities for hyphenation."""

from characterProcessing import LocaleDataMap
from logHandler import log
from pyphen import Pyphen, language_fallback


def _pyphenFactory(lang: str) -> Pyphen:
	"""Factory for Pyphen instances."""
	pyphenLang = language_fallback(lang)
	if not pyphenLang:
		raise LookupError(f"No Pyphen language found for locale '{lang}'")
	elif "_" in lang and "_" not in pyphenLang:
		raise LookupError(
			f"Pyphen resolved {lang!r} to {pyphenLang!r} but the original locale contains a region subtag. "
			"Fallbacks should be handled by LocaleDataMap instead",
		)
	return Pyphen(lang=pyphenLang)


_hypenationMap: LocaleDataMap[Pyphen] = LocaleDataMap(_pyphenFactory)

#: Set of locales for which we have already logged an unknown-language fallback.
#: Used to avoid spamming the log on every call for the same unsupported locale.
_loggedUnknownLocales: set[str] = set()


def getHyphenPositions(text: str, locale: str) -> tuple[int, ...]:
	"""Get the positions of hyphenation points in the given text for the given locale.

	If no hyphenation dictionary is available for the locale, an empty tuple is returned
	and a debug message is logged (once per locale).

	:param text: The text to find hyphenation points in.
	:param locale: The locale of the text.
	:return: A tuple of positions in the text where hyphenation points occur.
	"""
	try:
		pyphen = _hypenationMap.fetchLocaleData(locale=locale)
	except LookupError:
		if locale not in _loggedUnknownLocales:
			_loggedUnknownLocales.add(locale)
			log.debug(f"No Pyphen dictionary available for locale {locale!r}; hyphenation disabled.")
		return ()
	return tuple(pyphen.positions(text))
