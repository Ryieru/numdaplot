"""
Base class of the rules that compare each value to a single reference value.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from typing import ClassVar, cast

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.rule import Rule
from numdaplot.settings.field_types import require_field_types

MISSING_VALUE_OPERATION = "{rule_name}(None)"


@dataclass(frozen=True)
class ValueRule[ReferenceValue](Rule):
	"""
	Base class of the rules comparing each value to a reference value, or to the value at its position in an Array.

	Two rules are equal only when they have the same class and the same reference value,
	so ``Greater(1)`` and ``Less(1)`` are different.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The rules comparing values accept an Array as reference value.

	Parameters
	----------
	value
		The reference value each tested value is compared to, or an Array of them, one per tested value.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	RefusedOperationError
		When ``value`` is None for a rule with a rule of its own for missing values, such as ``Equal(None)``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> limit = ndp.Greater(100)
	>>> limit.value
	100
	>>> ndp.Array.from_list([80, 120]).select(limit)
	Array([120], dtype=INT64)
	"""

	# The rule testing missing values, used in place of this rule when it is given None.
	MISSING_VALUE_RULE: ClassVar[str | None] = None

	value: ReferenceValue

	def __post_init__(self) -> None:
		"""
		Check the reference value.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		RefusedOperationError
			When ``value`` is None for a rule with a rule of its own for missing values, such as ``Equal(None)``.
		"""
		rule_class = type(self)
		value = cast(object, self.value)
		refuse_missing_value(rule_class.__name__, self.MISSING_VALUE_RULE, value)
		require_field_types(self)


def refuse_missing_value(rule_name: str, missing_value_rule: str | None, value: object) -> None:
	"""
	Refuse None as the reference value of a rule that has a rule of its own for missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule_name
		The name of the rule, such as ``"Equal"``.
	missing_value_rule
		The rule testing missing values in its place, such as ``"IsMissing"``, or None when there is none.
	value
		The reference value.

	Raises
	------
	RefusedOperationError
		When the value is None and the rule has a rule of its own for missing values.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.rules.value_rule import refuse_missing_value
	>>> try:
	... 	refuse_missing_value("Equal", "IsMissing", None)
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Equal(None) is not available, use IsMissing instead.
	"""
	if value is not None:
		return

	if missing_value_rule is None:
		return

	operation = MISSING_VALUE_OPERATION.format(rule_name=rule_name)
	raise RefusedOperationError(operation, missing_value_rule)
