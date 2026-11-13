"""
Unit tests of InvalidSeedError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.invalid_seed_error import InvalidSeedError

SEED = -1
EXPECTED_MESSAGE = "Expected a seed of at least 0, got -1."


def test_invalid_seed_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidSeedError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidSeedError, NumdaplotError)


def test_invalid_seed_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSeedError(SEED)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_seed_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSeedError(SEED)

	assert error.seed == SEED
