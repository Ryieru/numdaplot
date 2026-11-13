"""
Unit tests of the column whose mean is a share.

.. versionadded:: 0.2.0
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas
import pytest

from numdaplot.column_storage.time_zones import normalize_time_zone_column
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.between import Between
from numdaplot.rules.greater import Greater
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.share import Share
from numdaplot.tables.aggregation.share_column import build_share_column

AGES = pandas.Series([70, None, 30], dtype="Int64")
SENIOR_AGE = 65
EXPECTED_MISSING_ROWS = [False, True, False]
EXPECTED_PRESENT_SHARE_VALUES = [1.0, 0.0]
EXPECTED_EVERY_SHARE_VALUES = [1.0, 0.0, 0.0]
CITIES = pandas.Series(["Pau", "Lyon"], dtype="string")
PARIS = ZoneInfo("Europe/Paris")
VISIT_TEXTS = pandas.Series(["2026-07-01 10:30", "2026-07-02 08:00"])
NAIVE_TIMES = pandas.to_datetime(VISIT_TEXTS)
PARIS_TIMES = NAIVE_TIMES.dt.tz_localize(PARIS)
NOON = datetime(2026, 7, 1, 12, 0, tzinfo=PARIS)
EXPECTED_TIME_SHARE_VALUES = [0.0, 1.0]


def test_build_share_column_leaves_out_missing_values_by_default() -> None:
	"""
	Check 1 for a match, 0 otherwise, and a missing value where the column has one.

	.. versionadded:: 0.2.0
	"""
	share_column = build_share_column(AGES, Share(rule=Greater(SENIOR_AGE)))

	missing_rows = share_column.isna()
	present_values = share_column.dropna()
	missing_list = missing_rows.tolist()
	present_list = present_values.tolist()
	assert missing_list == EXPECTED_MISSING_ROWS
	assert present_list == EXPECTED_PRESENT_SHARE_VALUES


def test_build_share_column_counts_missing_values_as_not_matching() -> None:
	"""
	Check that a missing value gives 0 when missing values count.

	.. versionadded:: 0.2.0
	"""
	share = Share(rule=Greater(SENIOR_AGE), missing=CountedMissing.INCLUDED)

	share_column = build_share_column(AGES, share)

	share_list = share_column.tolist()
	assert share_list == EXPECTED_EVERY_SHARE_VALUES


def test_build_share_column_compares_datetimes_in_the_time_zone_of_the_column() -> None:
	"""
	Check that a rule with a time zone is applied to a column with a time zone.

	.. versionadded:: 0.2.0
	"""
	stored_times = normalize_time_zone_column(PARIS_TIMES)

	share_column = build_share_column(stored_times, Share(rule=Greater(NOON)))

	share_list = share_column.tolist()
	assert share_list == EXPECTED_TIME_SHARE_VALUES


def test_build_share_column_rejects_a_rule_not_applying_to_the_column() -> None:
	"""
	Check that a number interval on texts raises IncompatibleTypesError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(IncompatibleTypesError):
		build_share_column(CITIES, Share(rule=Between(1, 2)))
