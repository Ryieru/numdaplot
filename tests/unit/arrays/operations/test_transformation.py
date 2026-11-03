"""
Unit tests of transform_values.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.operations.transformation import transform_values
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError

NEGATION_SYMBOL = "-"
VALUES = [1, -2]
EXPECTED_NEGATED_VALUES = [-1, 2]
BOOLEANS = [True]


def test_transform_values_applies_the_function_to_each_value() -> None:
	"""
	Check that each value is negated.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(VALUES)

	transformed_values = transform_values(values, numpy.negative, NEGATION_SYMBOL)

	transformed_list = transformed_values.tolist()
	assert transformed_list == EXPECTED_NEGATED_VALUES


def test_transform_values_rejects_a_function_not_applying_to_the_type() -> None:
	"""
	Check that negating booleans raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	booleans = numpy.array(BOOLEANS)

	with pytest.raises(IncompatibleTypesError):
		transform_values(booleans, numpy.negative, NEGATION_SYMBOL)
