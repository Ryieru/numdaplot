"""
Unit tests of the values whose mean is a share.

.. versionadded:: 0.2.0
"""

import numpy

from numdaplot.arrays.statistics.share_values import build_share_values, mark_share_values
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_missing import IsMissing
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.share import Share

AGES = numpy.array([70.0, numpy.nan, 30.0])
SENIOR_AGE = 65
EXPECTED_MISSING_POSITIONS = [False, True, False]
EXPECTED_PRESENT_SHARE_VALUES = [1.0, 0.0]
EXPECTED_MISSING_SHARE_VALUES = [0.0, 1.0, 0.0]
MATCHES = numpy.array([True, False, False])
MISSING = numpy.array([False, True, False])
EXPECTED_EVERY_SHARE_VALUES = [1.0, 0.0, 0.0]


def test_build_share_values_marks_the_matches_and_leaves_out_missing_values() -> None:
	"""
	Check 1 for a match, 0 otherwise, and NaN for a missing value.

	.. versionadded:: 0.2.0
	"""
	share_values = build_share_values(AGES, Share(rule=Greater(SENIOR_AGE)))

	missing_positions = numpy.isnan(share_values)
	present_values = share_values[~missing_positions]
	missing_list = missing_positions.tolist()
	present_list = present_values.tolist()
	assert missing_list == EXPECTED_MISSING_POSITIONS
	assert present_list == EXPECTED_PRESENT_SHARE_VALUES


def test_build_share_values_matches_missing_values_with_is_missing() -> None:
	"""
	Check that IsMissing marks the missing value as a match when missing values count.

	.. versionadded:: 0.2.0
	"""
	share = Share(rule=IsMissing(), missing=CountedMissing.INCLUDED)

	share_values = build_share_values(AGES, share)

	share_list = share_values.tolist()
	assert share_list == EXPECTED_MISSING_SHARE_VALUES


def test_mark_share_values_keeps_every_value_when_missing_values_count() -> None:
	"""
	Check that a missing value counts as 0 when missing values are included.

	.. versionadded:: 0.2.0
	"""
	share_values = mark_share_values(MATCHES, MISSING, CountedMissing.INCLUDED)

	share_list = share_values.tolist()
	assert share_list == EXPECTED_EVERY_SHARE_VALUES
