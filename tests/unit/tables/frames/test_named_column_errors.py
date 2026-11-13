"""
Unit tests of the name of a Table column in the errors about its values raised by a block.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.errors.settings.unmatched_value_error import UnmatchedValueError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.types.out_of_domain_error import OutOfDomainError
from numdaplot.errors.types.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors

COLUMN_NAME = "price"
NAMED_COLUMN = pandas.Series([1.0], name=COLUMN_NAME)
UNNAMED_COLUMN = pandas.Series([1.0])
OTHER_COLUMN = pandas.Series([1.0], name="fare")
OPERATION = "Contains"
TYPE_NAMES = ["FLOAT64"]
NAMED_MESSAGE = "Cannot apply Contains to the FLOAT64 column 'price'."
UNNAMED_MESSAGE = "Cannot apply Contains to FLOAT64."
FUNCTION_NAME = "SquareRoot"
NEGATIVE_VALUE = -1.0


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

	assert error_info.value.column_name == COLUMN_NAME


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

	assert error_info.value.column_name == COLUMN_NAME


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


def test_named_column_errors_names_the_column_of_a_domain_error() -> None:
	"""
	Check that a value outside the domain of a function gets the column.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(OutOfDomainError) as error_info, NamedColumnErrors(NAMED_COLUMN):
		raise OutOfDomainError(FUNCTION_NAME, NEGATIVE_VALUE)

	assert error_info.value.column_name == COLUMN_NAME


def test_named_column_errors_names_the_column_of_an_unmatched_value() -> None:
	"""
	Check that a value without new value gets the column.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(UnmatchedValueError) as error_info, NamedColumnErrors(NAMED_COLUMN):
		raise UnmatchedValueError(NEGATIVE_VALUE)

	assert error_info.value.column_name == COLUMN_NAME
