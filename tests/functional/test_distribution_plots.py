"""
Functional tests of the histograms and box plots of Tables and Arrays.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path

import pandas
import pytest
from matplotlib.patches import PathPatch, Rectangle

import numdaplot as ndp

PRICES_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", "Lyon", "Paris", "Lyon", None, "Pau"],
		"2025": [12.0, 9.5, 14.0, 10.0, 30.0, 7.0],
		"2026": [13.0, 10.5, None, 11.0, 31.0, 8.0],
	}
)
PRICES = ndp.Table.from_pandas(PRICES_FRAME)
YEARS = ["2025", "2026"]
STYLE = ndp.PlotStyle(title="Prices", x_label="Euros")
EXPECTED_YEAR_COUNTS = [1.0, 3.0, 0.0, 0.0, 0.0, 1.0]
EXPECTED_GROUPS = ["Lyon", "Paris", "Pau"]
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])


def test_a_histogram_counts_the_values_of_each_bin_of_the_given_width() -> None:
	"""
	Check bins on multiples of the width, the missing value left out, and the style.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HistogramChart(columns=["2026"], bins=ndp.BinWidth(5.0))

	plot = ndp.Plot.histogram(PRICES, chart, STYLE)

	axes = plot.to_matplotlib().axes[0]
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]
	first_edge = float(bars[0].get_x())
	assert heights == EXPECTED_YEAR_COUNTS
	assert first_edge == 5.0
	assert axes.get_title() == "Prices"
	assert axes.get_xlabel() == "Euros"
	assert axes.get_ylabel() == "Count"


def test_a_histogram_of_ratios_adds_up_to_one_per_column() -> None:
	"""
	Check that the bins of each column share out 1, both columns sharing the same bins.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.HistogramChart(columns=YEARS, bins=ndp.BinCount(4), measure=ndp.Measure.RATIO)

	plot = ndp.Plot.histogram(PRICES, chart)

	axes = plot.to_matplotlib().axes[0]
	bars = [patch for patch in axes.patches if isinstance(patch, Rectangle)]
	heights = [float(bar.get_height()) for bar in bars]
	first_column_total = sum(heights[:4])
	second_column_total = sum(heights[4:])
	_, legend_labels = axes.get_legend_handles_labels()
	assert first_column_total == pytest.approx(1.0)
	assert second_column_total == pytest.approx(1.0)
	assert legend_labels == YEARS


def test_a_box_plot_draws_the_years_side_by_side_in_each_city() -> None:
	"""
	Check one position per city in alphabetical order, one box per year, and a legend of the years.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BoxChart(columns=YEARS, group_by="city")

	plot = ndp.Plot.box(PRICES, chart)

	figure = plot.to_matplotlib()
	axes = figure.axes[0]
	boxes = [patch for patch in axes.patches if isinstance(patch, PathPatch)]
	city_labels = [label.get_text() for label in axes.get_xticklabels()]
	legend = axes.get_legend()
	assert len(boxes) == 6
	assert city_labels == EXPECTED_GROUPS
	assert axes.get_xlabel() == "city"
	assert legend is not None


def test_a_box_plot_of_an_array_draws_a_box_per_column_without_legend() -> None:
	"""
	Check that each column of an Array is a box at its number, with no legend.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.box(GRID, ndp.BoxChart())

	axes = plot.to_matplotlib().axes[0]
	column_labels = [label.get_text() for label in axes.get_xticklabels()]
	assert column_labels == ["0", "1"]
	assert axes.get_legend() is None


def test_a_box_plot_is_saved_as_an_image(tmp_path: Path) -> None:
	"""
	Check that a box plot is written as a PNG file.

	.. versionadded:: 0.1.0
	"""
	image_path = tmp_path / "prices.png"
	plot = ndp.Plot.box(PRICES, ndp.BoxChart(columns=YEARS))

	plot.save(image_path)

	image_start = image_path.read_bytes()[:4]
	assert image_start == b"\x89PNG"


def test_a_box_plot_rejects_groups_of_numbers() -> None:
	"""
	Check that a group_by holding numbers raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.BoxChart(columns=["2025"], group_by="2026")

	with pytest.raises(ndp.IncompatibleTypesError):
		ndp.Plot.box(PRICES, chart)
