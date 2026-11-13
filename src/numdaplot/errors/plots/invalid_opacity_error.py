"""
Error raised when an opacity is outside what can be drawn.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_OPACITY_MESSAGE = "Expected an opacity above 0 and up to 1, got {opacity}."


class InvalidOpacityError(NumdaplotError):
	"""
	Raised when an opacity is 0 or lower, which would draw nothing, greater than 1, or not a number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	opacity
		The rejected opacity.

	Attributes
	----------
	opacity
		The rejected opacity.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ScatterChart(opacity=0.0)
	... except ndp.InvalidOpacityError as error:
	... 	print(error)
	Expected an opacity above 0 and up to 1, got 0.0.
	"""

	def __init__(self, opacity: float) -> None:
		"""
		Build the error message from the opacity.

		.. versionadded:: 0.1.0

		Parameters
		----------
		opacity
			The rejected opacity.
		"""
		message = INVALID_OPACITY_MESSAGE.format(opacity=opacity)
		super().__init__(message)

		self.opacity = opacity
