"""
Unit tests of the summary of the missing values of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

from numdaplot.tables.missing.missing_summary import (
	format_ratio,
	list_summary_names,
	list_summary_types,
	summarize_missing,
)

FRAME = pandas.DataFrame(
	{
		"city": pandas.Series(["Paris", None, "Pau"], dtype="string"),
		"price": [120.0, None, None],
	}
)
EMPTY_FRAME = pandas.DataFrame({"price": pandas.Series(dtype="float64")})
EXPECTED_SUMMARY_COLUMNS = ["column", "type", "missing_count", "missing_ratio"]
EXPECTED_NAMES = ["city", "price", "total"]
EXPECTED_TYPES = ["TEXT", "FLOAT64", ""]
EXPECTED_COUNTS = [1, 2, 3]
EXPECTED_RATIOS = ["33.3 %", "66.7 %", "50.0 %"]
RATIOS_COLUMN = "missing_ratio"
COUNTS_COLUMN = "missing_count"
EIGHTH_RATIO = numpy.float64(0.125)
EXPECTED_EIGHTH_TEXT = "12.5 %"
NAN_RATIO = numpy.float64(numpy.nan)


def test_summarize_missing_has_one_row_per_column_then_a_total_row() -> None:
	"""
	Check the columns and the labels of the rows of the summary.

	.. versionadded:: 0.1.0
	"""
	summary = summarize_missing(FRAME)

	summary_columns = list(summary.columns)
	name_column = summary["column"]
	names = name_column.tolist()
	assert summary_columns == EXPECTED_SUMMARY_COLUMNS
	assert names == EXPECTED_NAMES


def test_summarize_missing_counts_each_column_and_the_whole_table() -> None:
	"""
	Check the counts and their percentages, the total ratio dividing by every value of the Table.

	.. versionadded:: 0.1.0
	"""
	summary = summarize_missing(FRAME)

	count_column = summary[COUNTS_COLUMN]
	ratio_column = summary[RATIOS_COLUMN]
	counts = count_column.tolist()
	ratios = ratio_column.tolist()
	assert counts == EXPECTED_COUNTS
	assert ratios == EXPECTED_RATIOS


def test_summarize_missing_leaves_the_ratios_of_a_table_without_rows_missing() -> None:
	"""
	Check that a Table without rows gives missing ratios.

	.. versionadded:: 0.1.0
	"""
	summary = summarize_missing(EMPTY_FRAME)

	ratio_column = summary[RATIOS_COLUMN]
	missing_ratios = ratio_column.isna()
	every_ratio_missing = bool(missing_ratios.all())
	assert every_ratio_missing


def test_list_summary_names_ends_with_the_total_label() -> None:
	"""
	Check the labels of the rows.

	.. versionadded:: 0.1.0
	"""
	summary_names = list_summary_names(FRAME)

	assert summary_names == EXPECTED_NAMES


def test_list_summary_types_leaves_the_type_of_the_total_row_empty() -> None:
	"""
	Check the type names of the rows.

	.. versionadded:: 0.1.0
	"""
	type_names = list_summary_types(FRAME)

	assert type_names == EXPECTED_TYPES


def test_format_ratio_writes_a_percentage_with_one_decimal() -> None:
	"""
	Check the text of a fraction.

	.. versionadded:: 0.1.0
	"""
	ratio_text = format_ratio(EIGHTH_RATIO)

	assert ratio_text == EXPECTED_EIGHTH_TEXT


def test_format_ratio_gives_nothing_for_nan() -> None:
	"""
	Check that NaN has no text.

	.. versionadded:: 0.1.0
	"""
	ratio_text = format_ratio(NAN_RATIO)

	assert ratio_text is None
