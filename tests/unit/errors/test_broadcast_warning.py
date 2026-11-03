"""
Unit tests of BroadcastWarning.

.. versionadded:: 0.1.0
"""

import warnings

from numdaplot.errors.broadcast_warning import BroadcastWarning

WARNING_MESSAGE = "Shapes differ."


def test_broadcast_warning_is_a_user_warning() -> None:
	"""
	Check that BroadcastWarning is a standard user warning.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(BroadcastWarning, UserWarning)


def test_broadcast_warning_is_silenced_by_the_warnings_module() -> None:
	"""
	Check that an ignore filter on BroadcastWarning stops it from being recorded.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as recorded_warnings:
		warnings.simplefilter("ignore", category=BroadcastWarning)
		warnings.warn(WARNING_MESSAGE, category=BroadcastWarning, stacklevel=1)

	assert recorded_warnings == []
