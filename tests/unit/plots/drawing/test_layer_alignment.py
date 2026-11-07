"""
Unit tests of the alignment of the charts of a Plot on shared labels.

.. versionadded:: 0.1.0
"""

from typing import cast

import numpy
import pandas
import pytest

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.point_values import PointValues, read_point_values
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.layer_alignment import (
	align_layer,
	align_layers,
	align_points,
	merge_labels,
	needs_shared_labels,
	pick_values,
	write_layer_labels,
)

SALES = ndp.Table.from_arrays(
	{"city": ndp.Array.from_list(["Paris", "Lyon"]), "sales": ndp.Array.from_list([120.0, 80.0])}
)
TARGETS = ndp.Table.from_arrays(
	{
		"city": ndp.Array.from_list(["Pau", "Paris"]),
		"target": ndp.Array.from_list([40.0, 130.0]),
		"rooms": ndp.Array.from_list([2.0, 3.0]),
	}
)
CITY_BARS = ChartLayer(ndp.BarChart(), read_table_values(SALES, "city", ["sales"], "BarChart"))
TARGET_VALUES = read_table_values(TARGETS, "city", ["target"], "LineChart")
TARGET_LINE = ChartLayer(ndp.LineChart(), TARGET_VALUES)
PRICES = ndp.Array.from_list([12.0, 15.5])
NUMBER_LINE = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
NUMBER_BARS = ChartLayer(ndp.BarChart(), read_array_values(PRICES, "BarChart"))
REPEATED_FRAME = pandas.DataFrame({"city": ["Paris", "Paris"], "sales": [1.0, 2.0]})
REPEATED_SALES = ndp.Table.from_pandas(REPEATED_FRAME)
REPEATED_BARS = ChartLayer(ndp.BarChart(), read_table_values(REPEATED_SALES, "city", ["sales"], "BarChart"))
EXPECTED_LABELS = ["Paris", "Lyon", "Pau"]
SOURCES = numpy.array([1, -1, 0])


def read_series_values(layer: ChartLayer) -> list[float]:
	"""
	Return the values of the first series of a chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer
		A chart and its values.

	Returns
	-------
	list[float]
		The values, NaN where missing.
	"""
	values = layer.values
	assert isinstance(values, ChartValues)
	# Some versions of the numpy stubs widen the list of a one-dimensional array.
	series_values = cast(list[float], values.series[0].values.tolist())

	return series_values


def test_align_layers_places_every_chart_on_the_merged_labels() -> None:
	"""
	Check that both charts share the labels and each value is on its label.

	.. versionadded:: 0.1.0
	"""
	bars, line = align_layers([CITY_BARS, TARGET_LINE])

	bar_values = read_series_values(bars)
	line_values = read_series_values(line)
	assert isinstance(line.values, ChartValues)
	assert line.values.positions.values.tolist() == EXPECTED_LABELS
	assert line.values.positions.kind == PositionKind.TEXTS
	assert numpy.isnan(bar_values[2])
	assert line_values[0] == 130.0
	assert numpy.isnan(line_values[1])


def test_align_layers_keeps_a_single_chart() -> None:
	"""
	Check that a Plot of one chart is left as it is, even with repeated labels.

	.. versionadded:: 0.1.0
	"""
	layers = [REPEATED_BARS]

	aligned_layers = align_layers(layers)

	assert aligned_layers is layers


def test_align_layers_keeps_number_lines_on_their_scale() -> None:
	"""
	Check that overlaid lines of numbers keep their number positions.

	.. versionadded:: 0.1.0
	"""
	layers = [NUMBER_LINE, NUMBER_LINE]

	aligned_layers = align_layers(layers)

	assert aligned_layers is layers


def test_align_layers_rejects_a_repeated_label() -> None:
	"""
	Check that a label repeated in one overlaid chart raises DuplicateLabelError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.DuplicateLabelError):
		align_layers([REPEATED_BARS, TARGET_LINE])


def test_needs_shared_labels_for_a_line_over_number_bars() -> None:
	"""
	Check that bars place even numbers on labels.

	.. versionadded:: 0.1.0
	"""
	shares_labels = needs_shared_labels([NUMBER_BARS, NUMBER_LINE])

	assert shares_labels


def test_write_layer_labels_writes_numbers_as_texts() -> None:
	"""
	Check that numbers become their text.

	.. versionadded:: 0.1.0
	"""
	labels = write_layer_labels(NUMBER_BARS)

	assert labels == ["0", "1"]


def test_merge_labels_keeps_the_first_order_then_the_new_labels() -> None:
	"""
	Check the order of the merged labels.

	.. versionadded:: 0.1.0
	"""
	merged_labels = merge_labels([["Paris", "Lyon"], ["Pau", "Paris"], ["Lyon"]])

	assert merged_labels == EXPECTED_LABELS


def test_align_layer_reorders_the_values_on_the_merged_labels() -> None:
	"""
	Check that each value moves to its label, NaN where the chart has none.

	.. versionadded:: 0.1.0
	"""
	aligned_layer = align_layer(TARGET_LINE, ["Pau", "Paris"], EXPECTED_LABELS)

	line_values = read_series_values(aligned_layer)
	assert line_values[0] == 130.0
	assert numpy.isnan(line_values[1])
	assert line_values[2] == 40.0


def test_align_points_reorders_the_values_of_the_points() -> None:
	"""
	Check that the sizes of the points follow their labels.

	.. versionadded:: 0.1.0
	"""
	points = read_point_values(TARGETS, None, "rooms", TARGET_VALUES.rows)

	aligned_points = align_points(points, SOURCES)

	assert aligned_points is not None
	assert aligned_points.sizes is not None
	sizes = cast(list[float], aligned_points.sizes.tolist())
	assert sizes[0] == 3.0
	assert numpy.isnan(sizes[1])


def test_align_points_keeps_none_without_points() -> None:
	"""
	Check that a chart without points stays without them.

	.. versionadded:: 0.1.0
	"""
	aligned_points = align_points(None, SOURCES)

	assert aligned_points is None


def test_align_points_keeps_missing_columns_missing() -> None:
	"""
	Check that a chart without color_by keeps no colors.

	.. versionadded:: 0.1.0
	"""
	points = PointValues(None, None, None, None)

	aligned_points = align_points(points, SOURCES)

	assert aligned_points is not None
	assert aligned_points.colors is None


def test_pick_values_fills_numbers_with_nan() -> None:
	"""
	Check that a missing number is NaN.

	.. versionadded:: 0.1.0
	"""
	picked_values = pick_values(numpy.array([1.0, 2.0]), SOURCES)

	assert picked_values[0] == 2.0
	assert numpy.isnan(picked_values[1])


def test_pick_values_fills_texts_with_none() -> None:
	"""
	Check that a missing text is None.

	.. versionadded:: 0.1.0
	"""
	texts = numpy.array(["Paris", "Lyon"], dtype=object)

	picked_values = pick_values(texts, SOURCES)

	assert picked_values.tolist() == ["Lyon", None, "Paris"]


def test_align_layer_keeps_the_type_of_the_values() -> None:
	"""
	Check that the aligned values keep the type of the values of the chart.

	.. versionadded:: 0.1.0
	"""
	aligned_layer = align_layer(TARGET_LINE, ["Pau", "Paris"], EXPECTED_LABELS)

	aligned_values = cast(ChartValues, aligned_layer.values)
	assert aligned_values.value_type == TARGET_VALUES.value_type
