"""
The first positions of one dimension.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.positions.position_count import require_position_count


@dataclass(frozen=True)
class First:
	"""
	The first positions of one dimension, used by ``Region``, such as the first 10 rows of a sorted Table.

	A dimension shorter than the count gives every position, without error.

	.. versionadded:: 0.2.0

	Parameters
	----------
	count
		The number of positions, at least 1.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidCountError
		When ``count`` is 0 or negative.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> scores = ndp.Array.from_list([40, 30, 20, 10])
	>>> scores.take(ndp.Region(rows=ndp.First(3)))
	Array([40, 30, 20], dtype=INT64)
	>>> scores.take(ndp.Region(rows=ndp.First(10)))
	Array([40, 30, 20, 10], dtype=INT64)
	"""

	count: int

	def __post_init__(self) -> None:
		"""
		Check that the count is 1 or more.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidCountError
			When ``count`` is 0 or negative.
		"""
		require_field_types(self)

		require_position_count(self.count)
