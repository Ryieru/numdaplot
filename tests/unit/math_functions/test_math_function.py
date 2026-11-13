"""
Unit tests of MathFunction.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.math_functions.math_function import MathFunction
from numdaplot.math_functions.square_root import SquareRoot


class CustomMathFunction(MathFunction):
	"""
	A MathFunction written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


def test_math_function_refuses_its_own_creation() -> None:
	"""
	Check that creating the base class itself raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		MathFunction()


def test_math_function_lets_a_subclass_of_numdaplot_be_created() -> None:
	"""
	Check that a subclass of numdaplot is created.

	.. versionadded:: 0.1.0
	"""
	created = SquareRoot()

	assert isinstance(created, MathFunction)


def test_math_function_lets_a_subclass_written_outside_numdaplot_be_created() -> None:
	"""
	Check that a subclass without its own constructor is created.

	.. versionadded:: 0.1.0
	"""
	created = CustomMathFunction()

	assert isinstance(created, MathFunction)
