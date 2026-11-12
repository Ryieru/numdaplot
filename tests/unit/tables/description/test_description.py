"""
Unit tests of Description.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.duplicate_statistic_error import DuplicateStatisticError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.less import Less
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.share import Share
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.description.description import Description, require_distinct_statistics

COLUMN_NAMES = ["price"]
REPEATED_NAMES = ["price", "price"]
EMPTY_NAMES = list[str]()
EMPTY_FUNCTIONS = list[Statistic]()
SENIOR_SHARE = Share(rule=Greater(65))
CHILD_SHARE = Share(rule=Less(18))
LISTED_CODES = [7, 9]


class UnknownStatistic(Statistic):
	"""
	A statistic numdaplot does not know.

	.. versionadded:: 0.2.0
	"""


def test_description_uses_the_default_functions_and_number_columns() -> None:
	"""
	Check that functions and columns are omitted by default.

	.. versionadded:: 0.1.0
	"""
	description = Description()

	assert description.functions is None
	assert description.columns is None


def test_description_keeps_its_own_copy_of_the_lists() -> None:
	"""
	Check that changing the given lists does not change the description.

	.. versionadded:: 0.1.0
	"""
	functions = list[Statistic]([Min(), Max()])
	column_names = list(COLUMN_NAMES)
	description = Description(functions=functions, columns=column_names)

	functions.clear()
	column_names.clear()

	assert description.functions == [Min(), Max()]
	assert description.columns == COLUMN_NAMES


@pytest.mark.parametrize(
	("functions", "columns"),
	[
		(EMPTY_FUNCTIONS, None),
		(None, EMPTY_NAMES),
	],
)
def test_description_rejects_empty_lists(functions: list[Statistic] | None, columns: list[str] | None) -> None:
	"""
	Check that an empty list of functions or columns raises EmptyListError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	functions
		The statistics.
	columns
		The described columns.
	"""
	with pytest.raises(EmptyListError):
		Description(functions=functions, columns=columns)


def test_description_rejects_a_repeated_column() -> None:
	"""
	Check that a repeated column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		Description(columns=REPEATED_NAMES)


def test_description_rejects_a_statistic_given_twice() -> None:
	"""
	Check that the same statistic twice raises DuplicateStatisticError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateStatisticError):
		Description(functions=[Max(), Min(), Max()])


def test_require_distinct_statistics_accepts_statistics_with_other_settings() -> None:
	"""
	Check that two quantiles of different fractions are distinct.

	.. versionadded:: 0.1.0
	"""
	require_distinct_statistics([Quantile(0.25), Quantile(0.75)])


def test_require_distinct_statistics_rejects_two_shares() -> None:
	"""
	Check that two shares with different rules, giving two rows named share, raise DuplicateStatisticError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(DuplicateStatisticError) as error_info:
		require_distinct_statistics([SENIOR_SHARE, CHILD_SHARE])

	assert error_info.value.statistic == SENIOR_SHARE
	assert error_info.value.other_statistic == CHILD_SHARE


def test_require_distinct_statistics_accepts_a_share_of_listed_values() -> None:
	"""
	Check that a share whose rule holds a list is accepted, although a list cannot be hashed.

	.. versionadded:: 0.2.0
	"""
	listed_share = Share(rule=IsIn(LISTED_CODES))

	require_distinct_statistics([listed_share])


def test_require_distinct_statistics_rejects_an_unknown_statistic() -> None:
	"""
	Check that a statistic numdaplot cannot name raises RefusedOperationError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(RefusedOperationError):
		require_distinct_statistics([UnknownStatistic()])
