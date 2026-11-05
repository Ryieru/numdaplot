"""
Unit tests of CalculationWarning.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.calculation_warning import CalculationWarning


def test_calculation_warning_is_a_standard_user_warning() -> None:
	"""
	Check that CalculationWarning is a standard user warning.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(CalculationWarning, UserWarning)
