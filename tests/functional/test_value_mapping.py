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
	"The value 9 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing, or "
	"others=Unmatched.KEEP to keep it."
)
EXPECTED_GRAVITY_LABELS = ["Indemne", "Blesse leger", None]
RATE_MAPPING = ndp.ValueMapping(changes=[ndp.ValueChange(1, 10)], others=ndp.Unmatched.MISSING)
EXPECTED_RATE_MESSAGE = (
	"INT64 values cannot be missing in an Array. Give decimal new values, such as 10.0, which can be missing."
)
DECIMAL_RATE_MAPPING = ndp.ValueMapping(changes=[ndp.ValueChange(1, 10.0)], others=ndp.Unmatched.MISSING)
SURVEY_ANSWERS = [1.0, 7.0, 3.0, 9.0, 5.0]
UNKNOWN_ANSWERS = ndp.ValueMapping(
	changes=[ndp.ValueChange(7, None), ndp.ValueChange(9, None)], others=ndp.Unmatched.KEEP
)
EXPECTED_KNOWN_ANSWERS = [1.0, 3.0, 5.0]
EXPECTED_UNKNOWN_COUNT = 2
INTEGER_ANSWERS = [1, 7, 3]
DECIMAL_DIABETES_CODES = [1.0, 3.0, 7.0]
DIABETES_TARGET = ndp.ValueMapping(changes=[ndp.ValueChange(1, 1), ndp.ValueChange(3, 0)], others=ndp.Unmatched.MISSING)
EXPECTED_PRESENT_TARGETS = [1.0, 0.0]
SMALL_CODES = [1, 2]
SMALL_CODE_LABELS = ndp.ValueMapping(changes=[ndp.ValueChange(1, 100), ndp.ValueChange(2, 2)])
UNKNOWN_ANSWER_CODES = [7.0, 9.0]
INTEGER_UNKNOWN_ANSWERS = [7, 9]
ONLY_UNKNOWN_ANSWERS = ndp.ValueMapping(changes=[ndp.ValueChange(7, None), ndp.ValueChange(9, None)])
EXPECTED_MISSING_ANSWER_COUNT = 2
EXPECTED_KEPT_INTEGER_MESSAGE = (
	"INT64 values cannot be missing in an Array. Give decimal new values, such as 10.0, or convert the Array to "
	"FLOAT64 first."
)


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


def test_only_listed_answers_become_missing_when_the_others_are_kept() -> None:
	"""
	Check that Unmatched.KEEP empties the unknown answers of a survey column and keeps the other answers.

	.. versionadded:: 0.2.0
	"""
	health_answers = ndp.Array.from_list(SURVEY_ANSWERS)
	survey = ndp.Table.from_arrays({"health": health_answers})
	health_column = survey.column("health")

	answers = health_column.apply(UNKNOWN_ANSWERS)

	known_values = answers.select(ndp.IsPresent())
	known_answers = known_values.to_list()
	unknown_flags = answers.check(ndp.IsMissing())
	unknown_count = unknown_flags.compute(ndp.Sum()).to_value()
	assert known_answers == EXPECTED_KNOWN_ANSWERS
	assert unknown_count == EXPECTED_UNKNOWN_COUNT


def test_kept_integers_with_a_missing_value_point_to_a_conversion() -> None:
	"""
	Check that integers kept with a missing value raise an error advising to convert the Array to FLOAT64.

	.. versionadded:: 0.2.0
	"""
	answers = ndp.Array.from_list(INTEGER_ANSWERS)

	with pytest.raises(ndp.UnsupportedMissingError) as error_info:
		answers.apply(UNKNOWN_ANSWERS)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_KEPT_INTEGER_MESSAGE


def test_decimals_given_only_missing_values_stay_decimals() -> None:
	"""
	Check that a mapping making every value missing keeps the decimal type of the Array.

	.. versionadded:: 0.2.0
	"""
	answers = ndp.Array.from_list(UNKNOWN_ANSWER_CODES)

	cleared_answers = answers.apply(ONLY_UNKNOWN_ANSWERS)

	missing_flags = cleared_answers.check(ndp.IsMissing())
	missing_count = missing_flags.compute(ndp.Sum()).to_value()
	assert cleared_answers.dtype == ndp.Type.FLOAT64
	assert missing_count == EXPECTED_MISSING_ANSWER_COUNT


def test_integers_given_only_missing_values_point_to_a_conversion() -> None:
	"""
	Check that integers made all missing raise an error advising to convert the Array to FLOAT64.

	.. versionadded:: 0.2.0
	"""
	answers = ndp.Array.from_list(INTEGER_UNKNOWN_ANSWERS)

	with pytest.raises(ndp.UnsupportedMissingError) as error_info:
		answers.apply(ONLY_UNKNOWN_ANSWERS)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_KEPT_INTEGER_MESSAGE


def test_decimal_codes_recoded_with_integers_stay_decimals_and_hold_missing_values() -> None:
	"""
	Check that integer new values given to decimal codes take the decimal type, so that other codes can be missing.

	.. versionadded:: 0.2.0
	"""
	codes = ndp.Array.from_list(DECIMAL_DIABETES_CODES)

	targets = codes.apply(DIABETES_TARGET)

	present_values = targets.select(ndp.IsPresent())
	present_targets = present_values.to_list()
	assert targets.dtype == ndp.Type.FLOAT64
	assert present_targets == EXPECTED_PRESENT_TARGETS


def test_small_integer_codes_keep_their_type() -> None:
	"""
	Check that a column converted to INT8 keeps INT8 when its codes get integer new values.

	.. versionadded:: 0.2.0
	"""
	codes = ndp.Array.from_list(SMALL_CODES)
	table = ndp.Table.from_arrays({"code": codes})
	small_table = table.convert(ndp.TableConversion(column="code", dtype=ndp.Type.INT8))
	small_codes = small_table.column("code")

	new_codes = small_codes.apply(SMALL_CODE_LABELS)

	assert new_codes.dtype == ndp.Type.INT8


def test_an_old_value_given_twice_is_refused() -> None:
	"""
	Check that 2 and 2.0 in two changes raise DuplicateValueError when the mapping is created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.DuplicateValueError):
		ndp.ValueMapping(changes=[ndp.ValueChange(2, "Feminin"), ndp.ValueChange(2.0, "F")])
