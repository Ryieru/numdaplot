"""
Base class of every chart.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_operation_error import RefusedOperationError

CONSTRUCTOR_OPERATION = "Creating a Chart with ndp.Chart()"
CONSTRUCTOR_ALTERNATIVE = "a chart such as ndp.LineChart"


class Chart:
	"""
	Base class of every chart, which says what a Plot draws and how its series look.

	A chart is immutable and checks its settings when it is created.

	Only its subclasses are created: calling ``ndp.Chart()`` raises ``RefusedOperationError``.

	Every chart, each passed to its own plot function:

	|Chart|What it draws|Example|
	|---|---|---|
	|``LineChart``|Each series as a line, with ``plot_line``|``ndp.LineChart(x="month", y=["sales"])``|
	|``BarChart``|Each value as a bar, with ``plot_bar``|``ndp.BarChart(x="city", y=["sales"])``|
	|``ScatterChart``|Each row as a point, with ``plot_scatter``|``ndp.ScatterChart(x="price", y="stock")``|
	|``HistogramChart``|The values per bin, with ``plot_histogram``|``ndp.HistogramChart(columns=["price"])``|
	|``BoxChart``|The spread of each column as a box, with ``plot_box``|``ndp.BoxChart(columns=["price"])``|
	|``PieChart``|Each row as a slice of a pie, with ``plot_pie``|``ndp.PieChart(labels="city", values="sales")``|
	|``HeatmapChart``|Each value as a colored cell, with ``plot_heatmap``|``ndp.HeatmapChart()``|
	|``MissingChart``|The missing values per column, with ``plot_missing_by_column``|``ndp.MissingChart()``|

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> bar_plot = ndp.plot_bar(prices, ndp.BarChart(orientation=ndp.Orientation.HORIZONTAL))
	>>> bar_plot.show()
	>>> line_plot = ndp.plot_line(prices, ndp.LineChart(marker=ndp.MarkerShape.CIRCLE))
	>>> line_plot.show()
	"""

	def __init__(self) -> None:
		"""
		Refuse the creation of the base class itself, and let a subclass be created.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			When the created object is a Chart and not one of its subclasses.
		"""
		created_class = type(self)
		if created_class is Chart:
			raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)
