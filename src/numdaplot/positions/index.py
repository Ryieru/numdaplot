"""
A single position in one dimension.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types


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
	InvalidTypeError
		When a setting is not of the type its annotation names.

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
		Check the type of the position.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
