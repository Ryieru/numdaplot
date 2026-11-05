"""
Number of values along each dimension of an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_shape_error import InvalidShapeError
from numdaplot.settings.setting_types import require_setting_type

LOWEST_DIMENSION = 0
DIMENSIONS_SETTING = "Shape dimensions"
DIMENSIONS_EXPECTED = "a list such as [3, 4]"
DIMENSIONS_TYPES = (list,)


@dataclass(frozen=True)
class Shape:
	"""
	Number of values along each dimension of an Array.

	``Shape([3, 4])`` describes 3 rows of 4 values, and ``Shape([5])`` a single row of 5 values.
	It is used by ``Array.filled``, ``Array.random`` and ``reshape``, and returned by ``Array.shape``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dimensions
		Number of values along each dimension, a list of at least one dimension and none lower than 0.
		The shape keeps its own copy of the list.

	Raises
	------
	InvalidSettingTypeError
		When ``dimensions`` is not a list, such as ``(3, 4)`` or ``3``.
	InvalidShapeError
		When ``dimensions`` is empty or holds a negative number.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.filled(shape=ndp.Shape([2, 3]), value=0)
	Array([[0, 0, 0],
	       [0, 0, 0]], dtype=INT64)
	>>> ndp.Array.from_list([[1, 2, 3], [4, 5, 6]]).shape
	Shape(dimensions=[2, 3])
	"""

	dimensions: list[int]

	def __post_init__(self) -> None:
		"""
		Check the dimensions and replace them with a copy that only the shape holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When ``dimensions`` is not a list.
		InvalidShapeError
			When ``dimensions`` is empty or holds a negative number.
		"""
		require_setting_type(DIMENSIONS_SETTING, DIMENSIONS_EXPECTED, self.dimensions, DIMENSIONS_TYPES)

		dimension_count = len(self.dimensions)
		if dimension_count == 0:
			raise InvalidShapeError(self.dimensions)

		for dimension in self.dimensions:
			if dimension < LOWEST_DIMENSION:
				raise InvalidShapeError(self.dimensions)

		dimensions_copy = list(self.dimensions)
		object.__setattr__(self, "dimensions", dimensions_copy)
