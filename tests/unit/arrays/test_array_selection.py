"""
Unit tests of ArraySelection.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_selection
from numdaplot.arrays.array_selection import ArraySelection
from numdaplot.arrays.replacement import Replacement
from numdaplot.positions.index import Index
from numdaplot.positions.region import Region
from numdaplot.rules.greater import Greater
from numdaplot.rules.rule import Rule

BUILD_RULE_MASK_NAME = "build_rule_mask"
BUILD_REGION_INDEX_NAME = "build_region_index"
REPLACE_REGION_NAME = "replace_region"
GRID = [[5, 12], [30, 8]]
FAKE_MASK = numpy.array([[False, True], [True, False]])
EXPECTED_SELECTED_VALUES = [12, 30]
EXPECTED_MASK = [[False, True], [True, False]]
FAKE_REGION_INDEX = (numpy.array([[1]]), numpy.array([[0, 1]]))
EXPECTED_TAKEN_VALUES = [[30, 8]]
FAKE_REPLACED_VALUES = numpy.array([[0, 0], [0, 0]])
EXPECTED_REPLACED_VALUES = [[0, 0], [0, 0]]
RULE = Greater(10)
REGION = Region(rows=Index(1))
NEW_VALUE = 0


def build_fake_mask(values: NDArray[Any], rule: Rule) -> NDArray[numpy.bool_]:
	"""
	Fake mask builder returning a known mask.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, ignored.
	rule
		The rule, ignored.

	Returns
	-------
	NDArray[numpy.bool_]
		Always the fake mask.
	"""
	return FAKE_MASK


def build_fake_region_index(region: Region, dimensions: tuple[int, ...]) -> tuple[NDArray[Any], ...]:
	"""
	Fake region index selecting the second row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	region
		The region, ignored.
	dimensions
		The dimensions, ignored.

	Returns
	-------
	tuple[NDArray, ...]
		Always the index of the second row.
	"""
	return FAKE_REGION_INDEX


def replace_with_fake_values(values: NDArray[Any], region: Region, new_values: object) -> NDArray[Any]:
	"""
	Fake replacement returning known values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, ignored.
	region
		The region, ignored.
	new_values
		The new values, ignored.

	Returns
	-------
	NDArray
		Always the fake replaced values.
	"""
	return FAKE_REPLACED_VALUES


def read_values(array: ArraySelection) -> list[Any]:
	"""
	Return the values of an Array as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	array
		The Array.

	Returns
	-------
	list[Any]
		Its values.
	"""
	numpy_values = array.to_numpy()
	raw_values = numpy_values.tolist()
	value_list = cast(list[Any], raw_values)

	return value_list


def test_select_keeps_the_values_of_the_mask(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that select keeps the values where the mask is True, in one dimension.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the mask builder with a fake.
	"""
	monkeypatch.setattr(array_selection, BUILD_RULE_MASK_NAME, build_fake_mask)
	values = numpy.array(GRID)
	array = ArraySelection(values)

	selected_array = array.select(RULE)

	selected_values = read_values(selected_array)
	assert selected_values == EXPECTED_SELECTED_VALUES


def test_check_returns_the_mask(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that check returns the mask itself, in the shape of the Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the mask builder with a fake.
	"""
	monkeypatch.setattr(array_selection, BUILD_RULE_MASK_NAME, build_fake_mask)
	values = numpy.array(GRID)
	array = ArraySelection(values)

	mask_array = array.check(RULE)

	mask_values = read_values(mask_array)
	assert mask_values == EXPECTED_MASK


def test_take_returns_the_values_of_the_region_index(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that take returns the values selected by the region index.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the region index with a fake selecting the second row.
	"""
	monkeypatch.setattr(array_selection, BUILD_REGION_INDEX_NAME, build_fake_region_index)
	values = numpy.array(GRID)
	array = ArraySelection(values)

	taken_array = array.take(REGION)

	taken_values = read_values(taken_array)
	assert taken_values == EXPECTED_TAKEN_VALUES


def test_replace_returns_the_replaced_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that replace returns what the replacement gives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the replacement with a fake.
	"""
	monkeypatch.setattr(array_selection, REPLACE_REGION_NAME, replace_with_fake_values)
	values = numpy.array(GRID)
	array = ArraySelection(values)
	replacement = Replacement(region=REGION, value=NEW_VALUE)

	replaced_array = array.replace(replacement)

	replaced_values = read_values(replaced_array)
	assert replaced_values == EXPECTED_REPLACED_VALUES
