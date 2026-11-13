"""
Display of an Array: its text.

.. versionadded:: 0.2.0
"""

from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.export.array_text import format_array


class ArrayDisplay(ArrayData):
	"""
	Display of an Array: its text, shown by ``print`` or at the end of a notebook cell.

	.. versionadded:: 0.2.0
	"""

	def __repr__(self) -> str:
		"""
		Return the text of the Array: its values, then its type.

		.. versionadded:: 0.1.0

		Returns
		-------
		str
			The text, such as ``Array([1, 2, 3], dtype=INT64)``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list(["a", "b"])
		Array(['a', 'b'], dtype=TEXT)
		"""
		array_text = format_array(self._values)

		return array_text
