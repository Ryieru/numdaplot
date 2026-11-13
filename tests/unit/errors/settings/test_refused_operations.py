"""
Unit tests of the refusal of the comparison operators.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.errors.settings.refused_operations import LESS_SYMBOL, refuse_comparison

OWNER = "an Array"
ALTERNATIVE = "select"
EXPECTED_COMPARISON_MESSAGE = "Comparing an Array with < is not available, use select instead."


def test_refuse_comparison_names_the_owner_the_operator_and_the_alternative() -> None:
	"""
	Check the message of a refused comparison.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(RefusedOperationError) as error_information:
		refuse_comparison(OWNER, LESS_SYMBOL, ALTERNATIVE)

	error_text = str(error_information.value)
	assert error_text == EXPECTED_COMPARISON_MESSAGE
