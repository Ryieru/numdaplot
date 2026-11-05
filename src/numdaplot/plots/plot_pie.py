"""
Pie plots of a Table.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.chart_requirement import require_chart_class
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.data.pie_values import read_pie_values
from numdaplot.plots.drawing.series_colors import require_color_count
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table

CHART_NAME = "PieChart"
X_LABEL_SETTING = "x_label"
Y_LABEL_SETTING = "y_label"
RIGHT_LABEL_SETTING = "right_label"
X_TICK_ROTATION_SETTING = "x_tick_rotation"
Y_TICK_ROTATION_SETTING = "y_tick_rotation"
FUNCTION_NAME = "plot_pie"


def plot_pie(data: Table, chart: PieChart, style: Style | None = None) -> Plot:
	"""
	Return a Plot sharing out the values of a column of a Table as slices of a disc.

	``PieChart.labels`` names the column of texts labeling the slices and ``PieChart.values`` the column of numbers
	sizing them. A Plot of a pie has no axes, so its style takes no axis label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table drawn.
	chart
		The labels, the values, the percentages and the colors.
	style
		The look of the Plot, the default ``Style`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	UnsupportedDataError
		When the data is an Array.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``labels`` does not hold texts, or ``values`` does not hold numbers.
	MissingValueError
		When a label or a value is missing.
	OutOfDomainError
		When a value is negative.
	EmptyTotalError
		When the values add up to 0.
	DuplicateLabelError
		When two slices have the same label.
	InvalidColorCountError
		When the colors of the chart are not one per slice.
	RefusedSettingError
		When the style has an axis setting: ``x_label``, ``y_label``, ``right_label``, ``x_tick_rotation`` or
		``y_tick_rotation``.

	Warns
	-----
	ReadabilityWarning
		When there are more than 5 slices.
	RefusedOperationError
		When ``chart`` is not a ``PieChart``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> devices = ndp.Array.from_list(["Phone", "Computer", "Tablet"])
	>>> visits = ndp.Array.from_list([5400.0, 3100.0, 900.0])
	>>> traffic = ndp.Table.from_arrays({"device": devices, "visits": visits})
	>>> chart = ndp.PieChart(labels="device", values="visits")
	>>> style = ndp.Style(title="Visits per device")
	>>> plot = ndp.plot_pie(traffic, chart, style)
	>>> plot.show()
	"""
	require_chart_class(chart, PieChart, FUNCTION_NAME)
	values = read_pie_values(data, chart)
	slice_count = len(values.rows)
	require_color_count(chart.colors, slice_count)
	require_no_axis_settings(style)
	layer = ChartLayer(chart, values)
	plot = create_plot(layer, style)

	return plot


def require_no_axis_settings(style: Style | None) -> None:
	"""
	Check that the style of a pie has no axis setting, a pie having no axes.

	The grid lines and the legend keep their default values, so a pie leaves them without effect.

	.. versionadded:: 0.1.0

	Parameters
	----------
	style
		The style given, or None.

	Raises
	------
	RefusedSettingError
		When the style has an ``x_label``, a ``y_label``, a ``right_label``, an ``x_tick_rotation`` or a
		``y_tick_rotation``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.plot_pie import require_no_axis_settings
	>>> try:
	... 	require_no_axis_settings(ndp.Style(x_tick_rotation=45))
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	PieChart does not accept x_tick_rotation.
	"""
	if style is None:
		return

	axis_settings = [
		(X_LABEL_SETTING, style.x_label),
		(Y_LABEL_SETTING, style.y_label),
		(RIGHT_LABEL_SETTING, style.right_label),
		(X_TICK_ROTATION_SETTING, style.x_tick_rotation),
		(Y_TICK_ROTATION_SETTING, style.y_tick_rotation),
	]

	for setting_name, setting_value in axis_settings:
		if setting_value is not None:
			raise RefusedSettingError(setting_name, CHART_NAME)
