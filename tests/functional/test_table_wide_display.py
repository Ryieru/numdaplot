"""
Functional tests of the display of the columns of a wide Table.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

LONG_NAME = "a_long_column_name_"
COLUMN_COUNT = 14
LAST_COLUMN_NAME = "a_long_column_name_13"
DOTS = "..."
HIDDEN_COLUMN_NAME = "a_long_column_name_7"
DESCRIBED_STATISTIC = "count_excluded"


def build_wide_table() -> ndp.Table:
	"""
	Return a Table too wide for the width of the terminal.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		One row and 14 columns with long names.
	"""
	columns = {f"{LONG_NAME}{number}": ndp.Array.from_list([float(number)]) for number in range(COLUMN_COUNT)}
	wide_table = ndp.Table.from_arrays(columns)

	return wide_table


def test_print_shows_every_column() -> None:
	"""
	Check that printing a wide Table hides no column.

	.. versionadded:: 0.1.0
	"""
	table_text = str(build_wide_table())

	assert table_text.count(LONG_NAME) == COLUMN_COUNT
	assert DOTS not in table_text


def test_describe_shows_the_statistics_of_every_column() -> None:
	"""
	Check that the description of a wide Table hides no column.

	.. versionadded:: 0.1.0
	"""
	description_text = str(build_wide_table().describe())

	assert description_text.count(LONG_NAME) == COLUMN_COUNT
	assert DESCRIBED_STATISTIC in description_text


def test_preview_shows_every_column_by_default(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that a preview without settings hides no column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed rows.
	"""
	build_wide_table().preview()

	printed_text = capsys.readouterr().out
	assert printed_text.count(LONG_NAME) == COLUMN_COUNT
	assert DOTS not in printed_text


def test_a_compact_preview_replaces_the_columns_that_do_not_fit(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that a compact preview keeps the last column and hides those in the middle.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed rows.
	"""
	build_wide_table().preview(ndp.Preview(columns=ndp.ShownColumns.COMPACT))

	printed_text = capsys.readouterr().out
	assert DOTS in printed_text
	assert LAST_COLUMN_NAME in printed_text
	assert HIDDEN_COLUMN_NAME not in printed_text


def test_an_empty_filter_result_shows_its_columns_and_no_pandas_word(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check print and preview of a Table without rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Reads what is printed.
	"""
	prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	condition = ndp.Condition(rule=ndp.Greater(100.0), columns=["price"])
	empty = prices.filter(ndp.Filter(conditions=[condition]))

	print(empty)
	empty.preview()

	printed_text = capsys.readouterr().out
	assert printed_text.count("(0 rows)") == 2
	assert printed_text.count("FLOAT64") == 2
	assert "DataFrame" not in printed_text
	assert "Index" not in printed_text


def test_a_table_without_columns_gives_its_row_count(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check print of a Table whose columns were all removed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Reads what is printed.
	"""
	prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	no_columns = prices.choose_columns(ndp.ColumnChoice(columns=["price"], mode=ndp.ColumnMode.DROP))

	print(no_columns)

	printed_text = capsys.readouterr().out
	assert printed_text == "(no columns, 2 rows)\n"
