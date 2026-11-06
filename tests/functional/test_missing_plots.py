"""
Functional tests of the plots of the missing values of a Table.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path
from typing import Any, cast

import numpy
import pandas
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import numdaplot as ndp

FLATS_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", None, "Pau", "Lyon"],
		"price": [12.0, None, None, 15.5],
		"rooms": [2.0, 3.0, 1.0, 4.0],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
EXPECTED_COLUMNS = ["city", "price", "rooms"]
EXPECTED_RATIOS = [0.25, 0.5, 0.0]
EXPECTED_MAP = [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
EXPECTED_MISSING_LEGEND = "Missing (3)"
LONG_TABLE_ROWS = 6000
LONG_TABLE_MISSING_STEP = 500
EXPECTED_LONG_TABLE_MISSING = 12


def test_missing_values_by_column_are_drawn_as_ratios() -> None:
	"""
	Check one bar per column, as high as its share of missing values, with ticks up to 1.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.missing_by_column(FLATS, ndp.MissingChart(measure=ndp.Measure.RATIO))

	axes = plot.to_matplotlib().axes[0]
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	# Some versions of the matplotlib stubs leave the ticks untyped.
	ticks = cast(NDArray[numpy.float64], axes.get_yticks())
	assert heights == EXPECTED_RATIOS
	assert column_labels == EXPECTED_COLUMNS
	assert float(ticks[-1]) == 1.0
	assert axes.get_ylabel() == "Missing ratio"


def test_missing_values_by_column_are_drawn_as_counts_by_default() -> None:
	"""
	Check that, without chart, the bars count the missing values and label their axis Missing count.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.missing_by_column(FLATS)

	axes = plot.to_matplotlib().axes[0]
	assert axes.get_ylabel() == "Missing count"


def test_the_missing_map_marks_each_missing_value_with_a_legend() -> None:
	"""
	Check one cell per value, the column names and a legend naming both colors.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.missing_map(FLATS)

	axes = plot.to_matplotlib().axes[0]
	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	legend = axes.get_legend()
	assert cells.tolist() == EXPECTED_MAP
	assert column_labels == EXPECTED_COLUMNS
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	assert legend_texts == [EXPECTED_MISSING_LEGEND, "Present"]


def test_the_missing_map_is_saved_as_a_pdf(tmp_path: Path) -> None:
	"""
	Check that the map is written as a PDF file.

	.. versionadded:: 0.1.0
	"""
	image_path = tmp_path / "missing.pdf"
	plot = ndp.Plot.missing_map(FLATS)

	plot.save(image_path)

	image_start = image_path.read_bytes()[:4]
	assert image_start == b"%PDF"


def test_the_missing_map_of_a_long_table_loses_no_missing_value() -> None:
	"""
	Check that each missing value spread over more rows than the image has pixels keeps its own band.

	.. versionadded:: 0.1.0
	"""
	prices = numpy.ones(LONG_TABLE_ROWS)
	prices[::LONG_TABLE_MISSING_STEP] = numpy.nan
	frame = pandas.DataFrame({"price": prices})
	table = ndp.Table.from_pandas(frame)

	axes = ndp.Plot.missing_map(table).to_matplotlib().axes[0]

	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	cell_total = cast(float, cells.sum())
	assert cells.shape[0] < LONG_TABLE_ROWS
	assert cell_total == EXPECTED_LONG_TABLE_MISSING


def test_the_missing_map_places_its_legend_past_the_axes_by_default() -> None:
	"""
	Check that the legend is anchored on the right of the axes, so it hides no cell.

	.. versionadded:: 0.1.0
	"""
	axes = ndp.Plot.missing_map(FLATS).to_matplotlib().axes[0]

	legend = axes.get_legend()
	assert legend is not None
	anchor = legend.get_bbox_to_anchor().transformed(axes.transAxes.inverted())
	assert anchor.x0 > 1.0
