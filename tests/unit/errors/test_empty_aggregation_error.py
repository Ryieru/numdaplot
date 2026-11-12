"""
Unit tests of EmptyAggregationError.

.. versionadded:: 0.2.0
"""

from numdaplot.errors.empty_aggregation_error import EMPTY_AGGREGATION_MESSAGE, EmptyAggregationError
from numdaplot.errors.numdaplot_error import NumdaplotError


def test_empty_aggregation_error_is_a_numdaplot_error() -> None:
	"""
	Check that EmptyAggregationError is caught by NumdaplotError.

	.. versionadded:: 0.2.0
	"""
	assert issubclass(EmptyAggregationError, NumdaplotError)


def test_empty_aggregation_error_explains_that_rows_or_columns_are_needed() -> None:
	"""
	Check the message of the error.

	.. versionadded:: 0.2.0
	"""
	error = EmptyAggregationError()

	error_text = str(error)
	assert error_text == EMPTY_AGGREGATION_MESSAGE
