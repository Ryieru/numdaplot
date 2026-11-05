"""
Unit tests of the warnings about values becoming NaN or an infinite value.

.. versionadded:: 0.1.0
"""

import warnings

import numpy
import pytest

from numdaplot.arrays.operations.float_errors import FloatErrorWarnings
from numdaplot.errors.calculation_warning import CalculationWarning

OPERATION_NAME = "/"
ZEROS = numpy.array([0.0])
ONES = numpy.array([1.0])
SMALLEST_DECIMALS = numpy.array([1e-308])


def test_float_error_warnings_warns_once_per_kind() -> None:
	"""
	Check that two kinds of errors in a block give two warnings.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		with FloatErrorWarnings(OPERATION_NAME):
			numpy.true_divide(ZEROS, ZEROS)
			numpy.true_divide(ONES, ZEROS)
			numpy.true_divide(ONES, ZEROS)

	assert len(caught_warnings) == 2


def test_float_error_warnings_points_at_the_calling_file() -> None:
	"""
	Check that the warning skips the files of the package.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		with FloatErrorWarnings(OPERATION_NAME):
			numpy.true_divide(ZEROS, ZEROS)

	assert caught_warnings[0].filename == __file__


def test_float_error_warnings_stays_silent_without_error() -> None:
	"""
	Check that a regular calculation gives no warning.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		with FloatErrorWarnings(OPERATION_NAME):
			numpy.true_divide(ONES, ONES)

	assert caught_warnings == []


def test_float_error_warnings_ignores_underflow() -> None:
	"""
	Check that a value too small for its type, which becomes 0, is not reported.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		with FloatErrorWarnings(OPERATION_NAME):
			numpy.multiply(SMALLEST_DECIMALS, SMALLEST_DECIMALS)

	assert caught_warnings == []


def test_float_error_warnings_does_not_warn_when_the_block_raises() -> None:
	"""
	Check that the error of the block is the only signal.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		with pytest.raises(ValueError), FloatErrorWarnings(OPERATION_NAME):
			numpy.true_divide(ZEROS, ZEROS)
			raise ValueError(OPERATION_NAME)

	assert not any(caught_warning.category is CalculationWarning for caught_warning in caught_warnings)
