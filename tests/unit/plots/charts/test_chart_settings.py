"""
Unit tests of the column and color checks shared by the charts.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.plots.charts.chart_settings import copy_colors, copy_columns
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

COLUMNS = ["price", "cost"]
DUPLICATED_COLUMNS = ["price", "price"]
COLORS = [Color.BLUE, CustomColor("#ff8800")]


def test_copy_columns_keeps_none_for_an_array() -> None:
	"""
	Check that no columns stay None.

	.. versionadded:: 0.1.0
	"""
	columns_copy = copy_columns(None)

	assert columns_copy is None


def test_copy_columns_returns_an_equal_list_that_is_not_the_given_one() -> None:
	"""
	Check that the names are copied, so changing the given list changes nothing.

	.. versionadded:: 0.1.0
	"""
	columns_copy = copy_columns(COLUMNS)

	assert columns_copy == COLUMNS
	assert columns_copy is not COLUMNS


def test_copy_columns_rejects_an_empty_list() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		copy_columns([])


def test_copy_columns_rejects_a_duplicated_name() -> None:
	"""
	Check that a name given twice raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		copy_columns(DUPLICATED_COLUMNS)


def test_copy_colors_returns_an_equal_list_that_is_not_the_given_one() -> None:
	"""
	Check that the colors are copied.

	.. versionadded:: 0.1.0
	"""
	colors_copy = copy_colors(COLORS)

	assert colors_copy == COLORS
	assert colors_copy is not COLORS


def test_copy_colors_keeps_none_for_the_default_cycle() -> None:
	"""
	Check that no colors stay None.

	.. versionadded:: 0.1.0
	"""
	colors_copy = copy_colors(None)

	assert colors_copy is None


def test_copy_colors_rejects_an_empty_list() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		copy_colors([])
