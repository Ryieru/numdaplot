"""
Error raised when two shapes do not match.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence

from numdaplot.errors.numdaplot_error import NumdaplotError

SHAPE_MISMATCH_MESSAGE = "Expected matching shapes, got {left_dimensions} and {right_dimensions}."


class ShapeMismatchError(NumdaplotError):
	"""
	Raised when two shapes do not match.

	Two Arrays cannot be combined, a replacement does not fit its region, or a reshape targets a shape
	holding another number of values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left_dimensions
		Dimensions of the first shape.
	right_dimensions
		Dimensions of the second shape.

	Attributes
	----------
	left_dimensions
		Dimensions of the first shape, as a list.
	right_dimensions
		Dimensions of the second shape, as a list.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2, 3])
	>>> try:
	... 	array.reshape(ndp.Shape([2, 2]))
	... except ndp.ShapeMismatchError as error:
	... 	print(error)
	Expected matching shapes, got [3] and [2, 2].
	"""

	def __init__(self, left_dimensions: Sequence[int], right_dimensions: Sequence[int]) -> None:
		"""
		Build the error message from the left dimensions and the right dimensions.

		.. versionadded:: 0.1.0

		Parameters
		----------
		left_dimensions
			Dimensions of the first shape.
		right_dimensions
			Dimensions of the second shape.
		"""
		left_list = list(left_dimensions)
		right_list = list(right_dimensions)
		message = SHAPE_MISMATCH_MESSAGE.format(left_dimensions=left_list, right_dimensions=right_list)
		super().__init__(message)

		self.left_dimensions = left_list
		self.right_dimensions = right_list
