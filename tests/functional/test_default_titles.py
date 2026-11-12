"""
Functional tests of the default titles and axis labels of the Plots.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

MONTHS = ndp.Array.from_list(["Jan", "Feb", "Mar"])
SALES = ndp.Array.from_list([120.0, 150.0, None])
COSTS = ndp.Array.from_list([80.0, 70.0, 60.0])
TAXES = ndp.Array.from_list([8.0, 7.0, 6.0])
TIPS = ndp.Array.from_list([2.0, 3.0, 1.0])
UNITS = ndp.Array.from_list([1, 2, 3])
SHOP = ndp.Table.from_arrays(
	{"month": MONTHS, "sales": SALES, "cost": COSTS, "tax": TAXES, "tip": TIPS, "units": UNITS},
)
COMPLETE_SHOP = ndp.Table.from_arrays({"month": MONTHS, "cost": COSTS})
ONE_LINE = ndp.LineChart(x="month", y=["sales"])
TWO_BARS = ndp.BarChart(x="month", y=["sales", "cost"])
FOUR_LINES = ndp.LineChart(x="month", y=["sales", "cost", "tax", "tip"])
POINTS = ndp.ScatterChart(x="units", y="sales")
GROUPED_BOXES = ndp.BoxChart(columns=["cost"], group_by="month")
HEATMAP = ndp.HeatmapChart(columns=["sales", "cost"], labels="month")
SHORTENED_NAMES = "sales, cost, tax and 1 more"
REMOVED_TEXT = ""
CHOSEN_TITLE = "Sales"
CHOSEN_X_LABEL = "Period"


@pytest.mark.parametrize(
	("plot", "expected"),
	[
		(ndp.Plot.line(SHOP, ONE_LINE), ("sales by month", "month", "sales")),
		(ndp.Plot.bar(SHOP, TWO_BARS), ("sales, cost by month", "month", "sales, cost")),
		(ndp.Plot.line(SHOP, FOUR_LINES), (f"{SHORTENED_NAMES} by month", "month", SHORTENED_NAMES)),
		(ndp.Plot.scatter(SHOP, POINTS), ("sales by units", "units", "sales")),
		(ndp.Plot.histogram(SHOP, ndp.HistogramChart(columns=["sales"])), ("Count by sales", "sales", "Count")),
		(ndp.Plot.box(SHOP, ndp.BoxChart(columns=["sales"])), ("sales by Column", "Column", "sales")),
		(ndp.Plot.box(SHOP, GROUPED_BOXES), ("cost by month", "month", "cost")),
		(ndp.Plot.heatmap(SHOP, HEATMAP), ("month by Column", "Column", "month")),
		(ndp.Plot.line(COSTS), ("Value by Row", "Row", "Value")),
		(ndp.Plot.bar(COSTS), ("Value by Row", "Row", "Value")),
		(ndp.Plot.scatter(COSTS), ("Value by Row", "Row", "Value")),
		(ndp.Plot.histogram(COSTS), ("Count by Value", "Value", "Count")),
		(ndp.Plot.box(COSTS), ("Value by Column", "Column", "Value")),
		(ndp.Plot.heatmap(COSTS), ("Row by Column", "Column", "Row")),
		(ndp.Plot.missing_by_column(SHOP), ("Missing count by Column", "Column", "Missing count")),
		(ndp.Plot.missing_map(SHOP), ("Map of missing values", "Column", "Row")),
	],
)
def test_a_plot_has_a_title_and_axis_labels_by_default(plot: ndp.Plot, expected: tuple[str, str, str]) -> None:
	"""
	Check the title and the labels of every kind of chart, written as the ``y`` label by the ``x`` label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		A Plot without style.
	expected
		The title, the label of the horizontal axis and the label of the vertical axis.
	"""
	drawn_figure = plot.to_matplotlib()
	axes = drawn_figure.axes[0]

	shown_texts = (drawn_figure.get_suptitle(), axes.get_xlabel(), axes.get_ylabel())
	assert shown_texts == expected


def test_a_pie_takes_its_title_from_its_columns() -> None:
	"""
	Check that a pie is titled after its values and its labels, and has no axis label.

	.. versionadded:: 0.1.0
	"""
	chart = ndp.PieChart(labels="month", values="cost")

	drawn_figure = ndp.Plot.pie(COMPLETE_SHOP, chart).to_matplotlib()
	axes = drawn_figure.axes[0]

	plot_title = drawn_figure.get_suptitle()
	assert plot_title == "cost by month"
	assert axes.get_xlabel() == REMOVED_TEXT


def test_an_empty_text_removes_the_default_title_and_labels() -> None:
	"""
	Check that a style with empty texts draws neither a title nor labels.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(title=REMOVED_TEXT, x_label=REMOVED_TEXT, y_label=REMOVED_TEXT)

	drawn_figure = ndp.Plot.line(SHOP, ONE_LINE, style).to_matplotlib()
	axes = drawn_figure.axes[0]

	shown_texts = (drawn_figure.get_suptitle(), axes.get_xlabel(), axes.get_ylabel())
	assert shown_texts == (REMOVED_TEXT, REMOVED_TEXT, REMOVED_TEXT)


def test_a_chosen_title_replaces_the_default_one() -> None:
	"""
	Check that the title of the style wins over the default one.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(title=CHOSEN_TITLE)

	drawn_figure = ndp.Plot.line(SHOP, ONE_LINE, style).to_matplotlib()

	plot_title = drawn_figure.get_suptitle()
	assert plot_title == CHOSEN_TITLE


def test_the_default_title_uses_a_chosen_label() -> None:
	"""
	Check that the title follows a label chosen in the style.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(x_label=CHOSEN_X_LABEL)

	drawn_figure = ndp.Plot.line(SHOP, ONE_LINE, style).to_matplotlib()

	plot_title = drawn_figure.get_suptitle()
	assert plot_title == f"sales by {CHOSEN_X_LABEL}"


def test_the_default_title_keeps_the_name_of_a_removed_label() -> None:
	"""
	Check that removing the label of an axis keeps its name in the title.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(x_label=REMOVED_TEXT)

	drawn_figure = ndp.Plot.line(SHOP, ONE_LINE, style).to_matplotlib()
	axes = drawn_figure.axes[0]

	plot_title = drawn_figure.get_suptitle()
	assert plot_title == "sales by month"
	assert axes.get_xlabel() == REMOVED_TEXT


def test_an_added_chart_keeps_the_title_of_the_first_one() -> None:
	"""
	Check that a chart added over a Plot changes neither its title nor its labels.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.bar(SHOP, ndp.BarChart(x="month", y=["sales"]))

	both = plot.add_line(SHOP, ndp.LineChart(x="month", y=["cost"]))

	drawn_figure = both.to_matplotlib()
	axes = drawn_figure.axes[0]
	plot_title = drawn_figure.get_suptitle()
	assert plot_title == "sales by month"
	assert axes.get_ylabel() == "sales"


def test_each_plot_of_a_figure_keeps_its_default_title() -> None:
	"""
	Check that the cells of a Figure show the titles of their Plots, and no title for the whole Figure.

	.. versionadded:: 0.1.0
	"""
	first_plot = ndp.Plot.line(SHOP, ONE_LINE)
	second_plot = ndp.Plot.bar(COSTS)
	layout = ndp.Layout(rows=1, columns=2)
	figure = (
		ndp.Figure(layout).place(first_plot, ndp.Cell(row=0, column=0)).place(second_plot, ndp.Cell(row=0, column=1))
	)

	matplotlib_figure = figure.to_matplotlib()

	titles = [subfigure.get_suptitle() for subfigure in matplotlib_figure.subfigs]
	assert titles == ["sales by month", "Value by Row"]
	plot_title = matplotlib_figure.get_suptitle()
	assert plot_title == REMOVED_TEXT
