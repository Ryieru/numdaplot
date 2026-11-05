"""
Mask of any rule applied to the values of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.selection.comparison_masks import build_between_mask, build_comparison_mask
from numdaplot.arrays.selection.membership_masks import build_contains_mask, build_membership_mask
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.between import Between
from numdaplot.rules.contains import Contains
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.is_missing import IsMissing
from numdaplot.rules.is_present import IsPresent
from numdaplot.rules.rule import Rule
from numdaplot.rules.value_rule import ValueRule
from numdaplot.settings.setting_types import require_object_not_class

UNKNOWN_RULE_OPERATION = "The rule {rule_name}"
UNKNOWN_RULE_ALTERNATIVE = "a rule of numdaplot"
RULE_SETTING = "rule"
RULE_EXPECTED = "a rule such as ndp.Greater(10)"


def build_rule_mask(values: NDArray[Any], rule: Rule) -> NDArray[numpy.bool_]:
	"""
	Return which values satisfy a rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	rule
		Any rule of numdaplot.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each value satisfying the rule. A missing value only satisfies ``IsMissing``.

	Raises
	------
	InvalidSettingTypeError
		When ``rule`` is a class, written without its parentheses.
	IncompatibleTypesError
		When the rule does not apply to the type of the values.
	RefusedOperationError
		When the rule is not a rule of numdaplot.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.rule_mask import build_rule_mask
	>>> build_rule_mask(numpy.array([1.0, numpy.nan]), ndp.IsPresent())
	array([ True, False])
	"""
	require_object_not_class(RULE_SETTING, RULE_EXPECTED, rule)

	match rule:
		case IsMissing():
			mask = find_missing(values)
		case IsPresent():
			missing = find_missing(values)
			mask = ~missing
		case Contains():
			mask = build_contains_mask(values, rule)
		case IsIn():
			membership_rule = cast(IsIn[Any], rule)
			mask = build_membership_mask(values, membership_rule)
		case Between():
			interval_rule = cast(Between[Any], rule)
			mask = build_between_mask(values, interval_rule)
		case ValueRule():
			comparison_rule = cast(ValueRule[Any], rule)
			mask = build_comparison_mask(values, comparison_rule)
		case _:
			rule_class = type(rule)
			operation = UNKNOWN_RULE_OPERATION.format(rule_name=rule_class.__name__)
			raise RefusedOperationError(operation, UNKNOWN_RULE_ALTERNATIVE)

	return mask
