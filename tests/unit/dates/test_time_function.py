"""
Unit tests of TimeFunction.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.errors.refused_operation_error import RefusedOperationError


class CustomTimeFunction(TimeFunction):
	"""
	A TimeFunction written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


def test_time_function_refuses_its_own_creation() -> None:
	"""
	Check that creating the base class itself raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		TimeFunction()


def test_time_function_lets_a_subclass_of_numdaplot_be_created() -> None:
	"""
	Check that a subclass of numdaplot is created.

	.. versionadded:: 0.1.0
	"""
	created = DatePart(unit=DatePartUnit.MONTH)

	assert isinstance(created, TimeFunction)


def test_time_function_lets_a_subclass_written_outside_numdaplot_be_created() -> None:
	"""
	Check that a subclass without its own constructor is created.

	.. versionadded:: 0.1.0
	"""
	created = CustomTimeFunction()

	assert isinstance(created, TimeFunction)
