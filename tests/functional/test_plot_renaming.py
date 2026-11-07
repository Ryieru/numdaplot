"""
Functional tests of the names under which a Plot shows its columns.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pytest
from matplotlib.figure import Figure

import numdaplot as ndp

MONTHS = ndp.Array.from_list(["Jan", "Feb", "Mar"])
SALES = ndp.Array.from_list([120.0, 150.0, None])
COSTS = ndp.Array.from_list([80.0, 70.0, 60.0])
UNITS = ndp.Array.from_list([1, 2, 3])
SHOP = ndp.Table.from_arrays({"month": MONTHS, "sales": SALES, "cost": COSTS, "units": UNITS})
NEW_NAMES = {"month": "Mois", "sales": "Ventes", "cost": "Couts", "units": "Unites"}
TWO_LINES = ndp.LineChart(x="month", y=["sales", "cost"])
EXPECTED_LEGEND = ["Ventes", "Couts"]
EXPECTED_MISSING_LABELS = ["Mois", "Ventes", "Couts", "Unites"]
EXPECTED_LATE_LEGEND = ["sales", "Couts"]
CHOSEN_TITLE = "Shop"
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 1.5]])
ARRAY_NAMES = ndp.Renaming(
	changes=[ndp.NameChange(old_name="0", new_name="Paris"), ndp.NameChange(old_name="1", new_name="Lyon")]
)
EXPECTED_ARRAY_LEGEND = ["Paris", "Lyon"]
SWAPPED_NAMES = ndp.Renaming(
	changes=[ndp.NameChange(old_name="sales", new_name="cost"), ndp.NameChange(old_name="cost", new_name="sales")]
)
EXPECTED_SWAPPED_LEGEND = ["cost", "sales"]
SALES_AS_COST = ndp.Renaming(changes=[ndp.NameChange(old_name="sales", new_name="cost")])
EXPECTED_DUPLICATE_MESSAGE = "The column name 'cost' appears more than once."
LATE_COLUMN = ndp.Renaming(changes=[ndp.NameChange(old_name="cost", new_name="Couts")])
MISSPELLED_COLUMN = ndp.Renaming(changes=[ndp.NameChange(old_name="cots", new_name="Couts")])
EXPECTED_NOT_FOUND_MESSAGE = "No column is named 'cots'."


def style_renaming(column_names: list[str]) -> ndp.PlotStyle:
	"""
	Return a style showing the given columns under their French names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The columns the Plot shows.

	Returns
	-------
	ndp.PlotStyle
		The style renaming exactly these columns.
	"""
	changes = [ndp.NameChange(old_name=name, new_name=NEW_NAMES[name]) for name in column_names]
	renaming = ndp.Renaming(changes=changes)
	style = ndp.PlotStyle(renaming=renaming)

	return style


def read_legend_texts(figure: Figure) -> list[str]:
	"""
	Return the texts of the legend drawn by a Plot, on its axes or past them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		The matplotlib figure of a Plot.

	Returns
	-------
	list[str]
		The texts of the legend, in order.
	"""
	legends = list(figure.legends)
	for axes in figure.axes:
		axes_legend = axes.get_legend()
		if axes_legend is not None:
			legends.append(axes_legend)

	first_legend = legends[0]
	legend_texts = [text.get_text() for text in first_legend.get_texts()]

	return legend_texts


def read_x_tick_texts(figure: Figure) -> list[str]:
	"""
	Return the labels of the horizontal axis of a Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		The matplotlib figure of a Plot.

	Returns
	-------
	list[str]
		The texts of the labels, in order.
	"""
	axes = figure.axes[0]
	tick_labels = axes.get_xticklabels()
	tick_texts = [label.get_text() for label in tick_labels]

	return tick_texts


@pytest.mark.parametrize(
	("plot", "expected"),
	[
		(
			ndp.Plot.line(SHOP, TWO_LINES, style_renaming(["month", "sales", "cost"])),
			("Ventes, Couts by Mois", "Mois", "Ventes, Couts"),
		),
		(
			ndp.Plot.scatter(SHOP, ndp.ScatterChart(x="units", y="sales"), style_renaming(["units", "sales"])),
			("Ventes by Unites", "Unites", "Ventes"),
		),
		(
			ndp.Plot.histogram(SHOP, ndp.HistogramChart(columns=["sales"]), style_renaming(["sales"])),
			("Count by Ventes", "Ventes", "Count"),
		),
		(
			ndp.Plot.box(SHOP, ndp.BoxChart(columns=["cost"], group_by="month"), style_renaming(["cost", "month"])),
			("Couts by Mois", "Mois", "Couts"),
		),
		(
			ndp.Plot.heatmap(
				SHOP, ndp.HeatmapChart(columns=["cost"], labels="month"), style_renaming(["cost", "month"])
			),
			("Mois by Column", "Column", "Mois"),
		),
	],
)
def test_the_default_title_and_labels_take_the_shown_names(plot: ndp.Plot, expected: tuple[str, str, str]) -> None:
	"""
	Check that the default title and axis labels are built from the shown names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		A Plot whose style renames its columns.
	expected
		The title, the label of the horizontal axis and the label of the vertical axis.
	"""
	figure = plot.to_matplotlib()

	axes = figure.axes[0]
	shown_texts = (axes.get_title(), axes.get_xlabel(), axes.get_ylabel())
	assert shown_texts == expected


def test_the_legend_shows_the_new_names() -> None:
	"""
	Check that each series of the legend takes its shown name.

	.. versionadded:: 0.1.0
	"""
	style = style_renaming(["month", "sales", "cost"])
	plot = ndp.Plot.line(SHOP, TWO_LINES, style)

	figure = plot.to_matplotlib()

	legend_texts = read_legend_texts(figure)
	assert legend_texts == EXPECTED_LEGEND


def test_a_given_title_keeps_its_text() -> None:
	"""
	Check that a title given in the style is not built from the shown names.

	.. versionadded:: 0.1.0
	"""
	renamed_style = style_renaming(["sales", "cost"])
	style = ndp.PlotStyle(title=CHOSEN_TITLE, renaming=renamed_style.renaming)
	plot = ndp.Plot.line(SHOP, TWO_LINES, style)

	figure = plot.to_matplotlib()

	axes = figure.axes[0]
	title = axes.get_title()
	assert title == CHOSEN_TITLE


def test_the_columns_of_an_array_can_be_named() -> None:
	"""
	Check that the series 0 and 1 of an Array take the given names.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.line(GRID, None, ndp.PlotStyle(renaming=ARRAY_NAMES))

	figure = plot.to_matplotlib()

	legend_texts = read_legend_texts(figure)
	assert legend_texts == EXPECTED_ARRAY_LEGEND


def test_the_boxes_and_the_missing_bars_show_the_new_names() -> None:
	"""
	Check the labels of the boxes and of the bars counting missing values.

	.. versionadded:: 0.1.0
	"""
	box_style = style_renaming(["sales", "cost"])
	missing_style = style_renaming(["month", "sales", "cost", "units"])
	box_plot = ndp.Plot.box(SHOP, ndp.BoxChart(columns=["sales", "cost"]), box_style)
	missing_plot = ndp.Plot.missing_by_column(SHOP, None, missing_style)

	box_figure = box_plot.to_matplotlib()
	missing_figure = missing_plot.to_matplotlib()

	box_texts = read_x_tick_texts(box_figure)
	missing_texts = read_x_tick_texts(missing_figure)
	assert box_texts == EXPECTED_LEGEND
	assert missing_texts == EXPECTED_MISSING_LABELS


def test_two_columns_can_swap_their_names() -> None:
	"""
	Check that two columns may show the name of each other.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.line(SHOP, TWO_LINES, ndp.PlotStyle(renaming=SWAPPED_NAMES))

	figure = plot.to_matplotlib()

	legend_texts = read_legend_texts(figure)
	assert legend_texts == EXPECTED_SWAPPED_LEGEND


def test_a_shown_name_of_another_column_is_refused_at_creation() -> None:
	"""
	Check that showing sales under the name of the drawn column cost raises at the creation of the Plot.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(renaming=SALES_AS_COST)

	with pytest.raises(ndp.DuplicateColumnError) as error_info:
		ndp.Plot.line(SHOP, TWO_LINES, style)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_DUPLICATE_MESSAGE


def test_a_shown_name_of_an_added_column_is_refused_when_it_is_added() -> None:
	"""
	Check that the conflict is raised by the add_* bringing the other column.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(renaming=SALES_AS_COST)
	plot = ndp.Plot.bar(SHOP, ndp.BarChart(x="month", y=["sales"]), style)

	with pytest.raises(ndp.DuplicateColumnError):
		plot.add_line(SHOP, ndp.LineChart(x="month", y=["cost"]), ndp.ValueAxis.RIGHT)


def test_a_column_brought_by_an_added_chart_can_be_renamed() -> None:
	"""
	Check that a renamed column absent from the first chart is accepted once an add_* draws it.

	.. versionadded:: 0.1.0
	"""
	style = ndp.PlotStyle(renaming=LATE_COLUMN)
	plot = ndp.Plot.bar(SHOP, ndp.BarChart(x="month", y=["sales"]), style)
	added_plot = plot.add_line(SHOP, ndp.LineChart(x="month", y=["cost"]), ndp.ValueAxis.RIGHT)

	figure = added_plot.to_matplotlib()

	legend_texts = read_legend_texts(figure)
	assert legend_texts == EXPECTED_LATE_LEGEND


def test_a_renamed_column_drawn_by_no_chart_is_refused_when_drawing(tmp_path: Path) -> None:
	"""
	Check that a misspelled column raises ColumnNotFoundError when the Plot is saved.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	plot = ndp.Plot.line(SHOP, TWO_LINES, ndp.PlotStyle(renaming=MISSPELLED_COLUMN))

	with pytest.raises(ndp.ColumnNotFoundError) as error_info:
		plot.save(tmp_path / "shop.png")

	error_text = str(error_info.value)
	assert error_text == EXPECTED_NOT_FOUND_MESSAGE
