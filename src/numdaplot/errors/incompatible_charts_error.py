"""
Error raised when a chart cannot be added to a Plot.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INCOMPATIBLE_CHARTS_MESSAGE = "A {chart_name} with {chart_positions} cannot be added to a Plot with {plot_positions}."


class IncompatibleChartsError(NumdaplotError):
	"""
	Raised when a chart added to a Plot places its ``x`` values on another kind of axis: numbers, dates or texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class added, such as ``LineChart``.
	chart_positions
		What the added chart has as ``x`` values: ``numbers``, ``dates`` or ``texts``.
	plot_positions
		What the Plot has as ``x`` values.

	Attributes
	----------
	chart_name
		Name of the chart class added, such as ``LineChart``.
	chart_positions
		What the added chart has as ``x`` values: ``numbers``, ``dates`` or ``texts``.
	plot_positions
		What the Plot has as ``x`` values.

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> days = ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 2)])
	>>> sales = ndp.Array.from_list([120.0, 80.0])
	>>> shops = ndp.Table.from_arrays({"city": cities, "day": days, "sales": sales})
	>>> plot = ndp.Plot.bar(shops, ndp.BarChart(x="city", y=["sales"]))
	>>> line = ndp.LineChart(x="day", y=["sales"])
	>>> try:
	... 	plot.add_line(shops, line)
	... except ndp.IncompatibleChartsError as error:
	... 	print(error)
	A LineChart with dates cannot be added to a Plot with texts.
	"""

	def __init__(self, chart_name: str, chart_positions: str, plot_positions: str) -> None:
		"""
		Build the error message from the chart and the two kinds of ``x`` values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		chart_name
			Name of the chart class added, such as ``LineChart``.
		chart_positions
			What the added chart has as ``x`` values: ``numbers``, ``dates`` or ``texts``.
		plot_positions
			What the Plot has as ``x`` values.
		"""
		message = INCOMPATIBLE_CHARTS_MESSAGE.format(
			chart_name=chart_name, chart_positions=chart_positions, plot_positions=plot_positions
		)
		super().__init__(message)
		self.chart_name = chart_name
		self.chart_positions = chart_positions
		self.plot_positions = plot_positions
