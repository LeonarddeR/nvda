# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Unit tests for the high level remote operations in UIAHandler.remote.
"""

from unittest import TestCase
from unittest.mock import Mock, patch
from ctypes import POINTER
from comtypes import COMError
import UIAHandler
import UIAHandler.remote
from UIAHandler import UIA
from UIAHandler._remoteOps import operation
from UIAHandler._remoteOps.lowLevel import (
	PatternId,
	PropertyId,
)


_OriginalOperation = operation.Operation


def _localOperation(*args, **kwargs):
	kwargs["localMode"] = True
	return _OriginalOperation(*args, **kwargs)


class Test_getAncestorsWithCache(TestCase):
	def _providerElement(self) -> tuple[Mock, Mock]:
		element = Mock(spec=POINTER(UIA.IUIAutomationElement))
		cachedElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		cachedElement.QueryInterface.return_value = cachedElement
		element.BuildUpdatedCache.return_value = cachedElement
		return element, cachedElement

	def _run(self, parentResults, propertyIds, **kwargs) -> tuple[list | None, Mock]:
		startElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		handlerMock = Mock()
		handlerMock.clientObject.RawViewWalker.GetParentElement.side_effect = parentResults
		with (
			patch.object(UIAHandler.remote, "_isSupported", True),
			patch.object(UIAHandler.remote.operation, "Operation", _localOperation),
			patch.object(UIAHandler, "handler", handlerMock),
		):
			result = UIAHandler.remote.getAncestorsWithCache(startElement, propertyIds, **kwargs)
		return result, handlerMock

	def test_unsupported_returnsNone(self):
		startElement = Mock(spec=POINTER(UIA.IUIAutomationElement))
		self.assertIsNone(
			UIAHandler.remote.getAncestorsWithCache(startElement, [UIA.UIA_NamePropertyId]),
		)

	def test_walk_yieldsCachedAncestorsUntilNullParent(self):
		parent1, cached1 = self._providerElement()
		parent2, cached2 = self._providerElement()
		result, handlerMock = self._run(
			[parent1, parent2, None],
			[UIA.UIA_NamePropertyId, UIA.UIA_ControlTypePropertyId],
		)
		self.assertEqual(result, [cached1, cached2])
		cacheRequest = handlerMock.clientObject.CreateCacheRequest.return_value
		parent1.BuildUpdatedCache.assert_called_once_with(cacheRequest)
		parent2.BuildUpdatedCache.assert_called_once_with(cacheRequest)

	def test_walk_appliesRequestedPropertiesAndPatterns(self):
		parent1, cached1 = self._providerElement()
		result, handlerMock = self._run(
			[parent1, None],
			[UIA.UIA_NamePropertyId],
			patternIds=[UIA.UIA_TextPatternId],
		)
		self.assertEqual(result, [cached1])
		cacheRequest = handlerMock.clientObject.CreateCacheRequest.return_value
		cacheRequest.AddProperty.assert_called_once_with(PropertyId.Name)
		cacheRequest.AddPattern.assert_called_once_with(PatternId.Text)

	def test_walk_respectsMaxDepth(self):
		parents = [self._providerElement() for _ in range(4)]
		result, handlerMock = self._run(
			[parent for parent, _ in parents],
			[UIA.UIA_NamePropertyId],
			maxDepth=2,
		)
		self.assertEqual(result, [cached for _, cached in parents[:2]])
		walker = handlerMock.clientObject.RawViewWalker
		self.assertEqual(walker.GetParentElement.call_count, 2)

	def test_walk_keepsAncestorsBeforeNavigationFailure(self):
		parent1, cached1 = self._providerElement()
		result, _ = self._run(
			[parent1, COMError(-2147467259, "gone", (None, None, None, 0, None))],
			[UIA.UIA_NamePropertyId],
		)
		self.assertEqual(result, [cached1])

	def test_walk_withoutAncestors_returnsNone(self):
		result, _ = self._run([None], [UIA.UIA_NamePropertyId])
		self.assertIsNone(result)
