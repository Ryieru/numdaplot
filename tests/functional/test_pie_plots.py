"""
Functional tests of the pie plots of Tables.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path

import pytest
from matplotlib.patches import Wedge

import numdaplot as ndp

DEVICES = ndp.Array.from_list(["Phone", "Computer", "Tablet"])
VISITS = ndp.Array.from_list([5000.0, 4000.0, 1000.0])
TRAFFIC = ndp.Table.from_arrays({"device": DEVICES, "visits": VISITS})
CHART = ndp.PieChart(labels="device", values="visits")
EXPECTED_TEXTS = ["Phone", "Computer", "Tablet", "50.0%", "40.0%", "10.0%"]
EXPECTED_ANGLES = [180.0, 144.0, 36.0]
FRUITS = ndp.Array.from_list(["apple", "pear", "plum", "fig", "kiwi", "lime"])
FRUIT_SALES = ndp.Array.from_list([30.0, 25.0, 15.0, 12.0, 10.0, 8.0])
FRUIT_SHARES = ndp.Table.from_arrays({"fruit": FRUITS, "sales": FRUIT_SALES})
NEGATIVE_VISITS = ndp.Array.from_list([5000.0, -10.0, 1000.0])
NEGATIVE_TRAFFIC = ndp.Table.from_arrays({"device": DEVICES, "visits": NEGATIVE_VISITS})


def test_a_pie_plot_shares_out_the_values_with_their_labels_and_percentages() -> None:
	"""
	Check one slice per row sized by its share, its label and its percentage, and the title.

	.. versionadded:: 0.1.0
	"""
	style = ndp.Style(title="Visits per device")

	plot = ndp.plot_pie(TRAFFIC, CHART, style)

	axes = plot.to_matplotlib().axes[0]
	slices = [patch for patch in axes.patches if isinstance(patch, Wedge)]
	angles = [slice_.theta2 - slice_.theta1 for slice_ in slices]
	texts = [text.get_text() for text in axes.texts]
	assert angles == pytest.approx(EXPECTED_ANGLES)
	assert texts == EXPECTED_TEXTS
	assert axes.get_title() == "Visits per device"
	assert axes.get_legend() is None


def test_a_pie_plot_of_many_slices_suggests_a_bar_plot() -> None:
	"""
	Check that 6 slices are drawn after a ReadabilityWarning.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="fruit", values="sales")

	with pytest.warns(ndp.ReadabilityWarning, match="6 slices"):
		plot = ndp.plot_pie(FRUIT_SHARES, chart)

	axes = plot.to_matplotlib().axes[0]
	slices = [patch for patch in axes.patches if isinstance(patch, Wedge)]
	assert len(slices) == 6


def test_a_pie_plot_rejects_a_negative_value() -> None:
	"""
	Check that a negative value raises OutOfDomainError, caught as a NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.NumdaplotError, match="-10.0"):
		ndp.plot_pie(NEGATIVE_TRAFFIC, CHART)


def test_a_pie_plot_is_saved_as_an_svg_image(tmp_path: Path) -> None:
	"""
	Check that a pie plot is written as an SVG file.

	.. versionadded:: 0.1.0
	"""
	image_path = tmp_path / "traffic.svg"
	plot = ndp.plot_pie(TRAFFIC, CHART)

	plot.save(image_path)

	image_start = image_path.read_bytes()[:5]
	assert image_start == b"<?xml"
