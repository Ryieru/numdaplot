"""
Error raised when a rotation is outside the accepted angles.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_ROTATION_MESSAGE = "Expected a rotation from -90 to 90 degrees, got {rotation}."


class InvalidRotationError(NumdaplotError):
	"""
	Raised when the ``x_tick_rotation`` or the ``y_tick_rotation`` of a ``PlotStyle`` is outside -90 to 90 degrees.

	Beyond these angles, the labels would be written upside down.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rotation
		The rotation given.

	Attributes
	----------
	rotation
		The rotation given.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.PlotStyle(x_tick_rotation=120)
	... except ndp.InvalidRotationError as error:
	... 	print(error)
	Expected a rotation from -90 to 90 degrees, got 120.
	"""

	def __init__(self, rotation: float) -> None:
		"""
		Build the error message from the rotation.

		.. versionadded:: 0.1.0

		Parameters
		----------
		rotation
			The rotation given.
		"""
		message = INVALID_ROTATION_MESSAGE.format(rotation=rotation)
		super().__init__(message)
		self.rotation = rotation
