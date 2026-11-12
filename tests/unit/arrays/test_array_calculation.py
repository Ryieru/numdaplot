"""
Unit tests of ArrayCalculation.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from typing import Any

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_calculation
from numdaplot.arrays.array_calculation import ArrayCalculation
from numdaplot.arrays.array_data import read_stored_values
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.arrays.math_functions.square_root import SquareRoot
from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.positions.axis import Axis
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.statistic import Statistic

COMPUTE_STATISTIC_NAME = "compute_statistic"
APPLY_MATH_FUNCTION_NAME = "apply_math_function"
GRID = [[1, 4], [9, 16]]
FAKE_RESULT = numpy.array([42.0])
EXPECTED_FAKE_RESULT = [42.0]
APPLY_TIME_FUNCTION_NAME = "apply_time_function"
DATES = numpy.array(["2026-12-31"], dtype="datetime64[D]")


class StatisticRecorder:
	"""
	Fake statistic computation recording the axis it receives.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without recorded axis.

		.. versionadded:: 0.1.0
		"""
		self.axes = list[Axis | None]()

	def compute(self, values: NDArray[Any], statistic: Statistic, axis: Axis | None) -> NDArray[Any]:
		"""
		Record the axis and return a known result.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The values, ignored.
		statistic
			The statistic, ignored.
		axis
			The recorded axis.

		Returns
		-------
		NDArray
			Always the fake result.
		"""
		self.axes.append(axis)

		return FAKE_RESULT


def apply_fake_function(values: NDArray[Any], function: MathFunction) -> NDArray[Any]:
	"""
	Fake math function application returning a known result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, ignored.
	function
		The math function, ignored.

	Returns
	-------
	NDArray
		Always the fake result.
	"""
	return FAKE_RESULT


def test_compute_returns_the_statistic_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that compute returns what the statistic computation gives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the statistic computation with a fake.
	"""
	recorder = StatisticRecorder()
	monkeypatch.setattr(array_calculation, COMPUTE_STATISTIC_NAME, recorder.compute)
	values = numpy.array(GRID)
	array = ArrayCalculation._create(values)

	result_array = array.compute(Mean())

	result_values = read_stored_values(result_array)
	result_list = result_values.tolist()
	assert result_list == EXPECTED_FAKE_RESULT


def test_compute_gives_its_axis_to_the_statistic_computation(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the axis reaches the statistic computation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the statistic computation with a fake recording the axis.
	"""
	recorder = StatisticRecorder()
	monkeypatch.setattr(array_calculation, COMPUTE_STATISTIC_NAME, recorder.compute)
	values = numpy.array(GRID)
	array = ArrayCalculation._create(values)

	array.compute(Mean(), axis=Axis.EACH_COLUMN)

	assert recorder.axes == [Axis.EACH_COLUMN]


def test_apply_returns_the_transformed_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that apply returns what the math function application gives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the math function application with a fake.
	"""
	monkeypatch.setattr(array_calculation, APPLY_MATH_FUNCTION_NAME, apply_fake_function)
	values = numpy.array(GRID)
	array = ArrayCalculation._create(values)

	result_array = array.apply(SquareRoot())

	result_values = read_stored_values(result_array)
	result_list = result_values.tolist()
	assert result_list == EXPECTED_FAKE_RESULT


def apply_fake_time_function(values: NDArray[Any], function: TimeFunction) -> NDArray[Any]:
	"""
	Fake time function application returning a known result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, ignored.
	function
		The time function, ignored.

	Returns
	-------
	NDArray
		Always the fake result.
	"""
	return FAKE_RESULT


def test_apply_hands_a_time_function_to_the_time_function_application(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that apply sends a time function to apply_time_function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the time function application with a fake.
	"""
	monkeypatch.setattr(array_calculation, APPLY_TIME_FUNCTION_NAME, apply_fake_time_function)
	array = ArrayCalculation._create(DATES)

	transformed_array = array.apply(DatePart(unit=DatePartUnit.MONTH))

	transformed_values = read_stored_values(transformed_array)
	transformed_list = transformed_values.tolist()
	assert transformed_list == EXPECTED_FAKE_RESULT
