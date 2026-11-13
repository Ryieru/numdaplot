"""
Unit tests of require_booleans.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.operations.boolean_operands import require_booleans
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError

AND_SYMBOL = "&"
BOOLEANS = [True, False]
INTEGERS = [1, 0]


def test_require_booleans_accepts_boolean_arrays_and_values() -> None:
	"""
	Check that a boolean array and a boolean are accepted.

	.. versionadded:: 0.1.0
	"""
	booleans = numpy.array(BOOLEANS)

	require_booleans([booleans, True], AND_SYMBOL)


def test_require_booleans_rejects_integers() -> None:
	"""
	Check that integers, whose bits numpy would combine, are rejected.

	.. versionadded:: 0.1.0
	"""
	booleans = numpy.array(BOOLEANS)
	integers = numpy.array(INTEGERS)

	with pytest.raises(IncompatibleTypesError):
		require_booleans([booleans, integers], AND_SYMBOL)
