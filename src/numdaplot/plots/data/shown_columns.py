"""
Columns shown by the charts of a Plot, and the checks of the names they are shown under.

.. versionadded:: 0.1.0
"""

from typing import cast

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.missing_cells import MissingCounts
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.data.sample_values import SampleValues
from numdaplot.tables.columns.renaming import Renaming


def find_shown_columns(layers: list[ChartLayer]) -> set[str]:
	"""
	Return the names of the columns shown by the charts of a Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.

	Returns
	-------
	set[str]
		The ``x`` column, the drawn columns, the group, color and size columns, or the columns of a missing value
		chart; ``"0"``, ``"1"``... for the columns of an Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.data.shown_columns import find_shown_columns
	>>> days = ndp.Array.from_list([1, 2])
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices})
	>>> layer = ChartLayer(ndp.LineChart(), read_table_values(sales, "day", ["price"], "LineChart"))
	>>> sorted(find_shown_columns([layer]))
	['day', 'price']
	"""
	shown_columns = set[str]()
	for layer in layers:
		value_columns = find_value_columns(layer.values)
		shown_columns.update(value_columns)
		if layer.points is not None:
			point_columns = find_point_columns(layer.points)
			shown_columns.update(point_columns)

	return shown_columns


def find_value_columns(values: ChartValues | SampleValues) -> list[str]:
	"""
	Return the names of the columns shown by the values of one chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a chart.

	Returns
	-------
	list[str]
		The column names, the columns of a missing value chart being its positions.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.data.sample_values import SampleValues
	>>> from numdaplot.plots.data.shown_columns import find_value_columns
	>>> prices = Series("price", numpy.array([12.0]))
	>>> find_value_columns(SampleValues([prices], None, "city", "price"))
	['price', 'city']
	"""
	if isinstance(values, MissingCounts):
		raw_columns = values.positions.values.tolist()
		missing_columns = cast(list[str], raw_columns)
		return missing_columns

	value_columns = [series.name for series in values.series]
	if isinstance(values, SampleValues):
		group_columns = optional_names(values.group_name)
		sample_columns = value_columns + group_columns
		return sample_columns

	position_columns = optional_names(values.positions.name)
	chart_columns = position_columns + value_columns

	return chart_columns


def find_point_columns(points: PointValues) -> list[str]:
	"""
	Return the names of the color and size columns of a scatter chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	points
		The colors and the sizes of the points.

	Returns
	-------
	list[str]
		The names of the columns given, empty when the points take no column.

	Examples
	--------
	>>> from numdaplot.plots.data.point_values import PointValues
	>>> from numdaplot.plots.data.shown_columns import find_point_columns
	>>> find_point_columns(PointValues("zone", None, None, None))
	['zone']
	"""
	color_columns = optional_names(points.color_name)
	size_columns = optional_names(points.size_name)
	point_columns = color_columns + size_columns

	return point_columns


def optional_names(name: str | None) -> list[str]:
	"""
	Return a name in a list, or an empty list when there is none.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		A column name, or None.

	Returns
	-------
	list[str]
		The name alone, or nothing.

	Examples
	--------
	>>> from numdaplot.plots.data.shown_columns import optional_names
	>>> optional_names("day"), optional_names(None)
	(['day'], [])
	"""
	if name is None:
		return []

	names = [name]

	return names


def require_distinct_shown_names(layers: list[ChartLayer], renaming: Renaming | None) -> None:
	"""
	Check that no column is shown under the name of another column that keeps its own name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot known so far.
	renaming
		The names under which some columns are shown, or None.

	Raises
	------
	DuplicateColumnError
		When a new name is the name of another shown column that is not renamed itself.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.data.shown_columns import require_distinct_shown_names
	>>> days = ndp.Array.from_list([1, 2])
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices})
	>>> layer = ChartLayer(ndp.LineChart(), read_table_values(sales, "day", ["price"], "LineChart"))
	>>> renaming = ndp.Renaming(changes=[ndp.NameChange(old_name="price", new_name="day")])
	>>> try:
	... 	require_distinct_shown_names([layer], renaming)
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'day' appears more than once.
	"""
	if renaming is None:
		return

	shown_columns = find_shown_columns(layers)
	renamed_columns = {change.old_name for change in renaming.changes}
	kept_columns = shown_columns - renamed_columns
	for change in renaming.changes:
		if change.new_name in kept_columns:
			raise DuplicateColumnError(change.new_name)


def require_renamed_columns_shown(layers: list[ChartLayer], renaming: Renaming | None) -> None:
	"""
	Check that every renamed column is shown by a chart of the Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		Every chart of the Plot.
	renaming
		The names under which some columns are shown, or None.

	Raises
	------
	ColumnNotFoundError
		At the first renamed column that no chart shows.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.data.shown_columns import require_renamed_columns_shown
	>>> layer = ChartLayer(ndp.LineChart(), read_array_values(ndp.Array.from_list([12.0]), "LineChart"))
	>>> renaming = ndp.Renaming(changes=[ndp.NameChange(old_name="prise", new_name="Price")])
	>>> try:
	... 	require_renamed_columns_shown([layer], renaming)
	... except ndp.ColumnNotFoundError as error:
	... 	print(error)
	No column is named 'prise'.
	"""
	if renaming is None:
		return

	shown_columns = find_shown_columns(layers)
	for change in renaming.changes:
		if change.old_name not in shown_columns:
			raise ColumnNotFoundError(change.old_name)
