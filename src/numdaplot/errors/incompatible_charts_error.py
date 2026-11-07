"""
Error raised when a chart cannot be added to a Plot.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INCOMPATIBLE_CHARTS_MESSAGE = "A {chart_name} with {chart_positions} cannot be added to a Plot with {plot_positions}."


class IncompatibleChartsError(NumdaplotError):
	"""
	Raised when a chart added to a Plot does not have the kind of values of an axis it shares with the Plot.

	Its ``x`` values are numbers, dates, texts or times of day while the Plot has another kind, or it measures numbers
	on an axis of times of day, or the reverse.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class added, such as ``LineChart``.
	chart_positions
		What the added chart has on the shared axis: ``numbers``, ``dates``, ``texts`` or ``times of day`` as ``x``
		values, or ``numbers on the left axis`` or ``times of day on the left axis`` as values.
	plot_positions
		What the Plot has on the shared axis.

	Attributes
	----------
	chart_name
		Name of the chart class added, such as ``LineChart``.
	chart_positions
		What the added chart has on the shared axis: ``numbers``, ``dates``, ``texts`` or ``times of day`` as ``x``
		values, or ``numbers on the left axis`` or ``times of day on the left axis`` as values.
	plot_positions
		What the Plot has on the shared axis.

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
		Build the error message from the chart and what each one has on the shared axis.

		.. versionadded:: 0.1.0

		Parameters
		----------
		chart_name
			Name of the chart class added, such as ``LineChart``.
		chart_positions
			What the added chart has on the shared axis: ``numbers``, ``dates``, ``texts`` or ``times of day`` as ``x``
			values, or ``numbers on the left axis`` or ``times of day on the left axis`` as values.
		plot_positions
			What the Plot has on the shared axis.
		"""
		message = INCOMPATIBLE_CHARTS_MESSAGE.format(
			chart_name=chart_name, chart_positions=chart_positions, plot_positions=plot_positions
		)
		super().__init__(message)
		self.chart_name = chart_name
		self.chart_positions = chart_positions
		self.plot_positions = plot_positions
