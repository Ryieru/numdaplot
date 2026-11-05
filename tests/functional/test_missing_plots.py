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


def test_missing_values_by_column_are_drawn_as_ratios() -> None:
	"""
	Check one bar per column, as high as its share of missing values, on an axis from 0 to 1.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_missing_by_column(FLATS, ndp.MissingChart(measure=ndp.Measure.RATIO))

	axes = plot.to_matplotlib().axes[0]
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	limits = [float(limit) for limit in axes.get_ylim()]
	assert heights == EXPECTED_RATIOS
	assert column_labels == EXPECTED_COLUMNS
	assert limits == [0.0, 1.0]
	assert axes.get_ylabel() == "Missing ratio"


def test_missing_values_by_column_are_drawn_as_counts_by_default() -> None:
	"""
	Check that, without chart, the bars count the missing values and label their axis Missing count.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_missing_by_column(FLATS)

	axes = plot.to_matplotlib().axes[0]
	assert axes.get_ylabel() == "Missing count"


def test_the_missing_map_marks_each_missing_value_with_a_legend() -> None:
	"""
	Check one cell per value, the column names and a legend naming both colors.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.plot_missing_map(FLATS)

	axes = plot.to_matplotlib().axes[0]
	# Some versions of the matplotlib stubs leave the cells of an image untyped.
	cells = cast(numpy.ma.MaskedArray[Any, Any], axes.images[0].get_array())
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	legend = axes.get_legend()
	assert cells.tolist() == EXPECTED_MAP
	assert column_labels == EXPECTED_COLUMNS
	assert legend is not None
	legend_texts = [text.get_text() for text in legend.get_texts()]
	assert legend_texts == ["Missing", "Present"]


def test_the_missing_map_is_saved_as_a_pdf(tmp_path: Path) -> None:
	"""
	Check that the map is written as a PDF file.

	.. versionadded:: 0.1.0
	"""
	image_path = tmp_path / "missing.pdf"
	plot = ndp.plot_missing_map(FLATS)

	plot.save(image_path)

	image_start = image_path.read_bytes()[:4]
	assert image_start == b"%PDF"
