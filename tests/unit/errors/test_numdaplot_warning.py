"""
Unit tests of NumdaplotWarning.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.numdaplot_warning import NumdaplotWarning


def test_numdaplot_warning_is_a_standard_user_warning() -> None:
	"""
	Check that NumdaplotWarning is a standard user warning, so filters on UserWarning still apply.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(NumdaplotWarning, UserWarning)


def test_numdaplot_warning_is_not_an_error() -> None:
	"""
	Check that catching NumdaplotError never catches a numdaplot warning.

	.. versionadded:: 0.1.0
	"""
	assert not issubclass(NumdaplotWarning, NumdaplotError)
