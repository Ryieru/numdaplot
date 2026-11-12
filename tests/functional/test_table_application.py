"""
Functional tests of a function applied to several columns of a Table.

.. versionadded:: 0.2.0
"""

from datetime import date

import pandas
import pytest

import numdaplot as ndp

INTEGER_DTYPE = "Int64"
QUESTION_NAMES = ["q1", "q2"]
FIRST_ANSWERS = [1, 7, 2]
SECOND_ANSWERS = [9, 3, 1]
EXPECTED_FIRST_ANSWERS = [1, None, 2]
EXPECTED_SECOND_ANSWERS = [None, 3, 1]
UNKNOWN_ANSWERS = ndp.ValueMapping(
	changes=[ndp.ValueChange(7, None), ndp.ValueChange(9, None)],
	others=ndp.Unmatched.KEEP,
)
EXPECTED_ANSWER_TYPES = {"q1": ndp.Type.INT64, "q2": ndp.Type.INT64, "city": ndp.Type.TEXT}
CITIES = ["Pau", "Dax", "Agen"]
AREAS = [4.0, 9.0]
VOLUMES = [16.0, 25.0]
EXPECTED_AREA_ROOTS = [2.0, 3.0]
EXPECTED_VOLUME_ROOTS = [4.0, 5.0]
NEGATIVE_VOLUMES = [16.0, -1.0]
EXPECTED_DOMAIN_MESSAGE = "SquareRoot is not defined for -1.0 in the column 'volume'."
MISSPELLED_COLUMN = "aera"
EXPECTED_NOT_FOUND_MESSAGE = "No column is named 'aera'."
SEX_CODES = [1, 2, 3]
SEX_LABELS = ndp.ValueMapping(changes=[ndp.ValueChange(1, "M"), ndp.ValueChange(2, "F")])
EXPECTED_UNMATCHED_MESSAGE = (
	"The value 3 of the column 'sex' has no ValueChange. Add one, or give others=Unmatched.MISSING to make it "
	"missing, or others=Unmatched.KEEP to keep it."
)
VISIT_DAYS = [date(2026, 3, 14), None, date(2026, 7, 1)]
EXPECTED_PRESENT_MONTHS = [3.0, 7.0]
EXPECTED_MISSING_MONTH_COUNT = 1
PICKUP_TEXTS = ["2026-03-14 23:30"]
PARIS_ZONE = "Europe/Paris"
EXPECTED_ZONE_MESSAGE = "Applying a function to 'pickup' needs datetimes without a time zone."


def build_survey() -> ndp.Table:
	"""
	Return a Table of two integer questions and a text column.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The columns q1, q2 and city.
	"""
	first_answers = ndp.Array.from_list(FIRST_ANSWERS)
	second_answers = ndp.Array.from_list(SECOND_ANSWERS)
	cities = ndp.Array.from_list(CITIES)
	survey = ndp.Table.from_arrays({"q1": first_answers, "q2": second_answers, "city": cities})

	return survey


def build_expected_survey() -> ndp.Table:
	"""
	Return the survey once the unknown answers are missing.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The integer columns q1 and q2 holding missing values, and the city column.
	"""
	first_answers = pandas.Series(EXPECTED_FIRST_ANSWERS, dtype=INTEGER_DTYPE)
	second_answers = pandas.Series(EXPECTED_SECOND_ANSWERS, dtype=INTEGER_DTYPE)
	frame = pandas.DataFrame({"q1": first_answers, "q2": second_answers, "city": CITIES})
	expected_survey = ndp.Table.from_pandas(frame)

	return expected_survey


def build_shapes() -> ndp.Table:
	"""
	Return a Table of areas and volumes.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The columns area and volume.
	"""
	areas = ndp.Array.from_list(AREAS)
	volumes = ndp.Array.from_list(VOLUMES)
	shapes = ndp.Table.from_arrays({"area": areas, "volume": volumes})

	return shapes


def test_listed_answers_become_missing_in_integer_columns() -> None:
	"""
	Check that several integer columns get missing values from a mapping and keep their type.

	.. versionadded:: 0.2.0
	"""
	survey = build_survey()
	expected_survey = build_expected_survey()

	cleaned_survey = survey.apply(ndp.TableApplication(function=UNKNOWN_ANSWERS, columns=QUESTION_NAMES))

	is_expected = cleaned_survey.is_equal(ndp.Equality(other=expected_survey))
	assert is_expected
	assert cleaned_survey.column_types == EXPECTED_ANSWER_TYPES


def test_the_source_table_keeps_its_values() -> None:
	"""
	Check that apply returns a new Table and leaves the source Table unchanged.

	.. versionadded:: 0.2.0
	"""
	survey = build_survey()
	original_survey = build_survey()

	survey.apply(ndp.TableApplication(function=UNKNOWN_ANSWERS, columns=QUESTION_NAMES))

	is_unchanged = survey.is_equal(ndp.Equality(other=original_survey))
	assert is_unchanged


def test_a_math_function_applies_to_each_listed_column() -> None:
	"""
	Check that a math function gives the result of each listed column.

	.. versionadded:: 0.2.0
	"""
	shapes = build_shapes()

	roots = shapes.apply(ndp.TableApplication(function=ndp.SquareRoot(), columns=["area", "volume"]))

	area_values = roots.column("area")
	volume_values = roots.column("volume")
	area_roots = area_values.to_list()
	volume_roots = volume_values.to_list()
	assert area_roots == EXPECTED_AREA_ROOTS
	assert volume_roots == EXPECTED_VOLUME_ROOTS


def test_a_time_function_skips_the_missing_dates() -> None:
	"""
	Check that a time function applies to a date column whose missing dates stay missing.

	.. versionadded:: 0.2.0
	"""
	days = ndp.Array.from_list(VISIT_DAYS)
	visits = ndp.Table.from_arrays({"day": days})
	month = ndp.DatePart(unit=ndp.DatePartUnit.MONTH)

	months = visits.apply(ndp.TableApplication(function=month, columns=["day"]))

	month_values = months.column("day")
	present_months = month_values.select(ndp.IsPresent())
	present_month_list = present_months.to_list()
	missing_flags = month_values.check(ndp.IsMissing())
	missing_sum = missing_flags.compute(ndp.Sum())
	missing_count = missing_sum.to_value()
	assert present_month_list == EXPECTED_PRESENT_MONTHS
	assert missing_count == EXPECTED_MISSING_MONTH_COUNT


def test_a_value_outside_the_domain_names_its_column() -> None:
	"""
	Check that the error of a math function names the column holding the value.

	.. versionadded:: 0.2.0
	"""
	areas = ndp.Array.from_list(AREAS)
	volumes = ndp.Array.from_list(NEGATIVE_VOLUMES)
	shapes = ndp.Table.from_arrays({"area": areas, "volume": volumes})

	with pytest.raises(ndp.OutOfDomainError) as error_info:
		shapes.apply(ndp.TableApplication(function=ndp.SquareRoot(), columns=["area", "volume"]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_DOMAIN_MESSAGE


def test_a_value_without_change_names_its_column() -> None:
	"""
	Check that the error of a mapping names the column holding the value.

	.. versionadded:: 0.2.0
	"""
	codes = ndp.Array.from_list(SEX_CODES)
	people = ndp.Table.from_arrays({"sex": codes})

	with pytest.raises(ndp.UnmatchedValueError) as error_info:
		people.apply(ndp.TableApplication(function=SEX_LABELS, columns=["sex"]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_UNMATCHED_MESSAGE


def test_an_unknown_column_is_refused() -> None:
	"""
	Check that a column name matching no column raises ColumnNotFoundError.

	.. versionadded:: 0.2.0
	"""
	shapes = build_shapes()

	with pytest.raises(ndp.ColumnNotFoundError) as error_info:
		shapes.apply(ndp.TableApplication(function=ndp.SquareRoot(), columns=["volume", MISSPELLED_COLUMN]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_NOT_FOUND_MESSAGE


def test_datetimes_with_a_time_zone_are_refused() -> None:
	"""
	Check that a datetime column with a time zone raises TimeZoneMismatchError naming the column.

	.. versionadded:: 0.2.0
	"""
	naive_times = pandas.to_datetime(PICKUP_TEXTS)
	naive_column = pandas.Series(naive_times)
	zoned_column = naive_column.dt.tz_localize(PARIS_ZONE)
	frame = pandas.DataFrame({"pickup": zoned_column})
	rides = ndp.Table.from_pandas(frame)
	hour = ndp.DatePart(unit=ndp.DatePartUnit.HOUR)

	with pytest.raises(ndp.TimeZoneMismatchError) as error_info:
		rides.apply(ndp.TableApplication(function=hour, columns=["pickup"]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_ZONE_MESSAGE
