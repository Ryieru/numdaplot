"""
Unit tests of InvalidWeightError.

.. versionadded:: 0.2.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.tables.invalid_weight_error import InvalidWeightError

WEIGHT = -2.0
COLUMN_NAME = "weight"
EXPECTED_MESSAGE = "Expected weights of at least 0 in the column 'weight', got -2.0."


def test_invalid_weight_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidWeightError is caught by NumdaplotError.

	.. versionadded:: 0.2.0
	"""
	assert issubclass(InvalidWeightError, NumdaplotError)


def test_invalid_weight_error_names_the_weight_and_its_column() -> None:
	"""
	Check the message and the attributes.

	.. versionadded:: 0.2.0
	"""
	error = InvalidWeightError(WEIGHT, COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.weight == WEIGHT
	assert error.column_name == COLUMN_NAME
