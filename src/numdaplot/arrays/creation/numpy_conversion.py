"""
Conversion of numpy arrays to the values stored by an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.data_types.type import Type

FIXED_LENGTH_TEXT_KIND = "U"


def copy_numpy_values(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return a copy of a numpy array that an Array can store.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A numpy array of a type numdaplot supports.

	Returns
	-------
	NDArray
		An independent copy, with fixed-length texts stored as variable-length texts.

	Raises
	------
	UnsupportedTypeError
		When numdaplot has no equivalent type, for example complex numbers or Python objects.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.numpy_conversion import copy_numpy_values
	>>> copy_numpy_values(numpy.array(["a", "bc"])).dtype
	StringDType()
	"""
	from_numpy_dtype(values.dtype)
	copied_values = values.copy()
	normalized_values = normalize_text(copied_values)

	return normalized_values


def normalize_text(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return values whose fixed-length texts are stored as variable-length texts, as every ``TEXT`` Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A numpy array of any type.

	Returns
	-------
	NDArray
		The same array when it holds no fixed-length text, otherwise a converted copy.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.numpy_conversion import normalize_text
	>>> normalize_text(numpy.array(["a"])).dtype
	StringDType()
	"""
	if values.dtype.kind != FIXED_LENGTH_TEXT_KIND:
		return values

	text_dtype = to_numpy_dtype(Type.TEXT)
	text_values = values.astype(text_dtype)

	return text_values
