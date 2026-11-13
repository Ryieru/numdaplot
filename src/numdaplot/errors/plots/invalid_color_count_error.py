"""
Error raised when a chart does not have one color per series.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_COLOR_COUNT_MESSAGE = "Expected one color per series, {series_count} series and {color_count} color(s) given."


class InvalidColorCountError(NumdaplotError):
	"""
	Raised when the colors of a chart are not exactly one per series.

	.. versionadded:: 0.1.0

	Parameters
	----------
	color_count
		The number of colors given.
	series_count
		The number of series drawn.

	Attributes
	----------
	color_count
		The number of colors given.
	series_count
		The number of series drawn.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2])
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> costs = ndp.Array.from_list([8.0, 9.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"], colors=[ndp.Color.BLUE])
	>>> try:
	... 	ndp.Plot.line(sales, chart)
	... except ndp.InvalidColorCountError as error:
	... 	print(error)
	Expected one color per series, 2 series and 1 color(s) given.
	"""

	def __init__(self, color_count: int, series_count: int) -> None:
		"""
		Build the error message from the two counts.

		.. versionadded:: 0.1.0

		Parameters
		----------
		color_count
			The number of colors given.
		series_count
			The number of series drawn.
		"""
		message = INVALID_COLOR_COUNT_MESSAGE.format(color_count=color_count, series_count=series_count)
		super().__init__(message)
		self.color_count = color_count
		self.series_count = series_count
