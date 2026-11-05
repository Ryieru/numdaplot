"""
Functional tests of the missing values of a Table: check, count, summary and removal.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

import numdaplot as ndp

VISITS = pandas.DataFrame(
	{
		"city": pandas.Series(["Paris", None, "Pau", "Nice"], dtype="string"),
		"price": [120.0, None, None, 90.0],
		"visit": [1, 2, 3, 4],
	}
)
EXPECTED_MISSING_CITIES = [False, True, False, False]
EXPECTED_MISSING_TOTAL = 3
EXPECTED_COLUMN_NAMES = ["city", "price", "visit"]
EXPECTED_COLUMN_RATIOS = [0.25, 0.5, 0.0]
EXPECTED_ROW_COUNTS = [0, 2, 1, 0]
EXPECTED_COMPLETE_VISITS = [1, 4]
EXPECTED_VISITS_WITH_PRICE = [1, 4]
EXPECTED_COLUMNS_WITHOUT_MISSING = ["visit"]
EXPECTED_COLUMNS_UNDER_HALF = ["city", "visit"]
HALF_RATIO = 0.5
EXPECTED_SUMMARY_LINES = [
	"  column     type  missing_count missing_ratio",
	"0   city     TEXT              1        25.0 %",
	"1  price  FLOAT64              2        50.0 %",
	"2  visit    INT64              0         0.0 %",
	"3  total                       3        25.0 %",
]
UNKNOWN_NAMES = ["discount"]
PERCENTAGE_RATIO = 30


def build_visits() -> ndp.Table:
	"""
	Return a Table of four visits, some with a missing city or price.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The visits.
	"""
	visits = ndp.Table.from_pandas(VISITS)

	return visits


def read_visit_numbers(table: ndp.Table) -> list[int]:
	"""
	Return the visit numbers of a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		A Table of visits.

	Returns
	-------
	list[int]
		The visit numbers.
	"""
	visit_numbers = table.column("visit")
	visit_list = visit_numbers.to_list()

	return visit_list


def test_check_marks_the_missing_values_of_each_column() -> None:
	"""
	Check that check with IsMissing gives a boolean Table of the missing values.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	missing = visits.check(ndp.IsMissing())

	missing_cities = missing.column("city")
	missing_city_list = missing_cities.to_list()
	assert missing_city_list == EXPECTED_MISSING_CITIES


def test_count_missing_gives_the_total_of_the_table() -> None:
	"""
	Check the single count of the whole Table read with to_value.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	missing_count = visits.count_missing()

	missing_total = missing_count.to_value()
	assert missing_total == EXPECTED_MISSING_TOTAL


def test_count_missing_gives_the_ratio_of_each_column() -> None:
	"""
	Check the ratio per column, each next to the name of its column.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()
	settings = ndp.MissingCount(measure=ndp.Measure.RATIO)

	column_ratios = visits.count_missing(settings, axis=ndp.Axis.EACH_COLUMN)

	names = column_ratios.column("column")
	ratios = column_ratios.column("missing_ratio")
	name_list = names.to_list()
	ratio_list = ratios.to_list()
	assert name_list == EXPECTED_COLUMN_NAMES
	assert ratio_list == EXPECTED_COLUMN_RATIOS


def test_count_missing_gives_the_count_of_each_row() -> None:
	"""
	Check the count per row.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	row_counts = visits.count_missing(axis=ndp.Axis.EACH_ROW)

	counts = row_counts.column("missing_count")
	count_list = counts.to_list()
	assert count_list == EXPECTED_ROW_COUNTS


def test_preview_missing_prints_the_summary_of_each_column(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check the printed summary, with the total line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed text.
	"""
	visits = build_visits()

	visits.preview_missing()

	captured = capsys.readouterr()
	printed_text = captured.out.rstrip()
	printed_lines = printed_text.splitlines()
	assert printed_lines == EXPECTED_SUMMARY_LINES


def test_drop_missing_removes_every_row_holding_a_missing_value() -> None:
	"""
	Check the default removal of rows.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	complete_visits = visits.drop_missing()

	visit_numbers = read_visit_numbers(complete_visits)
	assert visit_numbers == EXPECTED_COMPLETE_VISITS


def test_drop_missing_looks_only_at_the_given_columns() -> None:
	"""
	Check that rows are removed for a missing price only.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	visits_with_price = visits.drop_missing(ndp.MissingDrop(columns=["price"]))

	visit_numbers = read_visit_numbers(visits_with_price)
	assert visit_numbers == EXPECTED_VISITS_WITH_PRICE


def test_drop_missing_removes_the_columns_holding_a_missing_value() -> None:
	"""
	Check the removal of columns.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	complete_columns = visits.drop_missing(axis=ndp.Axis.EACH_COLUMN)

	assert complete_columns.column_names == EXPECTED_COLUMNS_WITHOUT_MISSING


def test_drop_missing_removes_the_columns_reaching_a_ratio() -> None:
	"""
	Check that a column with half of its values missing is removed with MissingRatio(0.5).

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()
	settings = ndp.MissingDrop(rule=ndp.MissingRatio(HALF_RATIO))

	remaining = visits.drop_missing(settings, axis=ndp.Axis.EACH_COLUMN)

	assert remaining.column_names == EXPECTED_COLUMNS_UNDER_HALF


def test_drop_missing_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	with pytest.raises(ndp.ColumnNotFoundError):
		visits.drop_missing(ndp.MissingDrop(columns=UNKNOWN_NAMES))


def test_missing_ratio_rejects_a_percentage() -> None:
	"""
	Check that a ratio written as a percentage raises InvalidFractionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidFractionError):
		ndp.MissingRatio(PERCENTAGE_RATIO)
