"""
Error raised when the values a chart shares out add up to 0.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_TOTAL_MESSAGE = "{chart_name} needs a positive total, the values of {column_name!r} add up to 0."


class EmptyTotalError(NumdaplotError):
	"""
	Raised when the values of a ``PieChart`` add up to 0, which leaves nothing to share out.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class, such as ``PieChart``.
	column_name
		The column of the values.

	Attributes
	----------
	chart_name
		Name of the chart class, such as ``PieChart``.
	column_name
		The column of the values.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> sales = ndp.Array.from_list([0.0, 0.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales")
	>>> try:
	... 	ndp.plot_pie(shares, chart)
	... except ndp.EmptyTotalError as error:
	... 	print(error)
	PieChart needs a positive total, the values of 'sales' add up to 0.
	"""

	def __init__(self, chart_name: str, column_name: str) -> None:
		"""
		Build the error message from the chart and the column.

		.. versionadded:: 0.1.0

		Parameters
		----------
		chart_name
			Name of the chart class, such as ``PieChart``.
		column_name
			The column of the values.
		"""
		message = EMPTY_TOTAL_MESSAGE.format(chart_name=chart_name, column_name=column_name)
		super().__init__(message)
		self.chart_name = chart_name
		self.column_name = column_name
