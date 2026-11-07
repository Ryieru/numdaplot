"""
Unit tests of DateParts.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.arrays.creation.date_parts import DateParts
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError

YEARS = ndp.Array.from_list([2025, 2026])
MONTHS = ndp.Array.from_list([3, 12])
DAYS = ndp.Array.from_list([15, 31])
TEXT_MONTHS = ndp.Array.from_list(["mars", "decembre"])
ONE_DAY = ndp.Array.from_list([15])


def test_date_parts_keep_their_arrays() -> None:
	"""
	Check that the three parts are available as attributes.

	.. versionadded:: 0.1.0
	"""
	parts = DateParts(year=YEARS, month=MONTHS, day=DAYS)

	assert parts.year is YEARS
	assert parts.month is MONTHS
	assert parts.day is DAYS


def test_date_parts_reject_a_part_of_texts() -> None:
	"""
	Check that a month written as texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		DateParts(year=YEARS, month=TEXT_MONTHS, day=DAYS)


def test_date_parts_reject_parts_of_different_shapes() -> None:
	"""
	Check that a day Array of another shape raises ShapeMismatchError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ShapeMismatchError):
		DateParts(year=YEARS, month=MONTHS, day=ONE_DAY)
