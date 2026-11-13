"""
Error raised when an image resolution is lower than 1 dot per inch.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_RESOLUTION_MESSAGE = "Expected a resolution of at least 1 dot per inch, got {dpi}."


class InvalidResolutionError(NumdaplotError):
	"""
	Raised when the ``dpi`` of ``ImageOptions`` is lower than 1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dpi
		The rejected number of dots per inch.

	Attributes
	----------
	dpi
		The rejected number of dots per inch.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ImageOptions(dpi=0)
	... except ndp.InvalidResolutionError as error:
	... 	print(error)
	Expected a resolution of at least 1 dot per inch, got 0.
	"""

	def __init__(self, dpi: int) -> None:
		"""
		Build the error message from the rejected resolution.

		.. versionadded:: 0.1.0

		Parameters
		----------
		dpi
			The rejected number of dots per inch.
		"""
		message = INVALID_RESOLUTION_MESSAGE.format(dpi=dpi)
		super().__init__(message)
		self.dpi = dpi
