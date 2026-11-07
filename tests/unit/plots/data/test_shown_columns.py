"""
Unit tests of the columns shown by the charts of a Plot and the checks of their shown names.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

import numdaplot as ndp
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.chart_values import Series
from numdaplot.plots.data.missing_cells import read_missing_counts
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.data.sample_values import SampleValues
from numdaplot.plots.data.shown_columns import (
	find_point_columns,
	find_shown_columns,
	find_value_columns,
	optional_names,
	require_distinct_shown_names,
	require_renamed_columns_shown,
)
from numdaplot.plots.data.table_values import read_table_values

DAYS = ndp.Array.from_list([1, 2])
PRICES = ndp.Array.from_list([12.0, None])
COSTS = ndp.Array.from_list([8.0, 9.0])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "cost": COSTS})
LINE_VALUES = read_table_values(SALES, "day", ["price", "cost"], "LineChart")
LINE_LAYER = ChartLayer(ndp.LineChart(), LINE_VALUES)
EXPECTED_LINE_COLUMNS = {"day", "price", "cost"}
PRICE_SERIES = Series("price", numpy.array([12.0]))
SAMPLES = SampleValues([PRICE_SERIES], None, "city", "price", ndp.Type.FLOAT64)
EXPECTED_SAMPLE_COLUMNS = ["price", "city"]
EXPECTED_MISSING_COLUMNS = ["day", "price", "cost"]
COLORED_POINTS = PointValues("zone", None, "passengers", None)
EXPECTED_POINT_COLUMNS = ["zone", "passengers"]
POINT_LAYER = ChartLayer(ndp.ScatterChart(), LINE_VALUES, COLORED_POINTS)
EXPECTED_POINT_LAYER_COLUMNS = {"day", "price", "cost", "zone", "passengers"}
PRICE_AS_COST = ndp.Renaming(changes=[ndp.NameChange(old_name="price", new_name="cost")])
SWAPPED_NAMES = ndp.Renaming(
	changes=[ndp.NameChange(old_name="price", new_name="cost"), ndp.NameChange(old_name="cost", new_name="price")]
)
PRICE_AS_PRICE_LABEL = ndp.Renaming(changes=[ndp.NameChange(old_name="price", new_name="Price")])
MISSPELLED_PRICE = ndp.Renaming(changes=[ndp.NameChange(old_name="prise", new_name="Price")])


def test_find_shown_columns_gives_the_x_and_drawn_columns() -> None:
	"""
	Check the columns of a line chart drawing two columns along a third one.

	.. versionadded:: 0.1.0
	"""
	shown_columns = find_shown_columns([LINE_LAYER])

	assert shown_columns == EXPECTED_LINE_COLUMNS


def test_find_shown_columns_adds_the_color_and_size_columns() -> None:
	"""
	Check that the columns of the colors and sizes of points are shown columns.

	.. versionadded:: 0.1.0
	"""
	shown_columns = find_shown_columns([POINT_LAYER])

	assert shown_columns == EXPECTED_POINT_LAYER_COLUMNS


def test_find_value_columns_gives_the_drawn_and_group_columns_of_samples() -> None:
	"""
	Check the columns of a box chart grouped by another column.

	.. versionadded:: 0.1.0
	"""
	value_columns = find_value_columns(SAMPLES)

	assert value_columns == EXPECTED_SAMPLE_COLUMNS


def test_find_value_columns_gives_the_positions_of_missing_counts() -> None:
	"""
	Check that the columns of a missing value chart are its positions.

	.. versionadded:: 0.1.0
	"""
	counts = read_missing_counts(SALES, ndp.Measure.COUNT)

	value_columns = find_value_columns(counts)

	assert value_columns == EXPECTED_MISSING_COLUMNS


def test_find_point_columns_gives_the_color_and_size_columns() -> None:
	"""
	Check the columns of the colors and the sizes of points.

	.. versionadded:: 0.1.0
	"""
	point_columns = find_point_columns(COLORED_POINTS)

	assert point_columns == EXPECTED_POINT_COLUMNS


@pytest.mark.parametrize(("name", "expected"), [("day", ["day"]), (None, [])])
def test_optional_names_gives_the_name_or_nothing(name: str | None, expected: list[str]) -> None:
	"""
	Check the list made of an optional name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		A name or None.
	expected
		The list expected.
	"""
	names = optional_names(name)

	assert names == expected


def test_require_distinct_shown_names_rejects_the_name_of_a_kept_column() -> None:
	"""
	Check that showing price as cost, a column keeping its name, raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		require_distinct_shown_names([LINE_LAYER], PRICE_AS_COST)


@pytest.mark.parametrize("renaming", [None, SWAPPED_NAMES, PRICE_AS_PRICE_LABEL])
def test_require_distinct_shown_names_accepts_distinct_names(renaming: ndp.Renaming | None) -> None:
	"""
	Check that no renaming, a swap and a new name raise nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	renaming
		An accepted renaming.
	"""
	require_distinct_shown_names([LINE_LAYER], renaming)


def test_require_renamed_columns_shown_rejects_a_column_no_chart_shows() -> None:
	"""
	Check that a misspelled column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		require_renamed_columns_shown([LINE_LAYER], MISSPELLED_PRICE)


@pytest.mark.parametrize("renaming", [None, PRICE_AS_PRICE_LABEL])
def test_require_renamed_columns_shown_accepts_shown_columns(renaming: ndp.Renaming | None) -> None:
	"""
	Check that no renaming and a renaming of a shown column raise nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	renaming
		An accepted renaming.
	"""
	require_renamed_columns_shown([LINE_LAYER], renaming)
