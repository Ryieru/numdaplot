"""
Unit tests of Rule.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.rules.greater import Greater
from numdaplot.rules.rule import Rule


class CustomRule(Rule):
	"""
	A Rule written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


def test_rule_refuses_its_own_creation() -> None:
	"""
	Check that creating the base class itself raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		Rule()


def test_rule_lets_a_subclass_of_numdaplot_be_created() -> None:
	"""
	Check that a subclass of numdaplot is created.

	.. versionadded:: 0.1.0
	"""
	created = Greater(10)

	assert isinstance(created, Rule)


def test_rule_lets_a_subclass_written_outside_numdaplot_be_created() -> None:
	"""
	Check that a subclass without its own constructor is created.

	.. versionadded:: 0.1.0
	"""
	created = CustomRule()

	assert isinstance(created, Rule)
