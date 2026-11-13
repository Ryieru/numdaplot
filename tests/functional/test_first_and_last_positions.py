"""
Functional tests of the first and the last positions of an Array or a Table.

.. versionadded:: 0.2.0
"""

import pytest

import numdaplot as ndp

CITIES = ["Pau", "Lyon", "Paris", "Nice", "Dax"]
SCORES = [12, 45, 30, 51, 8]
TOP_COUNT = 3
EXPECTED_TOP_CITIES = ["Nice", "Lyon", "Paris"]
EXPECTED_BOTTOM_CITIES = ["Pau", "Dax"]
LARGE_COUNT = 10
EXPECTED_COLUMN_NAMES = ["city", "score"]
GRID = [[1, 2, 3], [4, 5, 6]]
EXPECTED_LAST_COLUMNS = [[2, 3], [5, 6]]
EXPECTED_REPLACED_SCORES = [12, 45, 30, 0, 0]
EXPECTED_COUNT_MESSAGE = "Expected a count of at least 1, got 0."


def build_scores() -> ndp.Table:
	"""
	Return a Table of scores per city.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The columns city, score and rank.
	"""
	cities = ndp.Array.from_list(CITIES)
	scores = ndp.Array.from_list(SCORES)
	ranks = ndp.Array.from_list(SCORES)
	score_table = ndp.Table.from_arrays({"city": cities, "score": scores, "rank": ranks})

	return score_table


def sort_by_score(score_table: ndp.Table) -> ndp.Table:
	"""
	Return a Table sorted from the highest score to the lowest.

	.. versionadded:: 0.2.0

	Parameters
	----------
	score_table
		A Table with a score column.

	Returns
	-------
	ndp.Table
		The sorted Table.
	"""
	score_key = ndp.SortKey(column="score", order=ndp.Order.DESCENDING)
	sorting = ndp.TableSorting(keys=[score_key])
	sorted_table = score_table.sort(sorting)

	return sorted_table


def test_the_first_rows_of_a_sorted_table_are_its_top() -> None:
	"""
	Check that First takes the highest scores of a Table sorted from the highest.

	.. versionadded:: 0.2.0
	"""
	score_table = build_scores()
	sorted_scores = sort_by_score(score_table)

	top_scores = sorted_scores.take(ndp.Region(rows=ndp.First(TOP_COUNT)))

	top_city_values = top_scores.column("city")
	top_cities = top_city_values.to_list()
	assert top_cities == EXPECTED_TOP_CITIES


def test_the_last_rows_of_a_sorted_table_are_its_bottom() -> None:
	"""
	Check that Last takes the lowest scores, in the order of the Table.

	.. versionadded:: 0.2.0
	"""
	score_table = build_scores()
	sorted_scores = sort_by_score(score_table)

	bottom_scores = sorted_scores.take(ndp.Region(rows=ndp.Last(2)))

	bottom_city_values = bottom_scores.column("city")
	bottom_cities = bottom_city_values.to_list()
	assert bottom_cities == EXPECTED_BOTTOM_CITIES


def test_a_table_shorter_than_the_count_keeps_every_row() -> None:
	"""
	Check that First beyond the number of rows takes every row without error.

	.. versionadded:: 0.2.0
	"""
	score_table = build_scores()

	first_scores = score_table.take(ndp.Region(rows=ndp.First(LARGE_COUNT)))

	city_count = len(CITIES)
	assert first_scores.row_count == city_count


def test_the_first_columns_of_a_table_are_taken_by_position() -> None:
	"""
	Check that First chooses the first columns of a Table.

	.. versionadded:: 0.2.0
	"""
	score_table = build_scores()

	first_columns = score_table.take(ndp.Region(columns=ndp.First(2)))

	assert first_columns.column_names == EXPECTED_COLUMN_NAMES


def test_the_last_columns_of_a_grid_are_taken_by_position() -> None:
	"""
	Check that Last chooses the last columns of a two-dimensional Array.

	.. versionadded:: 0.2.0
	"""
	grid = ndp.Array.from_list(GRID)

	last_columns = grid.take(ndp.Region(columns=ndp.Last(2)))

	last_values = last_columns.to_list()
	assert last_values == EXPECTED_LAST_COLUMNS


def test_the_last_values_of_an_array_are_replaced() -> None:
	"""
	Check that Last chooses the values that replace changes.

	.. versionadded:: 0.2.0
	"""
	scores = ndp.Array.from_list(SCORES)
	replacement = ndp.Replacement(region=ndp.Region(rows=ndp.Last(2)), value=0)

	replaced_scores = scores.replace(replacement)

	replaced_values = replaced_scores.to_list()
	assert replaced_values == EXPECTED_REPLACED_SCORES


def test_no_first_row_is_refused() -> None:
	"""
	Check that First(0) raises InvalidCountError when it is created.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ndp.InvalidCountError) as error_info:
		ndp.First(0)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_COUNT_MESSAGE
