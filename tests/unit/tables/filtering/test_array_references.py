"""
Unit tests of the rules comparing a Table column with an Array, kept to the rows holding a value.

.. versionadded:: 0.2.0
"""

from typing import cast

import numpy
import pytest

from numdaplot.arrays.array import Array
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.dates.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.positions.shape_mismatch_error import ShapeMismatchError
from numdaplot.rules.between import Between
from numdaplot.rules.contains import Contains
from numdaplot.rules.equal import Equal
from numdaplot.rules.rule import Rule
from numdaplot.tables.filtering.array_references import keep_present_reference, keep_present_rows

ARRIVALS = Array.from_list(["Pau", "Nice", "Dax"])
PRESENT = numpy.array([True, False, True])
EXPECTED_PRESENT_ARRIVALS = ["Pau", "Dax"]
SHORT_PRESENT = numpy.array([True, True])
PARIS_ZONE = TimeZone("Europe/Paris")
TEXT_RULE = Contains("a")
VALUE_RULE = Equal("Pau")
LOWS = Array.from_list([10.0, 15.0, 20.0])
HIGHS = Array.from_list([30.0, 35.0, 40.0])
EXPECTED_PRESENT_LOWS = [10.0, 20.0]
EXPECTED_PRESENT_HIGHS = [30.0, 40.0]


def test_keep_present_reference_keeps_the_rows_holding_a_value() -> None:
	"""
	Check that the Array of the rule keeps the rows where the column holds a value.

	.. versionadded:: 0.2.0
	"""
	present_rule = keep_present_reference(Equal(ARRIVALS), PRESENT, None)

	assert isinstance(present_rule, Equal)
	assert isinstance(present_rule.value, Array)
	present_arrivals = present_rule.value.to_list()
	assert present_arrivals == EXPECTED_PRESENT_ARRIVALS


def test_keep_present_reference_keeps_a_rule_without_array() -> None:
	"""
	Check that a rule comparing with a single value, or a rule without value, is returned as it is.

	.. versionadded:: 0.2.0
	"""
	value_rule = keep_present_reference(VALUE_RULE, PRESENT, None)
	text_rule = keep_present_reference(TEXT_RULE, PRESENT, None)

	assert value_rule is VALUE_RULE
	assert text_rule is TEXT_RULE


def test_keep_present_reference_rejects_an_array_of_another_length() -> None:
	"""
	Check that an Array without one value per row raises ShapeMismatchError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ShapeMismatchError):
		keep_present_reference(Equal(ARRIVALS), SHORT_PRESENT, None)


def test_keep_present_reference_rejects_a_column_with_a_time_zone() -> None:
	"""
	Check that a column of datetimes with a time zone raises TimeZoneMismatchError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(TimeZoneMismatchError):
		keep_present_reference(Equal(ARRIVALS), PRESENT, PARIS_ZONE)


def test_keep_present_reference_keeps_the_rows_of_both_bounds() -> None:
	"""
	Check that both bounds of Between given by Arrays keep the rows holding a value.

	.. versionadded:: 0.2.0
	"""
	present_rule = keep_present_reference(Between(LOWS, HIGHS), PRESENT, None)

	assert isinstance(present_rule, Between)
	between_rule = cast(Between[float], present_rule)
	low_bounds = between_rule.low
	high_bounds = between_rule.high
	assert isinstance(low_bounds, Array)
	assert isinstance(high_bounds, Array)
	present_lows = low_bounds.to_list()
	present_highs = high_bounds.to_list()
	assert present_lows == EXPECTED_PRESENT_LOWS
	assert present_highs == EXPECTED_PRESENT_HIGHS


def test_keep_present_rows_rejects_an_array_of_another_length() -> None:
	"""
	Check that an Array without one value per row raises ShapeMismatchError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ShapeMismatchError):
		keep_present_rows(LOWS, SHORT_PRESENT)


class OwnRule(Rule):
	"""
	A rule written outside numdaplot, which is not a dataclass.

	.. versionadded:: 0.2.0
	"""


def test_keep_present_reference_keeps_a_rule_that_is_not_a_dataclass() -> None:
	"""
	Check that a rule written outside numdaplot is returned as it is, for the refusal that follows.

	.. versionadded:: 0.2.0
	"""
	own_rule = OwnRule()

	kept_rule = keep_present_reference(own_rule, PRESENT, None)

	assert kept_rule is own_rule
