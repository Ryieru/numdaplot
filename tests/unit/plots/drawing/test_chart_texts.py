"""
Unit tests of the choice of the title and the axis labels of a Plot.

.. versionadded:: 0.1.0
"""

import numdaplot as ndp
from numdaplot.plots.drawing.chart_texts import choose_label, choose_title, choose_title_label, find_title_name
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes

VALUE_LABEL = "Value"
SERIES_NAMES = "price, cost"
POSITION_LABEL = "day"
EXPECTED_NAMED_TITLE = "price, cost by day"
CHOSEN_Y_LABEL = "Euros"
EXPECTED_CHOSEN_TITLE = "Euros by day"
HISTOGRAM_MEASURE = "Count"
EXPECTED_HISTOGRAM_TITLE = "Count by price, cost"


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


def test_choose_title_names_several_series_labeled_value() -> None:
	"""
	Check that the title names the series whose axis is labeled Value.

	.. versionadded:: 0.2.0
	"""
	drawn_chart = DrawnChart(POSITION_LABEL, VALUE_LABEL, False, GridAxes.BOTH, None, y_title_name=SERIES_NAMES)

	title = choose_title(drawn_chart, ndp.PlotStyle())

	assert title == EXPECTED_NAMED_TITLE


def test_choose_title_names_the_values_of_a_histogram_on_the_x_axis() -> None:
	"""
	Check that the title names the columns of a histogram whose axis is labeled Value.

	.. versionadded:: 0.2.0
	"""
	drawn_chart = DrawnChart(VALUE_LABEL, HISTOGRAM_MEASURE, False, GridAxes.VALUES, None, x_title_name=SERIES_NAMES)

	title = choose_title(drawn_chart, ndp.PlotStyle())

	assert title == EXPECTED_HISTOGRAM_TITLE


def test_choose_title_prefers_the_chosen_label_to_the_title_name() -> None:
	"""
	Check that a label chosen in the style also names the values in the title.

	.. versionadded:: 0.2.0
	"""
	drawn_chart = DrawnChart(POSITION_LABEL, VALUE_LABEL, False, GridAxes.BOTH, None, y_title_name=SERIES_NAMES)

	title = choose_title(drawn_chart, ndp.PlotStyle(y_label=CHOSEN_Y_LABEL))

	assert title == EXPECTED_CHOSEN_TITLE


def test_find_title_name_falls_back_to_the_axis_label() -> None:
	"""
	Check that an axis without title name is named by its label.

	.. versionadded:: 0.2.0
	"""
	title_name = find_title_name(None, VALUE_LABEL)

	assert title_name == VALUE_LABEL
