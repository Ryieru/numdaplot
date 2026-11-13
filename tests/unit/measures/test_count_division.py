"""
Unit tests of the division of counts into fractions.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.measures.count_division import divide_counts

COUNTS = numpy.array([1, 3], dtype=numpy.int64)
VALUE_COUNT = 4
EXPECTED_RATIOS = [0.25, 0.75]
NO_VALUE = 0


def test_divide_counts_gives_the_fraction_of_each_count() -> None:
	"""
	Check the division by the number of values.

	.. versionadded:: 0.1.0
	"""
	ratios = divide_counts(COUNTS, VALUE_COUNT)

	ratio_list = ratios.tolist()
	assert ratio_list == EXPECTED_RATIOS


def test_divide_counts_gives_nan_without_any_value() -> None:
	"""
	Check that a division by no value gives NaN instead of an error.

	.. versionadded:: 0.1.0
	"""
	ratios = divide_counts(COUNTS, NO_VALUE)

	nan_ratios = numpy.isnan(ratios)
	is_nan = bool(nan_ratios.all())
	assert is_nan
