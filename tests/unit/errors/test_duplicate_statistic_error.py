"""
Unit tests of DuplicateStatisticError.

.. versionadded:: 0.2.0
"""

from numdaplot.errors.duplicate_statistic_error import DuplicateStatisticError
from numdaplot.errors.numdaplot_error import NumdaplotError

STATISTIC = "Sum()"
OTHER_STATISTIC = "Mean()"
EXPECTED_MESSAGE = "The statistic 'Sum()' appears more than once."
EXPECTED_SAME_NAME_MESSAGE = (
	"The statistics 'Sum()' and 'Mean()' give rows of the same name. "
	"Use aggregate with a result_name for each, or one description per statistic."
)


def test_duplicate_statistic_error_is_a_numdaplot_error() -> None:
	"""
	Check that DuplicateStatisticError is caught by NumdaplotError.

	.. versionadded:: 0.2.0
	"""
	assert issubclass(DuplicateStatisticError, NumdaplotError)


def test_duplicate_statistic_error_message_names_the_repeated_statistic() -> None:
	"""
	Check the message of a statistic given twice.

	.. versionadded:: 0.2.0
	"""
	error = DuplicateStatisticError(STATISTIC)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.other_statistic is None


def test_duplicate_statistic_error_names_both_statistics_of_the_same_name() -> None:
	"""
	Check the message of two different statistics giving rows of the same name, and the kept values.

	.. versionadded:: 0.2.0
	"""
	error = DuplicateStatisticError(STATISTIC, OTHER_STATISTIC)

	error_text = str(error)
	assert error_text == EXPECTED_SAME_NAME_MESSAGE
	assert error.statistic == STATISTIC
	assert error.other_statistic == OTHER_STATISTIC
