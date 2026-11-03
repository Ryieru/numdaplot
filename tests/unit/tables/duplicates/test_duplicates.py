"""
Unit tests of Deduplication and the removal of duplicated rows.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.tables.duplicates.deduplicated_frame import drop_duplicate_rows
from numdaplot.tables.duplicates.deduplication import Deduplication
from numdaplot.tables.duplicates.keep import Keep

VISITS = pandas.DataFrame(
	{
		"email": pandas.Series(["a@x.fr", "b@x.fr", "a@x.fr", None, None], dtype="string"),
		"visit": [1, 2, 3, 4, 5],
	}
)
EXPECTED_FIRST_VISITS = [1, 2, 4]
EXPECTED_LAST_VISITS = [2, 3, 5]
EXPECTED_SINGLE_VISITS = [2]
EXPECTED_EVERY_VISIT = [1, 2, 3, 4, 5]
EMPTY_NAMES = list[str]()
REPEATED_NAMES = ["email", "email"]


def read_visits(frame: pandas.DataFrame) -> list[int]:
	"""
	Return the visit column of the remaining rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The remaining rows.

	Returns
	-------
	list[int]
		The visit of each row.
	"""
	visit_column = frame["visit"]
	visits = visit_column.tolist()

	return visits


def test_deduplication_compares_every_column_and_keeps_the_first_row_by_default() -> None:
	"""
	Check the default columns and kept row.

	.. versionadded:: 0.1.0
	"""
	deduplication = Deduplication()

	assert deduplication.columns is None
	assert deduplication.keep == Keep.FIRST


def test_deduplication_rejects_an_empty_list_of_columns() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Deduplication(columns=EMPTY_NAMES)


def test_deduplication_rejects_a_repeated_column() -> None:
	"""
	Check that a repeated column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		Deduplication(columns=REPEATED_NAMES)


@pytest.mark.parametrize(
	("keep", "expected_visits"),
	[
		(Keep.FIRST, EXPECTED_FIRST_VISITS),
		(Keep.LAST, EXPECTED_LAST_VISITS),
		(Keep.NONE, EXPECTED_SINGLE_VISITS),
	],
)
def test_drop_duplicate_rows_keeps_the_chosen_row_and_treats_missing_values_as_equal(
	keep: Keep,
	expected_visits: list[int],
) -> None:
	"""
	Check the remaining visits for each kept row; the two missing emails are duplicates.

	.. versionadded:: 0.1.0

	Parameters
	----------
	keep
		The kept row of each group.
	expected_visits
		The remaining visits.
	"""
	deduplication = Deduplication(columns=["email"], keep=keep)

	remaining_frame = drop_duplicate_rows(VISITS, deduplication)

	visits = read_visits(remaining_frame)
	assert visits == expected_visits


def test_drop_duplicate_rows_compares_every_column_by_default() -> None:
	"""
	Check that no row is a duplicate when every column is compared.

	.. versionadded:: 0.1.0
	"""
	remaining_frame = drop_duplicate_rows(VISITS, Deduplication())

	visits = read_visits(remaining_frame)
	assert visits == EXPECTED_EVERY_VISIT


def test_drop_duplicate_rows_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	deduplication = Deduplication(columns=["mail"])

	with pytest.raises(ColumnNotFoundError):
		drop_duplicate_rows(VISITS, deduplication)
