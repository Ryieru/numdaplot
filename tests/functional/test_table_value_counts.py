"""
Functional tests of the count of the values of a column of a Table.

.. versionadded:: 0.2.0
"""

import math

import pandas
import pytest

import numdaplot as ndp

SEX_COLUMN = "sex"
COUNT_NAME = "value_count"
RATIO_NAME = "value_ratio"
TIME_COLUMN = "visit_time"
PARIS_ZONE = "Europe/Paris"
UNKNOWN_COLUMN = "age"
ANSWERS = pandas.DataFrame({SEX_COLUMN: pandas.Series([2, 1, 2, None, 2, 1, 9], dtype="Int64")})
EXPECTED_PRESENT_SEXES = [2, 1, 9]
EXPECTED_MISSING_SEXES = [False, False, False, True]
EXPECTED_COUNTS = [3, 2, 1, 1]
RATIO_TOTAL = 1.0
VISIT_TIMES = ["2026-07-01 10:30", "2026-07-02 08:00", "2026-07-01 10:30"]
EXPECTED_TIME_TYPES = {TIME_COLUMN: ndp.Type.DATETIME, COUNT_NAME: ndp.Type.INT64}
EXPECTED_TIME_ZONES = {TIME_COLUMN: ndp.TimeZone(PARIS_ZONE)}


def build_answers() -> ndp.Table:
	"""
	Return a Table of survey answers coded 1 and 2, with one missing answer and one refusal coded 9.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The answers.
	"""
	answers = ndp.Table.from_pandas(ANSWERS)

	return answers


def test_count_values_lists_each_answer_from_the_most_frequent() -> None:
	"""
	Check the answers in their order, the missing answer last.

	.. versionadded:: 0.2.0
	"""
	answers = build_answers()

	counts = answers.count_values(ndp.ValueCount(column=SEX_COLUMN))

	missing_cells = counts.check(ndp.IsMissing())
	missing_sexes = missing_cells.column(SEX_COLUMN)
	present_counts = counts.drop_missing()
	present_sexes = present_counts.column(SEX_COLUMN)
	missing_list = missing_sexes.to_list()
	present_list = present_sexes.to_list()
	assert missing_list == EXPECTED_MISSING_SEXES
	assert present_list == EXPECTED_PRESENT_SEXES


def test_count_values_counts_the_rows_of_each_answer() -> None:
	"""
	Check the number of rows of each answer.

	.. versionadded:: 0.2.0
	"""
	answers = build_answers()

	counts = answers.count_values(ndp.ValueCount(column=SEX_COLUMN))

	count_values = counts.column(COUNT_NAME)
	count_list = count_values.to_list()
	assert count_list == EXPECTED_COUNTS


def test_count_values_gives_ratios_adding_up_to_one() -> None:
	"""
	Check that the ratios, the missing answer included, add up to 1.

	.. versionadded:: 0.2.0
	"""
	answers = build_answers()

	ratios = answers.count_values(ndp.ValueCount(column=SEX_COLUMN, measure=ndp.Measure.RATIO))

	ratio_values = ratios.column(RATIO_NAME)
	ratio_sum = ratio_values.compute(ndp.Sum())
	ratio_total = ratio_sum.to_value()
	is_total_one = math.isclose(ratio_total, RATIO_TOTAL)
	assert is_total_one


def test_count_values_keeps_the_type_and_the_time_zone_of_the_column() -> None:
	"""
	Check that datetimes keep their type and their time zone.

	.. versionadded:: 0.2.0
	"""
	visit_texts = pandas.Series(VISIT_TIMES)
	naive_times = pandas.to_datetime(visit_texts)
	visit_times = naive_times.dt.tz_localize(PARIS_ZONE)
	visit_frame = pandas.DataFrame({TIME_COLUMN: visit_times})
	visits = ndp.Table.from_pandas(visit_frame)

	counts = visits.count_values(ndp.ValueCount(column=TIME_COLUMN))

	assert counts.column_types == EXPECTED_TIME_TYPES
	assert counts.column_time_zones == EXPECTED_TIME_ZONES


def test_count_values_rejects_an_unknown_column() -> None:
	"""
	Check that a column the Table does not have raises ColumnNotFoundError.

	.. versionadded:: 0.2.0
	"""
	answers = build_answers()

	with pytest.raises(ndp.ColumnNotFoundError):
		answers.count_values(ndp.ValueCount(column=UNKNOWN_COLUMN))
