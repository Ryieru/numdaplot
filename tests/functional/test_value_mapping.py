"""
Functional tests of the replacement of values by other values.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

SEX_CODES = [1, 2, 2, -1]
SEX_LABELS = ndp.ValueMapping(
	changes=[ndp.ValueChange(1, "Masculin"), ndp.ValueChange(2, "Feminin"), ndp.ValueChange(-1, None)]
)
EXPECTED_SEX_LABELS = ["Masculin", "Feminin", "Feminin", None]
GRAVITY_CODES = [1, 4, 9]
GRAVITY_LABELS = [ndp.ValueChange(1, "Indemne"), ndp.ValueChange(4, "Blesse leger")]
EXPECTED_UNMATCHED_MESSAGE = (
	"The value 9 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing."
)
EXPECTED_GRAVITY_LABELS = ["Indemne", "Blesse leger", None]
RATE_MAPPING = ndp.ValueMapping(changes=[ndp.ValueChange(1, 10)], others=ndp.Unmatched.MISSING)
EXPECTED_RATE_MESSAGE = (
	"INT64 values cannot be missing in an Array. Give decimal new values, such as 10.0, which can be missing."
)
DECIMAL_RATE_MAPPING = ndp.ValueMapping(changes=[ndp.ValueChange(1, 10.0)], others=ndp.Unmatched.MISSING)


def test_a_column_of_codes_gets_its_labels() -> None:
	"""
	Check the BAAC use: codes of a Table column replaced by labels, -1 becoming missing, then added back.

	.. versionadded:: 0.1.0
	"""
	codes = ndp.Array.from_list(SEX_CODES)
	victims = ndp.Table.from_arrays({"sexe": codes})

	labels = victims.column("sexe").apply(SEX_LABELS)
	labeled_victims = victims.add_column(ndp.NewColumn(name="sexe", values=labels, on_conflict=ndp.Conflict.REPLACE))

	sex_column = labeled_victims.column("sexe")
	sex_labels = sex_column.to_list()
	assert sex_labels == EXPECTED_SEX_LABELS


def test_a_code_without_label_is_named_in_the_error() -> None:
	"""
	Check that a forgotten code raises UnmatchedValueError naming it.

	.. versionadded:: 0.1.0
	"""
	codes = ndp.Array.from_list(GRAVITY_CODES)

	with pytest.raises(ndp.UnmatchedValueError) as error_info:
		codes.apply(ndp.ValueMapping(changes=GRAVITY_LABELS))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_UNMATCHED_MESSAGE


def test_codes_without_label_become_missing_when_asked() -> None:
	"""
	Check Unmatched.MISSING on a forgotten code.

	.. versionadded:: 0.1.0
	"""
	codes = ndp.Array.from_list(GRAVITY_CODES)

	labels = codes.apply(ndp.ValueMapping(changes=GRAVITY_LABELS, others=ndp.Unmatched.MISSING))

	gravity_labels = labels.to_list()
	assert gravity_labels == EXPECTED_GRAVITY_LABELS


def test_integers_with_a_missing_value_point_to_decimal_new_values() -> None:
	"""
	Check the message of integer new values that would hold a missing value, and the decimal solution.

	.. versionadded:: 0.1.0
	"""
	codes = ndp.Array.from_list(GRAVITY_CODES)

	with pytest.raises(ndp.UnsupportedMissingError) as error_info:
		codes.apply(RATE_MAPPING)

	rates = codes.apply(DECIMAL_RATE_MAPPING)
	error_text = str(error_info.value)
	rate_type = rates.dtype
	assert error_text == EXPECTED_RATE_MESSAGE
	assert rate_type == ndp.Type.FLOAT64


def test_an_old_value_given_twice_is_refused() -> None:
	"""
	Check that 2 and 2.0 in two changes raise DuplicateValueError when the mapping is created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.DuplicateValueError):
		ndp.ValueMapping(changes=[ndp.ValueChange(2, "Feminin"), ndp.ValueChange(2.0, "F")])
