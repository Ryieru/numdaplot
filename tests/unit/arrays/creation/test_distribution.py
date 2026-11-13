"""
Unit tests of Distribution.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.arrays.creation.uniform import Uniform
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError


class CustomDistribution(Distribution):
	"""
	A Distribution written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


def test_distribution_refuses_its_own_creation() -> None:
	"""
	Check that creating the base class itself raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		Distribution()


def test_distribution_lets_a_subclass_of_numdaplot_be_created() -> None:
	"""
	Check that a subclass of numdaplot is created.

	.. versionadded:: 0.1.0
	"""
	created = Uniform(low=0, high=1)

	assert isinstance(created, Distribution)


def test_distribution_lets_a_subclass_written_outside_numdaplot_be_created() -> None:
	"""
	Check that a subclass without its own constructor is created.

	.. versionadded:: 0.1.0
	"""
	created = CustomDistribution()

	assert isinstance(created, Distribution)
