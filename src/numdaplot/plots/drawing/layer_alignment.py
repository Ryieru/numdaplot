"""
Alignment of the charts of a Plot on shared ``x`` labels.

When bars or texts are overlaid, each ``x`` value is a label at its own position. The charts then share the
labels of all of them: the labels of the first chart in its order, followed by the new labels of the next ones,
and each value is placed on its label.

.. versionadded:: 0.1.0
"""

from dataclasses import replace
from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.data.unique_labels import require_unique_labels
from numdaplot.plots.drawing.axes.position_axis import write_position_labels
from numdaplot.plots.layers.chart_layer import ChartLayer

MINIMUM_SHARING_LAYERS = 2
NO_SOURCE = -1
TEXT_DTYPE = numpy.dtype(object)


def align_layers(layers: list[ChartLayer]) -> list[ChartLayer]:
	"""
	Return the charts of a Plot placed on the same labels, when several of them share label positions.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.

	Returns
	-------
	list[ChartLayer]
		The same charts, on the merged labels when bars or texts are overlaid, unchanged otherwise.

	Raises
	------
	DuplicateLabelError
		When a label appears twice in the ``x`` values of one overlaid chart.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.drawing.layer_alignment import align_layers
	>>> sales = ndp.Table.from_arrays(
	... 	{"city": ndp.Array.from_list(["Paris", "Lyon"]), "sales": ndp.Array.from_list([120.0, 80.0])}
	... )
	>>> targets = ndp.Table.from_arrays(
	... 	{"city": ndp.Array.from_list(["Pau", "Paris"]), "target": ndp.Array.from_list([40.0, 130.0])}
	... )
	>>> bars = ChartLayer(ndp.BarChart(), read_table_values(sales, "city", ["sales"], "BarChart"))
	>>> line = ChartLayer(ndp.LineChart(), read_table_values(targets, "city", ["target"], "LineChart"))
	>>> aligned_line = align_layers([bars, line])[1]
	>>> aligned_line.values.positions.values.tolist(), aligned_line.values.series[0].values.tolist()
	(['Paris', 'Lyon', 'Pau'], [130.0, nan, 40.0])
	"""
	shares_labels = needs_shared_labels(layers)
	if not shares_labels:
		return layers

	layer_labels = [write_layer_labels(layer) for layer in layers]
	merged_labels = merge_labels(layer_labels)
	label_pairs = zip(layers, layer_labels, strict=True)
	aligned_layers = [align_layer(layer, labels, merged_labels) for layer, labels in label_pairs]

	return aligned_layers


def needs_shared_labels(layers: list[ChartLayer]) -> bool:
	"""
	Return whether the charts of a Plot place their ``x`` values on shared labels.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.

	Returns
	-------
	bool
		True when several charts are overlaid and one of them draws bars or has texts as ``x`` values.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.layer_alignment import needs_shared_labels
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> line = ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))
	>>> needs_shared_labels([line, line])
	False
	"""
	layer_count = len(layers)
	if layer_count < MINIMUM_SHARING_LAYERS:
		return False

	for layer in layers:
		values = cast(ChartValues, layer.values)
		draws_bars = isinstance(layer.chart, BarChart)
		has_texts = values.positions.kind == PositionKind.TEXTS
		places_labels = draws_bars or has_texts
		if places_labels:
			return True

	return False


def write_layer_labels(layer: ChartLayer) -> list[str]:
	"""
	Return the label of each ``x`` value of a chart, after checking that none appears twice.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer
		A chart and its values.

	Returns
	-------
	list[str]
		The labels, such as ``"2026-01-01"`` for a date.

	Raises
	------
	DuplicateLabelError
		When a label appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.layer_alignment import write_layer_labels
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> write_layer_labels(ChartLayer(ndp.BarChart(), read_array_values(prices, "BarChart")))
	['0', '1']
	"""
	values = cast(ChartValues, layer.values)
	labels = write_position_labels(values.positions)
	require_unique_labels(labels)

	return labels


def merge_labels(layer_labels: list[list[str]]) -> list[str]:
	"""
	Return every label once: the labels of the first chart in its order, then the new labels of the next ones.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer_labels
		The labels of each chart.

	Returns
	-------
	list[str]
		The merged labels.

	Examples
	--------
	>>> from numdaplot.plots.drawing.layer_alignment import merge_labels
	>>> merge_labels([["Paris", "Lyon"], ["Pau", "Paris"]])
	['Paris', 'Lyon', 'Pau']
	"""
	merged_labels = dict[str, None]()

	for labels in layer_labels:
		new_labels = dict.fromkeys(labels)
		merged_labels.update(new_labels)

	label_list = list(merged_labels)

	return label_list


def align_layer(layer: ChartLayer, labels: list[str], merged_labels: list[str]) -> ChartLayer:
	"""
	Return a chart with its values placed on the merged labels, missing where it has no value for a label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer
		A chart and its values.
	labels
		The label of each of its ``x`` values.
	merged_labels
		The labels shared by every chart of the Plot.

	Returns
	-------
	ChartLayer
		The chart with text positions, its series and its point values reordered on the merged labels.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.layer_alignment import align_layer
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> layer = ChartLayer(ndp.BarChart(), read_array_values(prices, "BarChart"))
	>>> align_layer(layer, ["0", "1"], ["1", "2", "0"]).values.series[0].values
	array([15.5,  nan, 12. ])
	"""
	values = cast(ChartValues, layer.values)
	label_rows = {label: i for i, label in enumerate(labels)}
	source_rows = [label_rows.get(label, NO_SOURCE) for label in merged_labels]
	sources = numpy.array(source_rows, dtype=numpy.intp)
	merged_values = numpy.array(merged_labels, dtype=TEXT_DTYPE)
	positions = Positions(PositionKind.TEXTS, merged_values, values.positions.name)
	series = [Series(one_series.name, pick_values(one_series.values, sources)) for one_series in values.series]
	label_count = len(merged_labels)
	rows = numpy.arange(label_count)
	aligned_values = ChartValues(positions, series, rows, values.value_name, values.value_type)
	aligned_points = align_points(layer.points, sources)
	aligned_layer = replace(layer, values=aligned_values, points=aligned_points)

	return aligned_layer


def align_points(points: PointValues | None, sources: NDArray[numpy.intp]) -> PointValues | None:
	"""
	Return the values coloring and sizing the points of a ScatterChart, reordered on the merged labels.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Keeps the order of the ``color_by`` categories.

	Parameters
	----------
	points
		The values of the points, or None for a chart without them.
	sources
		For each merged label, the row of the chart holding its value, or -1 when the chart has none.

	Returns
	-------
	PointValues or None
		The reordered values, or None.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.point_values import PointValues
	>>> from numdaplot.plots.drawing.layer_alignment import align_points
	>>> points = PointValues(None, None, "surface", numpy.array([30.0, 45.0]))
	>>> align_points(points, numpy.array([1, -1])).sizes
	array([45., nan])
	"""
	if points is None:
		return None

	colors = None
	if points.colors is not None:
		colors = pick_values(points.colors, sources)

	sizes = None
	if points.sizes is not None:
		sizes = pick_values(points.sizes, sources)

	aligned_points = PointValues(points.color_name, colors, points.size_name, sizes, points.color_order)

	return aligned_points


def pick_values(values: NDArray[Any], sources: NDArray[numpy.intp]) -> NDArray[Any]:
	"""
	Return the values at given rows, missing where the row is -1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Numbers, NaN for a missing one, or texts, None for a missing one.
	sources
		The row of each value picked, or -1 for a missing value.

	Returns
	-------
	NDArray
		The picked values, of the same type: NaN or None where the row is -1.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.layer_alignment import pick_values
	>>> pick_values(numpy.array(["Paris", "Lyon"], dtype=object), numpy.array([1, -1, 0]))
	array(['Lyon', None, 'Paris'], dtype=object)
	"""
	missing_value = None
	if values.dtype != TEXT_DTYPE:
		missing_value = numpy.nan

	value_count = len(sources)
	picked_values = numpy.full(value_count, missing_value, dtype=values.dtype)
	has_source = sources != NO_SOURCE
	present_sources = sources[has_source]
	picked_values[has_source] = values[present_sources]

	return picked_values
