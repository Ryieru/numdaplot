"""
Unit tests of build_rule_mask.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.rules import rule_mask
from numdaplot.arrays.rules.rule_mask import build_rule_mask
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.between import Between
from numdaplot.rules.contains import Contains
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.is_missing import IsMissing
from numdaplot.rules.is_present import IsPresent
from numdaplot.rules.rule import Rule

DECIMALS = [1.0, numpy.nan]
EXPECTED_MISSING_MASK = [False, True]
EXPECTED_PRESENT_MASK = [True, False]
DISPATCHED_RULES = [
	(Greater(1), "build_comparison_mask"),
	(Between(low=1, high=2), "build_between_mask"),
	(IsIn([1]), "build_membership_mask"),
	(Contains("a"), "build_contains_mask"),
]
FAKE_MASK = numpy.array([True, True])
EXPECTED_FAKE_MASK = [True, True]


class UnknownRule(Rule):
	"""
	A rule numdaplot does not know.

	.. versionadded:: 0.1.0
	"""


def test_build_rule_mask_finds_missing_values() -> None:
	"""
	Check that IsMissing keeps the missing values.

	.. versionadded:: 0.1.0
	"""
	decimals = numpy.array(DECIMALS)

	mask = build_rule_mask(decimals, IsMissing())

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_MISSING_MASK


def test_build_rule_mask_finds_present_values() -> None:
	"""
	Check that IsPresent keeps the present values.

	.. versionadded:: 0.1.0
	"""
	decimals = numpy.array(DECIMALS)

	mask = build_rule_mask(decimals, IsPresent())

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_PRESENT_MASK


@pytest.mark.parametrize(("rule", "builder_name"), DISPATCHED_RULES)
def test_build_rule_mask_hands_each_rule_to_its_builder(
	monkeypatch: pytest.MonkeyPatch, rule: Rule, builder_name: str
) -> None:
	"""
	Check that each kind of rule is handed to the function building its mask.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the builder with a fake returning a known mask.
	rule
		A rule.
	builder_name
		The name of the function expected to build its mask.
	"""
	monkeypatch.setattr(rule_mask, builder_name, build_fake_mask)
	decimals = numpy.array(DECIMALS)

	mask = build_rule_mask(decimals, rule)

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_FAKE_MASK


def test_build_rule_mask_refuses_an_unknown_rule() -> None:
	"""
	Check that a rule outside numdaplot raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	decimals = numpy.array(DECIMALS)

	with pytest.raises(RefusedOperationError):
		build_rule_mask(decimals, UnknownRule())


def build_fake_mask(values: NDArray[Any], rule: Rule) -> NDArray[numpy.bool_]:
	"""
	Fake mask builder returning True everywhere.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, ignored.
	rule
		The rule, ignored.

	Returns
	-------
	NDArray[numpy.bool_]
		Always two True values.
	"""
	return FAKE_MASK
