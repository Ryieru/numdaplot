"""
Error raised when an operation does not apply to the number of dimensions of an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DIMENSION_MESSAGE = "{operation} does not apply to an Array of {dimension_count} dimension(s)."


class DimensionError(NumdaplotError):
	"""
	Raised when an operation does not apply to the number of dimensions of an Array.

	For example, an axis only applies to a two-dimensional Array, and a one-dimensional Array has no columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		Description of the rejected operation.
	dimension_count
		Number of dimensions of the Array.

	Attributes
	----------
	operation
		Description of the rejected operation.
	dimension_count
		Number of dimensions of the Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2, 3])
	>>> try:
	... 	array.compute(ndp.Sum(), axis=ndp.Axis.EACH_ROW)
	... except ndp.DimensionError as error:
	... 	print(error)
	An axis does not apply to an Array of 1 dimension(s).
	"""

	def __init__(self, operation: str, dimension_count: int) -> None:
		"""
		Build the error message from the operation and the dimension count.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			Description of the rejected operation.
		dimension_count
			Number of dimensions of the Array.
		"""
		message = DIMENSION_MESSAGE.format(operation=operation, dimension_count=dimension_count)
		super().__init__(message)

		self.operation = operation
		self.dimension_count = dimension_count
