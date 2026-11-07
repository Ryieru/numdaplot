"""
Unit tests of CalculationWarning.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.calculation_warning import CalculationWarning
from numdaplot.errors.numdaplot_warning import NumdaplotWarning


def test_calculation_warning_is_a_standard_user_warning() -> None:
	"""
	Check that CalculationWarning is a standard user warning.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(CalculationWarning, UserWarning)


def test_calculation_warning_is_a_numdaplot_warning() -> None:
	"""
	Check that CalculationWarning inherits NumdaplotWarning.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(CalculationWarning, NumdaplotWarning)
