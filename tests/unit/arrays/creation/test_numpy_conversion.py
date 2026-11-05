"""
Unit tests of copy_numpy_values and normalize_text.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pytest

from numdaplot.arrays.creation.numpy_conversion import copy_numpy_values, normalize_text
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError

# Some versions of the numpy stubs leave out the missing value marker of StringDType.
STRING_DTYPE_CLASS = cast(Any, numpy.dtypes.StringDType)
TEXT_DTYPE = STRING_DTYPE_CLASS(na_object=numpy.nan)
TEXT_DTYPE_MARKED_WITH_NONE = STRING_DTYPE_CLASS(na_object=None)
CHANGED_VALUE = 99
FIRST_POSITION = 0
ORIGINAL_VALUES = [1, 2]


def test_copy_numpy_values_is_independent_from_the_original() -> None:
	"""
	Check that changing the original array does not change the copy.

	.. versionadded:: 0.1.0
	"""
	original_values = numpy.array(ORIGINAL_VALUES)
	copied_values = copy_numpy_values(original_values)

	original_values[FIRST_POSITION] = CHANGED_VALUE

	copied_list = copied_values.tolist()
	assert copied_list == ORIGINAL_VALUES


def test_copy_numpy_values_rejects_python_objects() -> None:
	"""
	Check that an object array raises UnsupportedTypeError.

	.. versionadded:: 0.1.0
	"""
	object_values = numpy.array([None], dtype=object)

	with pytest.raises(UnsupportedTypeError):
		copy_numpy_values(object_values)


def test_normalize_text_stores_fixed_length_texts_as_variable_length_texts() -> None:
	"""
	Check that a fixed-length text array becomes a StringDType array.

	.. versionadded:: 0.1.0
	"""
	fixed_length_texts = numpy.array(["a", "bc"])

	normalized_values = normalize_text(fixed_length_texts)

	assert normalized_values.dtype == TEXT_DTYPE


def test_normalize_text_turns_another_missing_marker_into_nan() -> None:
	"""
	Check that a text array marking missing values with None gets the marker of a TEXT Array.

	.. versionadded:: 0.1.0
	"""
	marked_texts = numpy.array(["a", None], dtype=TEXT_DTYPE_MARKED_WITH_NONE)

	normalized_values = normalize_text(marked_texts)

	assert normalized_values.dtype == TEXT_DTYPE
	missing = numpy.isnan(normalized_values)
	assert missing.tolist() == [False, True]


def test_normalize_text_keeps_other_values_as_they_are() -> None:
	"""
	Check that numbers are returned without copy.

	.. versionadded:: 0.1.0
	"""
	numbers = numpy.array(ORIGINAL_VALUES)

	normalized_values = normalize_text(numbers)

	assert normalized_values is numbers
