"""
Error raised when a statistic needs at least one present value and gets none.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_ARRAY_MESSAGE = "Cannot compute {statistic_name} without any present value."


class EmptyArrayError(NumdaplotError):
	"""
	Raised when a statistic that needs at least one value gets none.

	``Mean`` or ``Max`` cannot be computed on values that are all missing, or on no value at all.

	.. versionadded:: 0.1.0

	Parameters
	----------
	statistic_name
		Name of the statistic.

	Attributes
	----------
	statistic_name
		Name of the statistic.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([None, None], dtype=ndp.Type.FLOAT64)
	>>> try:
	... 	array.compute(ndp.Mean())
	... except ndp.EmptyArrayError as error:
	... 	print(error)
	Cannot compute Mean without any present value.
	"""

	def __init__(self, statistic_name: str) -> None:
		"""
		Build the error message from the statistic name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		statistic_name
			Name of the statistic.
		"""
		message = EMPTY_ARRAY_MESSAGE.format(statistic_name=statistic_name)
		super().__init__(message)

		self.statistic_name = statistic_name
