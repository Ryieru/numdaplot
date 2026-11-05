"""
Unit tests of the name of a Table column in the type errors of a block.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors

NAMED_COLUMN = pandas.Series([1.0], name="price")
UNNAMED_COLUMN = pandas.Series([1.0])
OTHER_COLUMN = pandas.Series([1.0], name="fare")
OPERATION = "Contains"
TYPE_NAMES = ["FLOAT64"]
NAMED_MESSAGE = "Cannot apply Contains to the FLOAT64 column 'price'."
UNNAMED_MESSAGE = "Cannot apply Contains to FLOAT64."


def test_named_column_errors_names_the_column_of_a_type_error() -> None:
	"""
	Check that a type error gets the column.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError) as error_info, NamedColumnErrors(NAMED_COLUMN):
		raise IncompatibleTypesError(OPERATION, TYPE_NAMES)

	assert str(error_info.value) == NAMED_MESSAGE


def test_named_column_errors_names_the_column_of_a_conversion_error() -> None:
	"""
	Check that a conversion error gets the column.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as error_info, NamedColumnErrors(NAMED_COLUMN):
		raise ValueConversionError("TEXT", "FLOAT64", "abc")

	assert error_info.value.column_name == "price"


def test_named_column_errors_leaves_the_error_of_a_column_without_name() -> None:
	"""
	Check that a column without name changes nothing.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError) as error_info, NamedColumnErrors(UNNAMED_COLUMN):
		raise IncompatibleTypesError(OPERATION, TYPE_NAMES)

	assert str(error_info.value) == UNNAMED_MESSAGE


def test_named_column_errors_keeps_the_first_column_named() -> None:
	"""
	Check that nested blocks keep the column closest to the error.

	.. versionadded:: 0.1.0
	"""
	with (
		pytest.raises(IncompatibleTypesError) as error_info,
		NamedColumnErrors(OTHER_COLUMN),
		NamedColumnErrors(NAMED_COLUMN),
	):
		raise IncompatibleTypesError(OPERATION, TYPE_NAMES)

	assert error_info.value.column_name == "price"


def test_named_column_errors_leaves_other_errors() -> None:
	"""
	Check that any other error goes through unchanged.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueError), NamedColumnErrors(NAMED_COLUMN):
		raise ValueError(OPERATION)


def test_named_column_errors_does_nothing_without_error() -> None:
	"""
	Check that a block without error is not disturbed.

	.. versionadded:: 0.1.0
	"""
	with NamedColumnErrors(NAMED_COLUMN):
		result = 1

	assert result == 1
