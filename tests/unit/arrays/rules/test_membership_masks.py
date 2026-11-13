"""
Unit tests of build_membership_mask and build_contains_mask.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime

import numpy
import pytest

from numdaplot.arrays.rules.membership_masks import build_contains_mask, build_membership_mask
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.case import Case
from numdaplot.rules.contains import Contains
from numdaplot.rules.is_in import IsIn
from numdaplot.types.numpy_mapping import to_numpy_dtype
from numdaplot.types.type import Type

TEXT_DTYPE = "T"
COUNTRIES = ["FR", "DE", "IT"]
ACCEPTED_COUNTRIES = IsIn(["FR", "IT"])
EXPECTED_COUNTRY_MASK = [True, False, True]
DECIMALS = [1.0, numpy.nan]
ACCEPTED_DECIMALS = IsIn([1.0])
EXPECTED_DECIMAL_MASK = [True, False]
NUMBER_RULE = IsIn([1])
CITIES = ["Paris", "Lyon", "PARIS"]
SENSITIVE_RULE = Contains("Par")
IGNORED_CASE_RULE = Contains("par", case=Case.IGNORED)
EXPECTED_SENSITIVE_MASK = [True, False, False]
EXPECTED_IGNORED_CASE_MASK = [True, False, True]
INTEGERS = [1, 2]
DATETIMES = numpy.array(["2026-07-01T08:30", "NaT"], dtype="datetime64[ns]")
ACCEPTED_MOMENTS = IsIn([datetime(2026, 7, 1, 8, 30), date(2026, 1, 1)])
EXPECTED_MOMENT_MATCHES = [True, False]


def test_build_membership_mask_keeps_accepted_values() -> None:
	"""
	Check that the accepted texts are found.

	.. versionadded:: 0.1.0
	"""
	countries = numpy.array(COUNTRIES, dtype=TEXT_DTYPE)

	mask = build_membership_mask(countries, ACCEPTED_COUNTRIES)

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_COUNTRY_MASK


def test_build_membership_mask_never_accepts_a_missing_value() -> None:
	"""
	Check that NaN is not accepted.

	.. versionadded:: 0.1.0
	"""
	decimals = numpy.array(DECIMALS)

	mask = build_membership_mask(decimals, ACCEPTED_DECIMALS)

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_DECIMAL_MASK


def test_build_membership_mask_rejects_incomparable_values() -> None:
	"""
	Check that texts cannot be looked for among numbers.

	.. versionadded:: 0.1.0
	"""
	countries = numpy.array(COUNTRIES, dtype=TEXT_DTYPE)

	with pytest.raises(IncompatibleTypesError):
		build_membership_mask(countries, NUMBER_RULE)


def test_build_contains_mask_distinguishes_case_by_default() -> None:
	"""
	Check that a sensitive search does not match a different case.

	.. versionadded:: 0.1.0
	"""
	cities = numpy.array(CITIES, dtype=TEXT_DTYPE)

	mask = build_contains_mask(cities, SENSITIVE_RULE)

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_SENSITIVE_MASK


def test_build_contains_mask_can_ignore_case() -> None:
	"""
	Check that an insensitive search matches every case.

	.. versionadded:: 0.1.0
	"""
	cities = numpy.array(CITIES, dtype=TEXT_DTYPE)

	mask = build_contains_mask(cities, IGNORED_CASE_RULE)

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_IGNORED_CASE_MASK


def test_build_contains_mask_rejects_numbers() -> None:
	"""
	Check that Contains only applies to texts.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)

	with pytest.raises(IncompatibleTypesError):
		build_contains_mask(integers, SENSITIVE_RULE)


def test_build_membership_mask_finds_datetimes() -> None:
	"""
	Check that a datetime of the list matches the same datetime, and a missing value matches nothing.

	.. versionadded:: 0.1.0
	"""
	mask = build_membership_mask(DATETIMES, ACCEPTED_MOMENTS)

	matches = mask.tolist()
	assert matches == EXPECTED_MOMENT_MATCHES


def test_build_contains_mask_leaves_out_a_missing_text() -> None:
	"""
	Check that a missing text contains nothing, without error.

	.. versionadded:: 0.1.0
	"""
	text_dtype = to_numpy_dtype(Type.TEXT)
	texts = numpy.array(["Paris", numpy.nan], dtype=text_dtype)

	mask = build_contains_mask(texts, IGNORED_CASE_RULE)

	assert mask.tolist() == [True, False]
