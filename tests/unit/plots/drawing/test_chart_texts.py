"""
Unit tests of the choice of the title and the axis labels of a Plot.

.. versionadded:: 0.1.0
"""

import numdaplot as ndp
from numdaplot.plots.drawing.chart_texts import choose_label, choose_title, choose_title_label
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes


def test_choose_title_prefers_the_title_of_the_chart() -> None:
	"""
	Check that a chart with its own title does not get one built from its labels.

	.. versionadded:: 0.1.0
	"""
	drawn_chart = DrawnChart("day", "price", False, GridAxes.BOTH, None, title="Own title")

	title = choose_title(drawn_chart, ndp.PlotStyle())

	assert title == "Own title"


def test_choose_title_is_empty_without_labels() -> None:
	"""
	Check that a chart without labels gets no title.

	.. versionadded:: 0.1.0
	"""
	drawn_chart = DrawnChart(None, None, False, GridAxes.NONE, None)

	title = choose_title(drawn_chart, ndp.PlotStyle())

	assert title == ""


def test_choose_title_label_keeps_the_default_of_a_removed_label() -> None:
	"""
	Check that an empty label in the style gives the default name.

	.. versionadded:: 0.1.0
	"""
	label = choose_title_label("", "price")

	assert label == "price"


def test_choose_label_prefers_an_empty_style_label_to_the_default() -> None:
	"""
	Check that an empty label in the style removes the default one.

	.. versionadded:: 0.1.0
	"""
	label = choose_label("", "price")

	assert label == ""
