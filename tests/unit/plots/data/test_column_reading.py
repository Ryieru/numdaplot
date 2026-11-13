"""
Unit tests of the reading of the Table columns a chart draws.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.column_reading import (
	count_hours,
	find_value_families,
	read_hours,
	read_moments,
	read_numbers,
	read_positions,
	read_texts,
	read_values,
	require_same_family,
	write_hour_labels,
)
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.types.type import Type
from numdaplot.types.value_family import ValueFamily

CHART_NAME = "LineChart"
INTEGERS = pandas.Series([3, None, 5], dtype="Int64")
EXPECTED_NUMBERS = [3.0, 5.0]
TEXTS = pandas.Series(["Paris", None], dtype="string")
EXPECTED_TEXTS = ["Paris", None]
CATEGORIES = pandas.Series(["Paris", "Lyon"], dtype="category")
BOOLEANS = pandas.Series([True, False], dtype="boolean")
DURATIONS = pandas.Series(numpy.array([1, 2], dtype="timedelta64[h]").astype("timedelta64[ns]"))
DAYS = pandas.Series([pandas.Timestamp("2026-01-01"), pandas.NaT]).astype("datetime64[s]")
UTC_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("UTC")
PARIS_TIMES = UTC_TIMES.dt.tz_convert("Europe/Paris")
EXPECTED_PARIS_CLOCK = numpy.datetime64("2026-07-01T12:30", "ns")
MOMENT_DTYPE = numpy.dtype("datetime64[ns]")
REFUSED_POSITIONS = [DURATIONS]
STORED_HOURS = pandas.Series(numpy.array([55800000000, "NaT"], dtype="timedelta64[us]"))
EXPECTED_HOUR_LABELS = ["15:30", None]
HALF_PAST_THREE_HOURS = 15.5
TIME_VALUE_CHART_NAME = "BoxChart"
NUMBER_VALUE_CHART_NAME = "BarChart"
EXPECTED_TIME_VALUE_FAMILIES = frozenset({ValueFamily.NUMBER, ValueFamily.TIME})
EXPECTED_NUMBER_VALUE_FAMILIES = frozenset({ValueFamily.NUMBER})
NAMED_COUNTS = pandas.Series([3.0], name="count")
STORED_HOUR_GRID = numpy.array([[55800000000, "NaT"]], dtype="timedelta64[us]")
EXPECTED_HOUR_GRID_SHAPE = (1, 2)


def test_read_numbers_gives_nan_at_missing_integers() -> None:
	"""
	Check that a nullable integer column becomes float64 numbers with NaN.

	.. versionadded:: 0.1.0
	"""
	numbers = read_numbers(INTEGERS, CHART_NAME)

	missing = numpy.isnan(numbers)
	present_numbers = numbers[~missing].tolist()
	assert numbers.dtype == numpy.float64
	assert missing.tolist() == [False, True, False]
	assert present_numbers == EXPECTED_NUMBERS


def test_read_numbers_rejects_texts() -> None:
	"""
	Check that a text column raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_numbers(TEXTS, CHART_NAME)


def test_read_texts_gives_none_at_missing_texts() -> None:
	"""
	Check that a missing text becomes None.

	.. versionadded:: 0.1.0
	"""
	texts = read_texts(TEXTS, CHART_NAME)

	text_list = texts.tolist()
	assert text_list == EXPECTED_TEXTS


def test_read_texts_reads_categories_as_texts() -> None:
	"""
	Check that a category column gives its texts.

	.. versionadded:: 0.1.0
	"""
	texts = read_texts(CATEGORIES, CHART_NAME)

	text_list = texts.tolist()
	category_list = CATEGORIES.tolist()
	assert text_list == category_list


def test_read_moments_gives_the_clock_time_of_the_zone() -> None:
	"""
	Check that a datetime with a time zone gives its clock time in that zone, without zone.

	.. versionadded:: 0.1.0
	"""
	moments = read_moments(PARIS_TIMES)

	assert moments[0] == EXPECTED_PARIS_CLOCK


def test_read_moments_gives_nat_at_a_missing_date() -> None:
	"""
	Check that a missing date becomes NaT, in datetime64[ns].

	.. versionadded:: 0.1.0
	"""
	moments = read_moments(DAYS)

	missing = numpy.isnat(moments).tolist()
	assert moments.dtype == MOMENT_DTYPE
	assert missing == [False, True]


@pytest.mark.parametrize(
	("column", "expected_kind"),
	[(INTEGERS, PositionKind.NUMBERS), (DAYS, PositionKind.MOMENTS), (TEXTS, PositionKind.TEXTS)],
)
def test_read_positions_finds_the_kind_of_the_column(column: pandas.Series, expected_kind: PositionKind) -> None:
	"""
	Check that numbers, dates and texts give their position kind.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column of numbers, dates or texts.
	expected_kind
		Its kind of positions.
	"""
	kind, _ = read_positions(column, CHART_NAME)

	assert kind == expected_kind


@pytest.mark.parametrize("column", REFUSED_POSITIONS)
def test_read_positions_rejects_durations(column: pandas.Series) -> None:
	"""
	Check that durations raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column of durations.
	"""
	with pytest.raises(IncompatibleTypesError):
		read_positions(column, CHART_NAME)


def test_read_texts_writes_booleans_and_keeps_missing_ones() -> None:
	"""
	Check that booleans become the texts shown by a Table, None where one is missing.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series([True, None, False], dtype="boolean")

	texts = read_texts(column, CHART_NAME)

	assert texts.tolist() == ["True", None, "False"]


def test_read_positions_places_booleans_as_texts() -> None:
	"""
	Check that booleans take the positions of texts.

	.. versionadded:: 0.1.0
	"""
	kind, values = read_positions(BOOLEANS, CHART_NAME)

	assert kind == PositionKind.TEXTS
	assert values.tolist() == ["True", "False"]


def test_read_hours_counts_hours_since_midnight() -> None:
	"""
	Check 15:30 as 15.5 and NaN for a missing time.

	.. versionadded:: 0.1.0
	"""
	hours = read_hours(STORED_HOURS)

	second_missing = numpy.isnan(hours[1])
	is_second_missing = bool(second_missing)
	assert hours[0] == HALF_PAST_THREE_HOURS
	assert is_second_missing


def test_read_texts_writes_times_as_hour_labels() -> None:
	"""
	Check that times of day become HH:MM labels, None where missing.

	.. versionadded:: 0.1.0
	"""
	texts = read_texts(STORED_HOURS, "PieChart")

	text_list = texts.tolist()
	assert text_list == EXPECTED_HOUR_LABELS


def test_write_hour_labels_drops_the_seconds() -> None:
	"""
	Check the HH:MM labels of times of day.

	.. versionadded:: 0.1.0
	"""
	labels = write_hour_labels(STORED_HOURS)

	label_list = labels.tolist()
	assert label_list == EXPECTED_HOUR_LABELS


def test_read_positions_places_times_on_a_day() -> None:
	"""
	Check that a column of times gives positions in hours.

	.. versionadded:: 0.1.0
	"""
	kind, values = read_positions(STORED_HOURS, "LineChart")

	assert kind == PositionKind.TIMES
	assert values[0] == HALF_PAST_THREE_HOURS


@pytest.mark.parametrize(
	("chart_name", "expected_families"),
	[(TIME_VALUE_CHART_NAME, EXPECTED_TIME_VALUE_FAMILIES), (NUMBER_VALUE_CHART_NAME, EXPECTED_NUMBER_VALUE_FAMILIES)],
)
def test_find_value_families_adds_times_for_the_charts_measuring_them(
	chart_name: str, expected_families: frozenset[ValueFamily]
) -> None:
	"""
	Check that a box chart draws numbers and times of day, and a bar chart numbers only.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class.
	expected_families
		The families it draws.
	"""
	value_families = find_value_families(chart_name)

	assert value_families == expected_families


def test_read_values_counts_times_in_hours() -> None:
	"""
	Check that times of day drawn as values become their hours since midnight.

	.. versionadded:: 0.1.0
	"""
	values = read_values(STORED_HOURS, TIME_VALUE_CHART_NAME)

	first_value = values[0]
	second_value = values[1]
	second_missing = numpy.isnan(second_value)
	is_second_missing = bool(second_missing)
	assert first_value == HALF_PAST_THREE_HOURS
	assert is_second_missing


def test_read_values_reads_numbers_as_decimals() -> None:
	"""
	Check that numbers drawn as values become float64 numbers.

	.. versionadded:: 0.1.0
	"""
	values = read_values(INTEGERS, NUMBER_VALUE_CHART_NAME)

	missing_values = numpy.isnan(values)
	present_values = values[~missing_values]
	value_list = present_values.tolist()
	assert value_list == EXPECTED_NUMBERS


def test_read_values_rejects_times_for_a_chart_of_numbers() -> None:
	"""
	Check that times of day drawn as bars raise IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_values(STORED_HOURS, NUMBER_VALUE_CHART_NAME)


def test_require_same_family_accepts_numbers_of_another_type() -> None:
	"""
	Check that integers next to decimals are accepted.

	.. versionadded:: 0.1.0
	"""
	require_same_family(INTEGERS, Type.FLOAT64, TIME_VALUE_CHART_NAME)


def test_require_same_family_rejects_numbers_next_to_times() -> None:
	"""
	Check that numbers next to times of day raise IncompatibleTypesError naming the column.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError) as error_info:
		require_same_family(NAMED_COUNTS, Type.TIME, TIME_VALUE_CHART_NAME)

	assert error_info.value.column_name == NAMED_COUNTS.name


def test_count_hours_keeps_the_shape_of_the_times() -> None:
	"""
	Check that a grid of times gives a grid of hours, NaN where a time is missing.

	.. versionadded:: 0.1.0
	"""
	hours = count_hours(STORED_HOUR_GRID)

	first_hour = hours[0, 0]
	missing_hour = hours[0, 1]
	hour_missing = numpy.isnan(missing_hour)
	is_missing = bool(hour_missing)
	assert hours.shape == EXPECTED_HOUR_GRID_SHAPE
	assert first_hour == HALF_PAST_THREE_HOURS
	assert is_missing
