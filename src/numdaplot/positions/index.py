"""
A single position in one dimension.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.positions.whole_positions import require_whole_position


@dataclass(frozen=True)
class Index:
	"""
	A single position in one dimension, used by ``Region``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		The position, starting at 0. A negative position counts from the end:
		-1 is the last one.

	Raises
	------
	InvalidPositionError
		When ``position`` is not a whole number, such as ``1.5``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> scores = ndp.Array.from_list([10, 20, 30])
	>>> scores.take(ndp.Region(rows=ndp.Index(-1)))
	Array([30], dtype=INT64)
	"""

	position: int

	def __post_init__(self) -> None:
		"""
		Check that the position is a whole number.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidPositionError
			When ``position`` is not a whole number.
		"""
		require_whole_position(self.position, None)
