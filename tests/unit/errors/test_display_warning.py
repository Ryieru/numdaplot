"""
Unit tests of DisplayWarning.

.. versionadded:: 0.1.0
"""

import warnings

from numdaplot.errors.display_warning import DisplayWarning
from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.numdaplot_warning import NumdaplotWarning

MESSAGE = "No window can be opened, matplotlib has no graphical backend here."


def test_display_warning_is_a_user_warning() -> None:
	"""
	Check that DisplayWarning is filtered like any warning meant for users.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(DisplayWarning, UserWarning)


def test_display_warning_is_not_an_error() -> None:
	"""
	Check that catching NumdaplotError never catches the warning.

	.. versionadded:: 0.1.0
	"""
	assert not issubclass(DisplayWarning, NumdaplotError)


def test_display_warning_can_be_silenced() -> None:
	"""
	Check that the warnings module silences it.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("ignore", DisplayWarning)
		warnings.warn(MESSAGE, DisplayWarning, stacklevel=1)

	assert caught_warnings == []


def test_display_warning_is_a_numdaplot_warning() -> None:
	"""
	Check that DisplayWarning inherits NumdaplotWarning.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(DisplayWarning, NumdaplotWarning)
