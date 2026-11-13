"""
Charts of a Plot with their columns shown under new names.

.. versionadded:: 0.1.0
"""

import dataclasses
from typing import cast

import numpy

from numdaplot.plots.data.chart_values import ChartValues, Series
from numdaplot.plots.data.missing_cells import MissingCounts
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.data.sample_values import SampleValues
from numdaplot.plots.data.table_values import name_columns
from numdaplot.plots.layers.chart_layer import ChartLayer
from numdaplot.tables.columns.renaming import Renaming


def rename_layers(layers: list[ChartLayer], renaming: Renaming | None) -> list[ChartLayer]:
	"""
	Return the charts of a Plot with their columns shown under their new names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		Every chart of the Plot.
	renaming
		The names under which some columns are shown, or None to keep every name.

	Returns
	-------
	list[ChartLayer]
		New charts whose names, and the default labels built from them, are the shown names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.data.renamed_layers import rename_layers
	>>> grid = ndp.Array.from_list([[12.0, 8.0]])
	>>> layer = ChartLayer(ndp.LineChart(), read_array_values(grid, "LineChart"))
	>>> renaming = ndp.Renaming(changes=[ndp.NameChange(old_name="0", new_name="Paris")])
	>>> [series.name for series in rename_layers([layer], renaming)[0].values.series]
	['Paris', '1']
	"""
	if renaming is None:
		return layers

	new_names = {change.old_name: change.new_name for change in renaming.changes}
	renamed_layers = list[ChartLayer]()
	for layer in layers:
		renamed_layer = rename_layer(layer, new_names)
		renamed_layers.append(renamed_layer)

	return renamed_layers


def rename_layer(layer: ChartLayer, new_names: dict[str, str]) -> ChartLayer:
	"""
	Return one chart with its columns shown under their new names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer
		A chart and its values.
	new_names
		The new name of each renamed column.

	Returns
	-------
	ChartLayer
		A new chart, with renamed values and points.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.data.renamed_layers import rename_layer
	>>> layer = ChartLayer(ndp.LineChart(), read_array_values(ndp.Array.from_list([12.0]), "LineChart"))
	>>> rename_layer(layer, {"0": "Paris"}).values.series[0].name
	'Paris'
	"""
	renamed_values = rename_values(layer.values, new_names)
	renamed_points = layer.points
	if layer.points is not None:
		renamed_points = rename_points(layer.points, new_names)

	renamed_layer = dataclasses.replace(layer, values=renamed_values, points=renamed_points)

	return renamed_layer


def rename_values(values: ChartValues | SampleValues, new_names: dict[str, str]) -> ChartValues | SampleValues:
	"""
	Return the values of one chart with their columns shown under their new names.

	The label of the axis of the values follows when it names the drawn columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a chart.
	new_names
		The new name of each renamed column.

	Returns
	-------
	ChartValues or SampleValues
		New values of the same kind.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.data.renamed_layers import rename_values
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> sales = ndp.Table.from_arrays({"price": prices})
	>>> rename_values(read_table_values(sales, None, ["price"], "LineChart"), {"price": "Price"}).value_name
	'Price'
	"""
	if isinstance(values, MissingCounts):
		renamed_counts = rename_missing_counts(values, new_names)
		return renamed_counts

	renamed_series = rename_series(values.series, new_names)
	renamed_value_name = rename_value_name(values, renamed_series)
	if isinstance(values, SampleValues):
		renamed_group_name = rename_optional(values.group_name, new_names)
		renamed_samples = dataclasses.replace(
			values, series=renamed_series, group_name=renamed_group_name, value_name=renamed_value_name
		)
		return renamed_samples

	renamed_position_name = rename_optional(values.positions.name, new_names)
	renamed_positions = dataclasses.replace(values.positions, name=renamed_position_name)
	renamed_chart_values = dataclasses.replace(
		values, positions=renamed_positions, series=renamed_series, value_name=renamed_value_name
	)

	return renamed_chart_values


def rename_missing_counts(counts: MissingCounts, new_names: dict[str, str]) -> MissingCounts:
	"""
	Return the counts of a missing value chart with its columns shown under their new names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	counts
		The counts, one position per column of the Table.
	new_names
		The new name of each renamed column.

	Returns
	-------
	MissingCounts
		New counts whose positions are the shown names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.missing_cells import read_missing_counts
	>>> from numdaplot.plots.data.renamed_layers import rename_missing_counts
	>>> flats = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.0, None])})
	>>> counts = read_missing_counts(flats, ndp.Measure.COUNT)
	>>> rename_missing_counts(counts, {"price": "Price"}).positions.values.tolist()
	['Price']
	"""
	raw_columns = counts.positions.values.tolist()
	column_names = cast(list[str], raw_columns)
	shown_names = list[str]()
	for column_name in column_names:
		shown_name = new_names.get(column_name, column_name)
		shown_names.append(shown_name)

	position_dtype = counts.positions.values.dtype
	shown_values = numpy.array(shown_names, dtype=position_dtype)
	renamed_positions = dataclasses.replace(counts.positions, values=shown_values)
	renamed_counts = dataclasses.replace(counts, positions=renamed_positions)

	return renamed_counts


def rename_series(series: list[Series], new_names: dict[str, str]) -> list[Series]:
	"""
	Return series named after the shown names of their columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	series
		The series of a chart.
	new_names
		The new name of each renamed column.

	Returns
	-------
	list[Series]
		New series with the same numbers.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.data.renamed_layers import rename_series
	>>> rename_series([Series("price", numpy.array([12.0]))], {"price": "Price"})[0].name
	'Price'
	"""
	renamed_series = list[Series]()
	for one_series in series:
		shown_name = new_names.get(one_series.name, one_series.name)
		shown_series = dataclasses.replace(one_series, name=shown_name)
		renamed_series.append(shown_series)

	return renamed_series


def rename_value_name(values: ChartValues | SampleValues, renamed_series: list[Series]) -> str | None:
	"""
	Return the label of the axis of the values, following the series when it names them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a chart, with their series under their column names.
	renamed_series
		The same series under their shown names.

	Returns
	-------
	str or None
		The names of the renamed series when the label names the series, the label unchanged otherwise, such as
		``"value"`` for an Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.data.renamed_layers import rename_series, rename_value_name
	>>> prices = ndp.Array.from_list([12.0])
	>>> costs = ndp.Array.from_list([8.0])
	>>> sales = ndp.Table.from_arrays({"price": prices, "cost": costs})
	>>> values = read_table_values(sales, None, ["price", "cost"], "LineChart")
	>>> rename_value_name(values, rename_series(values.series, {"cost": "Cost"}))
	'price, Cost'
	"""
	if values.value_name is None:
		return None

	column_names = [one_series.name for one_series in values.series]
	shown_names = [one_series.name for one_series in renamed_series]
	if column_names == []:
		return values.value_name

	column_label = name_columns(column_names)
	if values.value_name != column_label:
		return values.value_name

	shown_label = name_columns(shown_names)

	return shown_label


def rename_points(points: PointValues, new_names: dict[str, str]) -> PointValues:
	"""
	Return the colors and the sizes of points with their columns shown under their new names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	points
		The colors and the sizes of a scatter chart.
	new_names
		The new name of each renamed column.

	Returns
	-------
	PointValues
		New points with the same colors and sizes.

	Examples
	--------
	>>> from numdaplot.plots.data.point_values import PointValues
	>>> from numdaplot.plots.data.renamed_layers import rename_points
	>>> rename_points(PointValues("zone", None, None, None), {"zone": "Zone"}).color_name
	'Zone'
	"""
	color_name = rename_optional(points.color_name, new_names)
	size_name = rename_optional(points.size_name, new_names)
	renamed_points = dataclasses.replace(points, color_name=color_name, size_name=size_name)

	return renamed_points


def rename_optional(name: str | None, new_names: dict[str, str]) -> str | None:
	"""
	Return the shown name of a column, when there is a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		A column name, or None.
	new_names
		The new name of each renamed column.

	Returns
	-------
	str or None
		The new name, the name itself when it is not renamed, or None.

	Examples
	--------
	>>> from numdaplot.plots.data.renamed_layers import rename_optional
	>>> rename_optional("day", {"day": "Day"}), rename_optional("hour", {"day": "Day"}), rename_optional(None, {})
	('Day', 'hour', None)
	"""
	if name is None:
		return None

	shown_name = new_names.get(name, name)

	return shown_name
