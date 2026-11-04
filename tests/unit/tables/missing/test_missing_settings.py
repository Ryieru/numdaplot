"""
Unit tests of MissingCount, MissingRatio and MissingDrop.

.. versionadded:: 0.1.0
"""

import math

import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_fraction_error import InvalidFractionError
from numdaplot.positions.axis import Axis
from numdaplot.ratios.measure import Measure
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.missing.missing_mode import MissingMode
from numdaplot.tables.missing.missing_ratio import MissingRatio
from numdaplot.tables.missing.ratio_comparison import RatioComparison

HALF_RATIO = 0.5
REJECTED_RATIOS = [-0.1, 1.5, math.nan]
EMPTY_NAMES = list[str]()
REPEATED_NAMES = ["price", "price"]
LOOKED_NAMES = ["price"]
ADDED_NAME = "stock"


def test_missing_count_counts_the_whole_table_by_default() -> None:
	"""
	Check the default axis and measure.

	.. versionadded:: 0.1.0
	"""
	missing_count = MissingCount()

	assert missing_count.axis is None
	assert missing_count.measure == Measure.COUNT


def test_missing_ratio_reaches_its_threshold_at_least_by_default() -> None:
	"""
	Check the default comparison.

	.. versionadded:: 0.1.0
	"""
	missing_ratio = MissingRatio(ratio=HALF_RATIO)

	assert missing_ratio.comparison == RatioComparison.AT_LEAST


@pytest.mark.parametrize("ratio", REJECTED_RATIOS)
def test_missing_ratio_rejects_a_value_that_is_not_a_fraction(ratio: float) -> None:
	"""
	Check that a ratio outside 0 to 1, or NaN, raises InvalidFractionError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	ratio
		A rejected ratio.
	"""
	with pytest.raises(InvalidFractionError):
		MissingRatio(ratio=ratio)


def test_missing_drop_removes_rows_with_any_missing_value_in_every_column_by_default() -> None:
	"""
	Check the default axis, columns and rule.

	.. versionadded:: 0.1.0
	"""
	missing_drop = MissingDrop()

	assert missing_drop.axis == Axis.EACH_ROW
	assert missing_drop.columns is None
	assert missing_drop.rule == MissingMode.ANY


def test_missing_drop_rejects_an_empty_list_of_columns() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		MissingDrop(columns=EMPTY_NAMES)


def test_missing_drop_rejects_a_repeated_column() -> None:
	"""
	Check that a column named twice raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		MissingDrop(columns=REPEATED_NAMES)


def test_missing_drop_keeps_its_own_copy_of_the_columns() -> None:
	"""
	Check that changing the given list afterwards does not change the settings.

	.. versionadded:: 0.1.0
	"""
	looked_names = list(LOOKED_NAMES)
	missing_drop = MissingDrop(columns=looked_names)

	looked_names.append(ADDED_NAME)

	assert missing_drop.columns == LOOKED_NAMES
