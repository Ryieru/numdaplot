"""
Unit tests of the check of every value of a Table against a rule.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.column_storage.column_values import find_column_type
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_missing import IsMissing
from numdaplot.tables.filtering.checked_frame import check_frame
from numdaplot.types.type import Type

FRAME = pandas.DataFrame(
	{
		"city": pandas.Series(["Paris", None, "Pau"], dtype="string"),
		"price": [120.0, None, 90.0],
	}
)
NUMBER_FRAME = pandas.DataFrame({"price": [120.0, None, 90.0]})
EMPTY_FRAME = pandas.DataFrame({"price": pandas.Series(dtype="float64")})
PRICE_LIMIT = 100
EXPECTED_MISSING = {"city": [False, True, False], "price": [False, True, False]}
EXPECTED_ABOVE_LIMIT = {"price": [True, False, False]}
EXPECTED_EMPTY_NAMES = ["price"]
EXPECTED_TYPES = [Type.BOOL, Type.BOOL]


def read_checks(frame: pandas.DataFrame) -> dict[str, list[bool]]:
	"""
	Return the values of every column of a checked Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The checked columns.

	Returns
	-------
	dict[str, list[bool]]
		The values of each column, by name.
	"""
	checks = dict[str, list[bool]]()

	for column_name in frame.columns:
		column = frame[column_name]
		checked_name = str(column_name)
		checks[checked_name] = column.tolist()

	return checks


def test_check_frame_marks_the_missing_values_of_every_column() -> None:
	"""
	Check IsMissing on a text and a decimal column.

	.. versionadded:: 0.1.0
	"""
	checked = check_frame(FRAME, IsMissing())

	checks = read_checks(checked)
	assert checks == EXPECTED_MISSING


def test_check_frame_gives_false_for_a_missing_value_with_another_rule() -> None:
	"""
	Check that a missing value does not satisfy a comparison.

	.. versionadded:: 0.1.0
	"""
	checked = check_frame(NUMBER_FRAME, Greater(PRICE_LIMIT))

	checks = read_checks(checked)
	assert checks == EXPECTED_ABOVE_LIMIT


def test_check_frame_stores_booleans() -> None:
	"""
	Check that every checked column is of type BOOL.

	.. versionadded:: 0.1.0
	"""
	checked = check_frame(FRAME, IsMissing())

	column_types = [find_column_type(checked[column_name]) for column_name in checked.columns]
	assert column_types == EXPECTED_TYPES


def test_check_frame_rejects_a_rule_that_does_not_apply_to_a_column() -> None:
	"""
	Check that a comparison with a number on a text column raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		check_frame(FRAME, Greater(PRICE_LIMIT))


def test_check_frame_keeps_the_columns_of_a_table_without_rows() -> None:
	"""
	Check that an empty Table gives an empty check with the same columns.

	.. versionadded:: 0.1.0
	"""
	checked = check_frame(EMPTY_FRAME, IsMissing())

	column_names = list(checked.columns)
	row_count = len(checked)
	assert column_names == EXPECTED_EMPTY_NAMES
	assert row_count == 0
