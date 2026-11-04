"""
Unit tests of the drawing of the missing values of a Table.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Any, cast

import numpy
import pandas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.data.missing_cells import read_missing_cells, read_missing_counts
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.missing_drawing import (
	MISSING_LABEL,
	PRESENT_LABEL,
	add_legend_swatch,
	draw_missing_chart,
	draw_missing_map,
)

FLATS_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", None, "Pau"],
		"price": [12.0, None, None],
		"rooms": [2.0, 3.0, 1.0],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
EXPECTED_COLUMNS = ["city", "price", "rooms"]
EXPECTED_COUNTS = [1.0, 2.0, 0.0]
EXPECTED_MAP = [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
SWATCH_COLOR = "#33415c"


def draw_counts(measure: ndp.Measure) -> Figure:
	"""
	Return a figure with the missing values of each column of the flats drawn as bars.

	.. versionadded:: 0.1.0

	Parameters
	----------
	measure
		Counts or ratios.

	Returns
	-------
	Figure
		The figure drawn.
	"""
	figure = Figure()
	axes = figure.add_subplot()
	chart = ndp.MissingChart(measure=measure)
	values = read_missing_counts(FLATS, measure)
	draw_missing_chart(axes, ChartLayer(chart, values))

	return figure


def test_draw_missing_chart_draws_one_bar_per_column() -> None:
	"""
	Check that each column gets a bar labeled with its name, even without missing value.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.COUNT)

	axes = figure.axes[0]
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert heights == EXPECTED_COUNTS
	assert column_labels == EXPECTED_COLUMNS


def test_draw_missing_chart_places_ratios_between_zero_and_one() -> None:
	"""
	Check that ratios get an axis from 0 to 1.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.RATIO)

	limits = list(figure.axes[0].get_ylim())
	assert limits == [0.0, 1.0]


def test_draw_missing_chart_places_counts_on_whole_ticks() -> None:
	"""
	Check that every tick of the counts is a whole number.

	.. versionadded:: 0.1.0
	"""
	figure = draw_counts(ndp.Measure.COUNT)

	# Some versions of the matplotlib stubs leave the ticks untyped.
	ticks = cast(NDArray[numpy.float64], figure.axes[0].get_yticks())
	whole_ticks = [float(tick).is_integer() for tick in ticks]
	assert all(whole_ticks)


def test_draw_missing_map_draws_a_cell_per_value() -> None:
	"""
	Check that each value is a cell, 1 where missing, without grid lines.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	drawn_chart = draw_missing_map(axes, ChartLayer(MissingMapChart(), read_missing_cells(FLATS)))

	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert cells.tolist() == EXPECTED_MAP
	assert column_labels == EXPECTED_COLUMNS
	assert drawn_chart.y_label == "Row"
	assert drawn_chart.grid_axes == GridAxes.NONE


def test_draw_missing_map_names_both_colors_in_the_legend() -> None:
	"""
	Check that the legend names the missing and the present color.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	draw_missing_map(axes, ChartLayer(MissingMapChart(), read_missing_cells(FLATS)))

	_, legend_labels = axes.get_legend_handles_labels()
	assert legend_labels == [MISSING_LABEL, PRESENT_LABEL]


def test_add_legend_swatch_draws_nothing_visible() -> None:
	"""
	Check that the swatch has no size, so it draws nothing on the axes.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	add_legend_swatch(axes, SWATCH_COLOR, MISSING_LABEL)

	swatch = axes.patches[0]
	assert isinstance(swatch, Rectangle)
	assert swatch.get_width() == 0
	assert swatch.get_height() == 0
