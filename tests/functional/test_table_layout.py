"""
Functional tests of the sort and the removal of duplicated rows of a Table.

.. versionadded:: 0.1.0
"""

import pandas

import numdaplot as ndp

VISITS = pandas.DataFrame(
	{
		"email": pandas.Series(["b@x.fr", "a@x.fr", "b@x.fr", None], dtype="string"),
		"amount": [20.0, None, 10.0, 5.0],
		"visit": [1, 2, 3, 4],
	}
)
EXPECTED_BY_EMAIL_THEN_AMOUNT = [2, 1, 3, 4]
EXPECTED_MISSING_AMOUNT_FIRST = [2, 4, 3, 1]
EXPECTED_FIRST_VISITS = [1, 2, 4]
EXPECTED_LAST_VISITS = [2, 3, 4]
EXPECTED_SINGLE_VISITS = [2, 4]


def build_visits() -> ndp.Table:
	"""
	Return a Table of four visits.

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


def test_rows_are_sorted_by_several_keys() -> None:
	"""
	Check a sort by email, then by amount descending, the missing email last.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()
	by_email = ndp.SortKey(column="email")
	by_amount = ndp.SortKey(column="amount", order=ndp.Order.DESCENDING)

	sorted_visits = visits.sort(ndp.Sorting(keys=[by_email, by_amount]))

	visit_numbers = read_visit_numbers(sorted_visits)
	assert visit_numbers == EXPECTED_BY_EMAIL_THEN_AMOUNT


def test_missing_values_can_come_first() -> None:
	"""
	Check an ascending sort of amounts with the missing amount first.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()
	by_amount = ndp.SortKey(column="amount", missing=ndp.MissingPosition.FIRST)

	sorted_visits = visits.sort(ndp.Sorting(keys=[by_amount]))

	visit_numbers = read_visit_numbers(sorted_visits)
	assert visit_numbers == EXPECTED_MISSING_AMOUNT_FIRST


def test_duplicated_emails_keep_the_chosen_visit() -> None:
	"""
	Check the remaining visits when keeping the first, the last, or no duplicated email.

	.. versionadded:: 0.1.0
	"""
	visits = build_visits()

	first_visits = visits.drop_duplicates(ndp.Deduplication(columns=["email"]))
	last_visits = visits.drop_duplicates(ndp.Deduplication(columns=["email"], keep=ndp.Keep.LAST))
	single_visits = visits.drop_duplicates(ndp.Deduplication(columns=["email"], keep=ndp.Keep.NONE))

	first_numbers = read_visit_numbers(first_visits)
	last_numbers = read_visit_numbers(last_visits)
	single_numbers = read_visit_numbers(single_visits)
	assert first_numbers == EXPECTED_FIRST_VISITS
	assert last_numbers == EXPECTED_LAST_VISITS
	assert single_numbers == EXPECTED_SINGLE_VISITS
