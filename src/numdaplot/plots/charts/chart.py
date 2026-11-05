"""
Base class of every chart.

.. versionadded:: 0.1.0
"""


class Chart:
	"""
	Base class of every chart, which says what a Plot draws and how its series look.

	A chart is immutable and checks its settings when it is created.

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
	>>> chart = ndp.BarChart()
	>>> isinstance(chart, ndp.Chart)
	True
	>>> plot = ndp.plot_bar(prices, chart)
	>>> plot.show()
	"""
