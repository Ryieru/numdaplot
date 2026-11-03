"""
Unit tests of ArrayCalculation.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_calculation
from numdaplot.arrays.array_calculation import ArrayCalculation
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.arrays.math_functions.square_root import SquareRoot
from numdaplot.positions.axis import Axis
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.statistic import Statistic

COMPUTE_STATISTIC_NAME = "compute_statistic"
APPLY_MATH_FUNCTION_NAME = "apply_math_function"
GRID = [[1, 4], [9, 16]]
FAKE_RESULT = numpy.array([42.0])
EXPECTED_FAKE_RESULT = [42.0]


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
	array = ArrayCalculation(values)

	result_array = array.compute(Mean())

	result_values = result_array.to_numpy()
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
	array = ArrayCalculation(values)

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
	array = ArrayCalculation(values)

	result_array = array.apply(SquareRoot())

	result_values = result_array.to_numpy()
	result_list = result_values.tolist()
	assert result_list == EXPECTED_FAKE_RESULT
