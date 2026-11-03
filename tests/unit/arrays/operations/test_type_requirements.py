"""
Unit tests of require_family and require_comparable.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

from numdaplot.arrays.operations.type_requirements import require_comparable, require_family
from numdaplot.data_types.value_family import ValueFamily
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError

OPERATION = "Mean"
NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})
INTEGERS = [1, 2]
TEXTS = ["a", "b"]
TEXT_DTYPE = "T"
DECIMAL_REFERENCE = 1.5
TEXT_REFERENCE = "a"
DATETIMES = numpy.array(["2026-01-31T08:00"], dtype="datetime64[ns]")
DAY_REFERENCE = date(2026, 1, 31)
EXPECTED_MESSAGE = "Cannot apply Mean to TEXT."


def test_require_family_accepts_values_of_an_accepted_family() -> None:
	"""
	Check that integers are accepted as numbers.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)

	require_family(integers, NUMBER_FAMILIES, OPERATION)


def test_require_family_rejects_values_of_another_family() -> None:
	"""
	Check that texts are rejected where numbers are expected, naming the type.

	.. versionadded:: 0.1.0
	"""
	texts = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	with pytest.raises(IncompatibleTypesError, match=EXPECTED_MESSAGE):
		require_family(texts, NUMBER_FAMILIES, OPERATION)


def test_require_comparable_accepts_a_decimal_for_integers() -> None:
	"""
	Check that integers can be compared with a decimal.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)

	require_comparable(integers, DECIMAL_REFERENCE, OPERATION)


def test_require_comparable_accepts_a_date_for_datetimes() -> None:
	"""
	Check that datetimes can be compared with a date.

	.. versionadded:: 0.1.0
	"""
	require_comparable(DATETIMES, DAY_REFERENCE, OPERATION)


def test_require_comparable_rejects_a_text_for_integers() -> None:
	"""
	Check that integers cannot be compared with a text.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)

	with pytest.raises(IncompatibleTypesError):
		require_comparable(integers, TEXT_REFERENCE, OPERATION)
