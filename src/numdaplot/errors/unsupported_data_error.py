"""
Error raised when a chart cannot draw an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNSUPPORTED_DATA_MESSAGE = "{owner_name} cannot draw {data_name}, use a Table."


class UnsupportedDataError(NumdaplotError):
	"""
	Raised when a chart or a plot function that needs the column names of a Table is given an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	owner_name
		What refuses the data, such as ``PieChart``.
	data_name
		The data refused, such as ``an Array``.

	Attributes
	----------
	owner_name
		What refuses the data, such as ``PieChart``.
	data_name
		The data refused, such as ``an Array``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sales = ndp.Array.from_list([120.0, 80.0])
	>>> chart = ndp.PieChart()
	>>> try:
	... 	ndp.plot_pie(sales, chart)
	... except ndp.UnsupportedDataError as error:
	... 	print(error)
	PieChart cannot draw an Array, use a Table.
	"""

	def __init__(self, owner_name: str, data_name: str) -> None:
		"""
		Build the error message from what refuses the data and the data.

		.. versionadded:: 0.1.0

		Parameters
		----------
		owner_name
			What refuses the data, such as ``PieChart``.
		data_name
			The data refused, such as ``an Array``.
		"""
		message = UNSUPPORTED_DATA_MESSAGE.format(owner_name=owner_name, data_name=data_name)
		super().__init__(message)
		self.owner_name = owner_name
		self.data_name = data_name
