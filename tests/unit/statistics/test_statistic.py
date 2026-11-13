"""
Unit tests of Statistic.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.statistic import Statistic


class CustomStatistic(Statistic):
	"""
	A Statistic written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


def test_statistic_refuses_its_own_creation() -> None:
	"""
	Check that creating the base class itself raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		Statistic()


def test_statistic_lets_a_subclass_of_numdaplot_be_created() -> None:
	"""
	Check that a subclass of numdaplot is created.

	.. versionadded:: 0.1.0
	"""
	created = Mean()

	assert isinstance(created, Statistic)


def test_statistic_lets_a_subclass_written_outside_numdaplot_be_created() -> None:
	"""
	Check that a subclass without its own constructor is created.

	.. versionadded:: 0.1.0
	"""
	created = CustomStatistic()

	assert isinstance(created, Statistic)
