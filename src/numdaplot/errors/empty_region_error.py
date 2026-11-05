"""
Error raised when a Region chooses neither rows nor columns.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_REGION_MESSAGE = "A Region needs rows, columns or both, got neither."


class EmptyRegionError(NumdaplotError):
	"""
	Raised when a ``Region`` is created without rows and without columns, which would choose the whole object.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Region()
	... except ndp.EmptyRegionError as error:
	... 	print(error)
	A Region needs rows, columns or both, got neither.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.1.0
		"""
		super().__init__(EMPTY_REGION_MESSAGE)
