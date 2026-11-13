"""
Values coloring and sizing the points of a ScatterChart.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass, replace
from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.argument_checks.column_names import require_known_columns
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import find_column_type
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.charts.color_scale import ColorScale
from numdaplot.plots.data.chart_values import ChartValues, Series
from numdaplot.plots.data.column_reading import read_numbers, read_texts, require_column_family
from numdaplot.tables.table import Table
from numdaplot.tables.table_data import read_stored_frame
from numdaplot.types.type import Type
from numdaplot.types.value_family import ValueFamily

CHART_NAME = "ScatterChart"
NUMBER_COLORS_DTYPE = numpy.dtype(numpy.float64)
SCALE_ON_TEXTS = "scale without a color_by column of numbers"
COLOR_FAMILIES = frozenset({ValueFamily.NUMBER, ValueFamily.TEXT, ValueFamily.BOOL, ValueFamily.TIME})


@dataclass(frozen=True, eq=False)
class PointValues:
	"""
	The values coloring and sizing each point of a ScatterChart, one per drawn row.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Keeps the order of the categories of a ``color_by`` column of categories.

	Parameters
	----------
	color_name
		The ``color_by`` column, or None.
	colors
		Its values: float64 numbers or texts, or None.
	size_name
		The ``size_by`` column, or None.
	sizes
		Its float64 numbers, or None.
	color_order
		The texts of the categories of a ``color_by`` column of categories, in their order, None for any other
		column, whose texts are sorted when drawn.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.point_values import PointValues
	>>> PointValues("city", numpy.array(["Paris"], dtype=object), None, None).color_name
	'city'
	"""

	color_name: str | None
	colors: NDArray[Any] | None
	size_name: str | None
	sizes: NDArray[numpy.float64] | None
	color_order: list[str] | None = None


def read_point_values(
	table: Table, color_name: str | None, size_name: str | None, rows: NDArray[numpy.intp]
) -> PointValues:
	"""
	Return the values of the ``color_by`` and ``size_by`` columns of a ScatterChart for the drawn rows.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Reads the order of the categories of a ``color_by`` column of categories.

	Parameters
	----------
	table
		The Table drawn.
	color_name
		The ``color_by`` column, or None.
	size_name
		The ``size_by`` column, or None.
	rows
		The row numbers drawn.

	Returns
	-------
	PointValues
		The values of each column given, in the order of the drawn rows, and the order of the ``color_by``
		categories.

	Raises
	------
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``color_by`` holds neither numbers nor texts, or ``size_by`` does not hold numbers.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.point_values import read_point_values
	>>> surfaces = ndp.Array.from_list([30.0, 45.0])
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "city": cities})
	>>> read_point_values(flats, "city", "surface", numpy.arange(2)).sizes
	array([30., 45.])
	"""
	frame = read_stored_frame(table)
	column_names = frame.columns.tolist()
	colors = None
	sizes = None
	color_order = None
	if color_name is not None:
		require_known_columns([color_name], column_names)
		color_column = frame[color_name]
		all_colors = read_colors(color_column)
		colors = all_colors[rows]
		color_order = read_category_order(color_column)

	if size_name is not None:
		require_known_columns([size_name], column_names)
		all_sizes = read_numbers(frame[size_name], CHART_NAME)
		sizes = all_sizes[rows]

	point_values = PointValues(color_name, colors, size_name, sizes, color_order)

	return point_values


def require_scale_on_numbers(scale: ColorScale | None, colors: NDArray[Any] | None) -> None:
	"""
	Check that a color scale colors numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	scale
		The ``scale`` of a ScatterChart, or None.
	colors
		The values of its ``color_by`` column, float64 numbers or texts.

	Raises
	------
	RefusedSettingError
		When a scale is given for texts or booleans, which take one color per value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.point_values import require_scale_on_numbers
	>>> require_scale_on_numbers(ndp.ColorScale.BLUES, numpy.array([1.5]))
	>>> try:
	... 	require_scale_on_numbers(ndp.ColorScale.BLUES, numpy.array(["Paris"], dtype=object))
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	ScatterChart does not accept scale without a color_by column of numbers.
	"""
	if scale is None or colors is None:
		return

	if colors.dtype != NUMBER_COLORS_DTYPE:
		raise RefusedSettingError(SCALE_ON_TEXTS, CHART_NAME)


def read_colors(column: Column) -> NDArray[Any]:
	"""
	Return the values of a ``color_by`` column: float64 numbers or texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	NDArray
		Numbers with NaN, or texts with None, where a value is missing.

	Raises
	------
	IncompatibleTypesError
		When the column holds neither numbers, texts, booleans nor times of day.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.point_values import read_colors
	>>> read_colors(pandas.Series([2.5, None], dtype="float64"))
	array([2.5, nan])
	"""
	family = require_column_family(column, COLOR_FAMILIES, CHART_NAME)
	if family == ValueFamily.NUMBER:
		numbers = read_numbers(column, CHART_NAME)
		return numbers

	texts = read_texts(column, CHART_NAME)

	return texts


def read_category_order(column: Column) -> list[str] | None:
	"""
	Return the texts of the categories of a column of categories, in their order.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	list[str] or None
		The categories written as the texts of the column, None for a column of another type.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.point_values import read_category_order
	>>> from numdaplot.tables.table_data import read_stored_frame
	>>> ages = ndp.Table.from_arrays({"age": ndp.Array.from_list([25, 5])})
	>>> brackets = ndp.Brackets(limits=[0, 10, 100])
	>>> age_groups = ages.convert(ndp.TableConversion(columns=["age"], dtype=ndp.Type.CATEGORY, format=brackets))
	>>> read_category_order(read_stored_frame(age_groups)["age"])
	['0 to 9', '10 to 99']
	"""
	column_type = find_column_type(column)
	if column_type != Type.CATEGORY:
		return None

	categories = column.cat.categories
	raw_category_column = pandas.Series(categories)
	category_column = raw_category_column.astype(column.dtype)
	category_texts = read_texts(category_column, CHART_NAME)
	category_order = cast(list[str], category_texts.tolist())

	return category_order


def hide_missing_points(chart_values: ChartValues, point_values: PointValues) -> ChartValues:
	"""
	Return the values of a ScatterChart without the points whose color or size value is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_values
		The positions and the series.
	point_values
		The values coloring and sizing the points.

	Returns
	-------
	ChartValues
		The same values, NaN in the series where a color or size value is missing.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
	>>> from numdaplot.plots.data.point_values import PointValues, hide_missing_points
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> positions = Positions(PositionKind.NUMBERS, numpy.array([0.0, 1.0]), None)
	>>> price_series = Series("price", numpy.array([1.0, 2.0]))
	>>> chart_values = ChartValues(positions, [price_series], numpy.arange(2), "price", ndp.Type.FLOAT64)
	>>> point_values = PointValues(None, None, "surface", numpy.array([30.0, numpy.nan]))
	>>> hide_missing_points(chart_values, point_values).series[0].values
	array([ 1., nan])
	"""
	row_count = len(chart_values.rows)
	missing = numpy.zeros(row_count, dtype=numpy.bool_)

	for point_column in (point_values.colors, point_values.sizes):
		if point_column is None:
			continue

		missing_values = pandas.isna(point_column)
		missing = missing | missing_values

	shown_series = list[Series]()

	for series in chart_values.series:
		shown_numbers = numpy.where(missing, numpy.nan, series.values)
		series_copy = Series(series.name, shown_numbers)
		shown_series.append(series_copy)

	shown_values = replace(chart_values, series=shown_series)

	return shown_values
