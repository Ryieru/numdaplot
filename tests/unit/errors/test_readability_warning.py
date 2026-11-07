"""
Unit tests of ReadabilityWarning.

.. versionadded:: 0.1.0
"""

import warnings

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.numdaplot_warning import NumdaplotWarning
from numdaplot.errors.readability_warning import ReadabilityWarning

MESSAGE = "A PieChart with 6 slices is hard to read."


def test_readability_warning_is_a_user_warning() -> None:
	"""
	Check that ReadabilityWarning is filtered like any warning meant for users.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ReadabilityWarning, UserWarning)


def test_readability_warning_is_not_an_error() -> None:
	"""
	Check that catching NumdaplotError never catches the warning.

	.. versionadded:: 0.1.0
	"""
	assert not issubclass(ReadabilityWarning, NumdaplotError)


def test_readability_warning_can_be_silenced() -> None:
	"""
	Check that the warnings module silences it.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("ignore", ReadabilityWarning)
		warnings.warn(MESSAGE, ReadabilityWarning, stacklevel=1)

	assert caught_warnings == []


def test_readability_warning_is_a_numdaplot_warning() -> None:
	"""
	Check that ReadabilityWarning inherits NumdaplotWarning.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ReadabilityWarning, NumdaplotWarning)
