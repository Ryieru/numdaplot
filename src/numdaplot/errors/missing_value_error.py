"""
Error raised when a chart cannot draw a missing value.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

MISSING_VALUE_MESSAGE = "{chart_name} cannot draw a missing value, found one in {column_name!r}."


class MissingValueError(NumdaplotError):
	"""
	Raised when a column drawn by a chart that needs every value, such as a ``PieChart``, has a missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class, such as ``PieChart``.
	column_name
		The column holding the missing value.

	Attributes
	----------
	chart_name
		Name of the chart class, such as ``PieChart``.
	column_name
		The column holding the missing value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> sales = ndp.Array.from_list([120.0, None])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales")
	>>> try:
	... 	ndp.plot_pie(shares, chart)
	... except ndp.MissingValueError as error:
	... 	print(error)
	PieChart cannot draw a missing value, found one in 'sales'.
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
			The column holding the missing value.
		"""
		message = MISSING_VALUE_MESSAGE.format(chart_name=chart_name, column_name=column_name)
		super().__init__(message)
		self.chart_name = chart_name
		self.column_name = column_name
