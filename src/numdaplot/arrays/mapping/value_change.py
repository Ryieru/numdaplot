"""
One old value and the new value replacing it.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.rules.rule_values import ScalarValue


@dataclass(frozen=True)
class ValueChange:
	"""
	One old value of an Array and the new value replacing it, used by ``ValueMapping``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	old_value
		The value replaced, of the type family of the Array: ``2.0`` finds the integer ``2``.
	new_value
		The value replacing it, or None to make it missing.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names, such as None as old value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> severities = ndp.Array.from_list([1, 2, -1])
	>>> changes = [ndp.ValueChange(1, "Indemne"), ndp.ValueChange(2, "Tue"), ndp.ValueChange(-1, None)]
	>>> severities.apply(ndp.ValueMapping(changes=changes))
	Array(['Indemne', 'Tue', nan], dtype=TEXT)
	"""

	old_value: ScalarValue
	new_value: ScalarValue | None

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
