"""
Unit tests of JoinRelationError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.join_relation_error import (
	JoinRelationError,
	format_combination,
	format_key_names,
	format_key_values,
)
from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.repeated_key import RepeatedKey

RELATION_NAME = "Relation.ONE_TO_MANY"
TABLE_NAME = "the left Table"
SINGLE_KEY = RepeatedKey(["Num_Acc"], [202500000001], 3)
EXPECTED_SINGLE_MESSAGE = (
	"Expected each key of the left Table to appear once for Relation.ONE_TO_MANY, but 'Num_Acc' 202500000001 "
	"appears 3 times."
)
COMBINED_KEY = RepeatedKey(["Num_Acc", "id_vehicule"], [202500000001, "A01"], 2)
EXPECTED_COMBINED_MESSAGE = (
	"Expected each key of the left Table to appear once for Relation.ONE_TO_MANY, but ('Num_Acc', 'id_vehicule') "
	"(202500000001, 'A01') appears 2 times."
)
SINGLE_NAME = ["Num_Acc"]
EXPECTED_SINGLE_NAME = "'Num_Acc'"
TEXT_VALUE = ["A01"]
EXPECTED_TEXT_VALUE = "'A01'"
NUMBER_VALUE = [101]
EXPECTED_NUMBER_VALUE = "101"
TWO_TEXTS = ["101", "'A01'"]
EXPECTED_COMBINATION = "(101, 'A01')"


def test_join_relation_error_is_a_numdaplot_error() -> None:
	"""
	Check that JoinRelationError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(JoinRelationError, NumdaplotError)


def test_join_relation_error_names_a_single_repeated_key() -> None:
	"""
	Check the message and the attributes for one key column.

	.. versionadded:: 0.1.0
	"""
	error = JoinRelationError(RELATION_NAME, TABLE_NAME, SINGLE_KEY)

	error_text = str(error)
	assert error_text == EXPECTED_SINGLE_MESSAGE
	assert error.relation_name == RELATION_NAME
	assert error.table_name == TABLE_NAME
	assert error.repeated_key == SINGLE_KEY


def test_join_relation_error_names_a_repeated_combination_of_keys() -> None:
	"""
	Check the message for two key columns.

	.. versionadded:: 0.1.0
	"""
	error = JoinRelationError(RELATION_NAME, TABLE_NAME, COMBINED_KEY)

	error_text = str(error)
	assert error_text == EXPECTED_COMBINED_MESSAGE


def test_format_key_names_quotes_a_single_name() -> None:
	"""
	Check that one name is quoted without parentheses.

	.. versionadded:: 0.1.0
	"""
	names_text = format_key_names(SINGLE_NAME)

	assert names_text == EXPECTED_SINGLE_NAME


def test_format_key_values_quotes_texts_only() -> None:
	"""
	Check that a text is quoted and a number is not.

	.. versionadded:: 0.1.0
	"""
	text_value = format_key_values(TEXT_VALUE)
	number_value = format_key_values(NUMBER_VALUE)

	assert text_value == EXPECTED_TEXT_VALUE
	assert number_value == EXPECTED_NUMBER_VALUE


def test_format_combination_puts_several_texts_between_parentheses() -> None:
	"""
	Check the combination of two texts.

	.. versionadded:: 0.1.0
	"""
	combination = format_combination(TWO_TEXTS)

	assert combination == EXPECTED_COMBINATION
