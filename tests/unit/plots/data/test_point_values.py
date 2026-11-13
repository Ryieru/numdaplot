"""
Unit tests of the values coloring and sizing the points of a ScatterChart.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

import numdaplot as ndp
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.point_values import (
	hide_missing_points,
	read_category_order,
	read_colors,
	read_point_values,
)
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.tables.table_data import read_stored_frame

FLATS_FRAME = pandas.DataFrame(
	{
		"surface": [30.0, 45.0, 60.0],
		"price": [150.0, 210.0, 260.0],
		"city": ["Paris", None, "Pau"],
		"rooms": [1.0, 2.0, None],
		"open": [True, False, True],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
ALL_ROWS = numpy.arange(3)
SOME_ROWS = numpy.array([0, 2])
EXPECTED_SOME_SIZES = [30.0, 60.0]
AGES = [25, 5, 70]
AGE_BRACKETS = ndp.Brackets(limits=[0, 10, 20, 100])
EXPECTED_AGE_ORDER = ["0 to 9", "10 to 19", "20 to 99"]
AGE_COLUMN = "age"
CITY_COLUMN = "city"


def test_read_point_values_reads_the_given_columns_for_the_drawn_rows() -> None:
	"""
	Check that the color and size values follow the drawn rows.

	.. versionadded:: 0.1.0
	"""
	point_values = read_point_values(FLATS, "city", "surface", SOME_ROWS)

	assert point_values.colors is not None
	assert point_values.sizes is not None
	colors = point_values.colors.tolist()
	sizes = point_values.sizes.tolist()
	assert colors == ["Paris", "Pau"]
	assert sizes == EXPECTED_SOME_SIZES


def test_read_point_values_keeps_none_without_columns() -> None:
	"""
	Check that a chart without color_by and size_by reads nothing.

	.. versionadded:: 0.1.0
	"""
	point_values = read_point_values(FLATS, None, None, ALL_ROWS)

	assert point_values.colors is None
	assert point_values.sizes is None


def test_read_point_values_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown size_by column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		read_point_values(FLATS, None, "surfaec", ALL_ROWS)


def test_read_point_values_rejects_sizes_that_are_not_numbers() -> None:
	"""
	Check that a text size_by column raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_point_values(FLATS, None, "city", ALL_ROWS)


def test_read_colors_writes_booleans_as_texts() -> None:
	"""
	Check that a boolean color_by column gives one text per value.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series([True, False], dtype="boolean")

	colors = read_colors(column)

	assert colors.tolist() == ["True", "False"]


def test_read_colors_rejects_durations() -> None:
	"""
	Check that a color_by column of durations raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series(numpy.array([1], dtype="timedelta64[ns]"))

	with pytest.raises(IncompatibleTypesError):
		read_colors(column)


def test_hide_missing_points_hides_rows_missing_a_color_or_a_size() -> None:
	"""
	Check that a row missing its color or its size value draws no point.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_table_values(FLATS, "surface", ["price"], "ScatterChart")
	point_values = read_point_values(FLATS, "city", "rooms", chart_values.rows)

	shown_values = hide_missing_points(chart_values, point_values)

	shown_series = shown_values.series[0]
	hidden_values = numpy.isnan(shown_series.values)
	hidden = hidden_values.tolist()
	assert hidden == [False, True, True]
	assert shown_values.value_type == chart_values.value_type


def build_age_groups() -> ndp.Table:
	"""
	Return a Table whose age column holds categories cut by brackets.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The column age, of type CATEGORY.
	"""
	ages = ndp.Array.from_list(AGES)
	age_table = ndp.Table.from_arrays({AGE_COLUMN: ages})
	conversion = ndp.TableConversion(columns=[AGE_COLUMN], dtype=ndp.Type.CATEGORY, format=AGE_BRACKETS)
	age_groups = age_table.convert(conversion)

	return age_groups


def test_read_category_order_follows_the_categories() -> None:
	"""
	Check that the categories of a column come as texts in their order, even the one no row holds.

	.. versionadded:: 0.2.0
	"""
	age_groups = build_age_groups()
	frame = read_stored_frame(age_groups)

	category_order = read_category_order(frame[AGE_COLUMN])

	assert category_order == EXPECTED_AGE_ORDER


def test_read_category_order_gives_none_for_texts() -> None:
	"""
	Check that a column of texts has no category order.

	.. versionadded:: 0.2.0
	"""
	frame = read_stored_frame(FLATS)

	category_order = read_category_order(frame[CITY_COLUMN])

	assert category_order is None


def test_read_point_values_keeps_the_order_of_color_categories() -> None:
	"""
	Check that a color_by column of categories gives the order of its categories.

	.. versionadded:: 0.2.0
	"""
	age_groups = build_age_groups()
	row_count = len(AGES)
	rows = numpy.arange(row_count)

	point_values = read_point_values(age_groups, AGE_COLUMN, None, rows)

	assert point_values.color_order == EXPECTED_AGE_ORDER
