"""
Functional tests of the statistics of an Array.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

import numdaplot as ndp

TEMPERATURES = [12.0, None, 18.0]
EXPECTED_MEAN_TEMPERATURE = 15.0
PRESENT_TEMPERATURE_COUNT = 2
SALES = [[1, 2, 3], [4, 5, 6]]
EXPECTED_ROW_TOTALS = [6, 15]
EXPECTED_COLUMN_MAXIMUMS = [4, 5, 6]
COUNTRIES = ["FR", "DE", "FR"]
MOST_FREQUENT_COUNTRY = "FR"
DAYS = [date(2026, 3, 1), None, date(2025, 1, 1)]
EARLIEST_DAY = date(2025, 1, 1)
MISSING_TEMPERATURES = [None, None]
SALARIES = [1000, 2000, 3000, 4000, 5000]
NINTH_DECILE = 0.9
EXPECTED_NINTH_DECILE = 4600.0


def test_the_mean_ignores_missing_values() -> None:
	"""
	Check that the mean of 12, None and 18 is 15.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(TEMPERATURES)

	mean_temperature = temperatures.compute(ndp.Mean())

	mean_value = mean_temperature.to_value()
	assert mean_value == EXPECTED_MEAN_TEMPERATURE


def test_the_count_ignores_missing_values() -> None:
	"""
	Check that Count gives the number of present values.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(TEMPERATURES)

	temperature_count = temperatures.compute(ndp.Count())

	count_value = temperature_count.to_value()
	assert count_value == PRESENT_TEMPERATURE_COUNT


def test_a_statistic_gives_one_value_per_row() -> None:
	"""
	Check that EACH_ROW gives the total of each row.

	.. versionadded:: 0.1.0
	"""
	sales = ndp.Array.from_list(SALES)

	row_totals = sales.compute(ndp.Sum(), axis=ndp.Axis.EACH_ROW)

	row_total_list = row_totals.to_list()
	assert row_total_list == EXPECTED_ROW_TOTALS


def test_a_statistic_gives_one_value_per_column() -> None:
	"""
	Check that EACH_COLUMN gives the maximum of each column.

	.. versionadded:: 0.1.0
	"""
	sales = ndp.Array.from_list(SALES)

	column_maximums = sales.compute(ndp.Max(), axis=ndp.Axis.EACH_COLUMN)

	column_maximum_list = column_maximums.to_list()
	assert column_maximum_list == EXPECTED_COLUMN_MAXIMUMS


def test_the_most_frequent_text_is_found() -> None:
	"""
	Check that MostFrequent works on texts.

	.. versionadded:: 0.1.0
	"""
	countries = ndp.Array.from_list(COUNTRIES)

	most_frequent = countries.compute(ndp.MostFrequent())

	most_frequent_value = most_frequent.to_value()
	assert most_frequent_value == MOST_FREQUENT_COUNTRY


def test_the_earliest_date_ignores_missing_dates() -> None:
	"""
	Check that Min works on dates holding a missing date.

	.. versionadded:: 0.1.0
	"""
	days = ndp.Array.from_list(DAYS)

	earliest = days.compute(ndp.Min())

	earliest_value = earliest.to_value()
	assert earliest_value == EARLIEST_DAY


def test_a_quantile_is_computed() -> None:
	"""
	Check the ninth decile of five salaries.

	.. versionadded:: 0.1.0
	"""
	salaries = ndp.Array.from_list(SALARIES)

	ninth_decile = salaries.compute(ndp.Quantile(NINTH_DECILE))

	decile_value = ninth_decile.to_value()
	is_close = numpy.allclose(decile_value, EXPECTED_NINTH_DECILE)
	assert is_close


def test_the_mean_of_only_missing_values_is_rejected() -> None:
	"""
	Check that Mean without any present value raises EmptyArrayError.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(MISSING_TEMPERATURES, dtype=ndp.Type.FLOAT64)

	with pytest.raises(ndp.EmptyArrayError):
		temperatures.compute(ndp.Mean())


def test_the_mean_of_texts_is_rejected() -> None:
	"""
	Check that Mean on texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	countries = ndp.Array.from_list(COUNTRIES)

	with pytest.raises(ndp.IncompatibleTypesError):
		countries.compute(ndp.Mean())
