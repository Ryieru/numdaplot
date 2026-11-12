"""
Error raised when an Aggregation computes nothing.

.. versionadded:: 0.2.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_AGGREGATION_MESSAGE = "An Aggregation needs calculations, a row_count or both, got neither."


class EmptyAggregationError(NumdaplotError):
	"""
	Raised when an ``Aggregation`` has no calculation and no ``row_count``, so it would compute nothing.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Aggregation(group_by=["city"])
	... except ndp.EmptyAggregationError as error:
	... 	print(error)
	An Aggregation needs calculations, a row_count or both, got neither.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.2.0
		"""
		super().__init__(EMPTY_AGGREGATION_MESSAGE)
