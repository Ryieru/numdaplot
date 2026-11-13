"""
Unit tests of the description of the columns of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.rules.between import Between
from numdaplot.rules.greater import Greater
from numdaplot.statistics.count import Count
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.share import Share
from numdaplot.tables.description.described_frame import (
	compute_description_cell,
	convert_result_to_text,
	describe_column,
	describe_frame,
	describe_statistic,
	find_described_columns,
	find_number_columns,
	find_result_family,
)
from numdaplot.tables.description.description import Description
from numdaplot.types.value_family import ValueFamily

FRAME = pandas.DataFrame(
	{
		"city": pandas.Series(["Pau", "Lyon"], dtype="string"),
		"price": [10.0, 30.0],
		"count": pandas.Series([1, None], dtype="Int64"),
		"paid": pandas.Series([True, False], dtype="boolean"),
	}
)
EXPECTED_DEFAULT_NAMES = [
	"count_excluded",
	"mean",
	"standard_deviation",
	"min",
	"quantile_25",
	"median",
	"quantile_75",
	"max",
]
EXPECTED_COLUMN_NAMES = ["statistic", "price", "count"]
EXPECTED_NUMBER_COLUMNS = ["price", "count"]
STATISTIC_FRAME = pandas.DataFrame({"statistic": [1.0]})
EXPECTED_MIXED_RESULTS = ["2", "Lyon", pandas.NA]
EXPECTED_NUMBER_RESULTS = [2.0, 20.0]
TEXTS = numpy.array(["a"], dtype="T")
NUMBER = numpy.array([2])
EXPECTED_TEXT = ["2"]
UTC_RESULT = numpy.array(["2026-07-01T08:30"], dtype="datetime64[ns]")
PARIS = TimeZone("Europe/Paris")
AGES = pandas.Series([70.0, None, 30.0, 80.0])
PRESENT_AGES = numpy.array([70.0, 30.0, 80.0])
SENIOR_AGE = 65
EXPECTED_SENIOR_SHARE = [2 / 3]
CITIES = pandas.Series(["Pau", "Lyon"], dtype="string")
PRESENT_CITIES = numpy.array(["Pau", "Lyon"], dtype="T")
EXPECTED_PARIS_TEXT = ["2026-07-01 10:30:00+02:00"]


def test_describe_frame_describes_every_number_column_by_default() -> None:
	"""
	Check the default statistics and the described columns.

	.. versionadded:: 0.1.0
	"""
	described_frame = describe_frame(FRAME, Description())

	statistic_column = described_frame["statistic"]
	statistic_names = statistic_column.tolist()
	column_names = described_frame.columns.tolist()
	assert statistic_names == EXPECTED_DEFAULT_NAMES
	assert column_names == EXPECTED_COLUMN_NAMES


def test_find_described_columns_keeps_the_given_columns() -> None:
	"""
	Check that given columns win over the number columns.

	.. versionadded:: 0.1.0
	"""
	description = Description(columns=["city"])

	described_names = find_described_columns(FRAME, description)

	assert described_names == ["city"]


def test_find_described_columns_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	description = Description(columns=["prise"])

	with pytest.raises(ColumnNotFoundError):
		find_described_columns(FRAME, description)


def test_find_described_columns_rejects_a_column_named_statistic() -> None:
	"""
	Check that a described column named statistic raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		find_described_columns(STATISTIC_FRAME, Description())


def test_find_number_columns_leaves_out_texts_and_booleans() -> None:
	"""
	Check that only integers and decimals are number columns.

	.. versionadded:: 0.1.0
	"""
	number_names = find_number_columns(FRAME)

	assert number_names == EXPECTED_NUMBER_COLUMNS


def test_describe_column_writes_mixed_results_as_texts() -> None:
	"""
	Check that a count and a text give texts, and a mean of texts is missing.

	.. versionadded:: 0.1.0
	"""
	city_column = FRAME["city"]

	described_column = describe_column(city_column, [Count(), Min(), Mean()])

	results = described_column.tolist()
	assert results == EXPECTED_MIXED_RESULTS


def test_describe_column_keeps_number_results_as_numbers() -> None:
	"""
	Check that a count and a mean stay numbers.

	.. versionadded:: 0.1.0
	"""
	price_column = FRAME["price"]

	described_column = describe_column(price_column, [Count(), Mean()])

	results = described_column.tolist()
	assert results == EXPECTED_NUMBER_RESULTS


def test_compute_description_cell_gives_nothing_for_a_statistic_that_does_not_apply() -> None:
	"""
	Check that the mean of texts gives None instead of an error.

	.. versionadded:: 0.1.0
	"""
	result = compute_description_cell(TEXTS, Mean(), TEXTS.size)

	assert result is None


def test_describe_statistic_computes_a_share_on_the_whole_column() -> None:
	"""
	Check the share of a column, its missing value left out.

	.. versionadded:: 0.2.0
	"""
	result = describe_statistic(AGES, PRESENT_AGES, Share(rule=Greater(SENIOR_AGE)))

	assert result is not None
	result_list = result.tolist()
	assert result_list == EXPECTED_SENIOR_SHARE


def test_describe_statistic_gives_nothing_for_a_share_whose_rule_does_not_apply() -> None:
	"""
	Check that a number interval on texts gives None instead of an error.

	.. versionadded:: 0.2.0
	"""
	result = describe_statistic(CITIES, PRESENT_CITIES, Share(rule=Between(1, 2)))

	assert result is None


def test_convert_result_to_text_writes_the_value() -> None:
	"""
	Check that a number becomes its text, and no result stays None.

	.. versionadded:: 0.1.0
	"""
	text_result = convert_result_to_text(NUMBER, None)
	no_result = convert_result_to_text(None, None)

	assert text_result is not None
	text_list = text_result.tolist()
	assert text_list == EXPECTED_TEXT
	assert no_result is None


def test_find_result_family_reads_the_family_of_the_type() -> None:
	"""
	Check that a number result belongs to the number family.

	.. versionadded:: 0.1.0
	"""
	result_family = find_result_family(NUMBER)

	assert result_family == ValueFamily.NUMBER


def test_convert_result_to_text_writes_a_datetime_in_the_zone_of_its_column() -> None:
	"""
	Check that a UTC result of a Paris column is written in Paris time with its offset.

	.. versionadded:: 0.1.0
	"""
	text_result = convert_result_to_text(UTC_RESULT, PARIS)

	assert text_result is not None
	text_list = text_result.tolist()
	assert text_list == EXPECTED_PARIS_TEXT
