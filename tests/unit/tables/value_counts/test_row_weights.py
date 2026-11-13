"""
Unit tests of the weights of the rows of a Table.

.. versionadded:: 0.2.0
"""

import numpy
import pandas
import pytest

from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.tables.invalid_weight_error import InvalidWeightError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.tables.value_counts.row_weights import (
	read_row_weights,
	require_number_weights,
	require_positive_weights,
	select_weighted_rows,
)

WEIGHT_COLUMN = "weight"
SEX_COLUMN = "sex"
INTEGER_DTYPE = "Int64"
TEXT_DTYPE = "string"
FRAME = pandas.DataFrame({SEX_COLUMN: [1, 2, 2], WEIGHT_COLUMN: [300.0, None, 100.0]})
EXPECTED_KEPT_SEXES = [1, 2]
EXPECTED_KEPT_WEIGHTS = [300.0, 100.0]
EXPECTED_ROW_NUMBERS = [0, 1]
EXPECTED_ROW_COUNT = 3
INTEGER_WEIGHTS = pandas.Series([3, None], dtype=INTEGER_DTYPE)
EXPECTED_INTEGER_WEIGHT = 3.0
TEXT_WEIGHTS = pandas.Series(["high"], dtype=TEXT_DTYPE)
EXPECTED_TEXT_MESSAGE = "Cannot apply ValueCount weights to the TEXT column 'weight'."
NEGATIVE_WEIGHTS = numpy.array([2.0, numpy.nan, -1.0, -5.0])
NEGATIVE_WEIGHT = -1.0
PRESENT_WEIGHTS = numpy.array([0.0, numpy.nan, 2.5])
UNKNOWN_COLUMN = "poids"


def test_select_weighted_rows_keeps_every_row_without_weights() -> None:
	"""
	Check that without weights every row counts once.

	.. versionadded:: 0.2.0
	"""
	weighted_rows = select_weighted_rows(FRAME, None)

	row_count = len(weighted_rows.frame)
	assert weighted_rows.weights is None
	assert row_count == EXPECTED_ROW_COUNT


def test_select_weighted_rows_leaves_out_the_rows_without_weight() -> None:
	"""
	Check that a row whose weight is missing is left out, the other rows numbered from 0.

	.. versionadded:: 0.2.0
	"""
	weighted_rows = select_weighted_rows(FRAME, WEIGHT_COLUMN)

	assert weighted_rows.weights is not None
	kept_frame = weighted_rows.frame
	sex_column = kept_frame[SEX_COLUMN]
	kept_weights = weighted_rows.weights.tolist()
	kept_sexes = sex_column.tolist()
	row_numbers = kept_frame.index.tolist()
	assert kept_weights == EXPECTED_KEPT_WEIGHTS
	assert kept_sexes == EXPECTED_KEPT_SEXES
	assert row_numbers == EXPECTED_ROW_NUMBERS


def test_read_row_weights_reads_integers_as_decimals() -> None:
	"""
	Check that integer weights become decimals, a missing weight NaN.

	.. versionadded:: 0.2.0
	"""
	frame = pandas.DataFrame({WEIGHT_COLUMN: INTEGER_WEIGHTS})

	weights = read_row_weights(frame, WEIGHT_COLUMN)

	first_weight = float(weights[0])
	is_second_missing = bool(numpy.isnan(weights[1]))
	assert first_weight == EXPECTED_INTEGER_WEIGHT
	assert is_second_missing


def test_read_row_weights_rejects_an_unknown_column() -> None:
	"""
	Check that a column of weights matching no column raises ColumnNotFoundError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ColumnNotFoundError):
		read_row_weights(FRAME, UNKNOWN_COLUMN)


def test_require_number_weights_names_a_column_of_texts() -> None:
	"""
	Check that weights written as texts raise IncompatibleTypesError naming their column.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(IncompatibleTypesError) as error_info:
		require_number_weights(TEXT_WEIGHTS, WEIGHT_COLUMN)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_TEXT_MESSAGE


def test_require_positive_weights_rejects_the_first_negative_weight() -> None:
	"""
	Check that the first negative weight raises InvalidWeightError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidWeightError) as error_info:
		require_positive_weights(NEGATIVE_WEIGHTS, WEIGHT_COLUMN)

	assert error_info.value.weight == NEGATIVE_WEIGHT


def test_require_positive_weights_accepts_zero_and_missing_weights() -> None:
	"""
	Check that a weight of 0 and a missing weight are accepted.

	.. versionadded:: 0.2.0
	"""
	require_positive_weights(PRESENT_WEIGHTS, WEIGHT_COLUMN)
