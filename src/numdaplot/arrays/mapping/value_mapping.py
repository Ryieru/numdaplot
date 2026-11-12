"""
Replacement of each value of an Array by a new value.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.mapping.unmatched import Unmatched
from numdaplot.arrays.mapping.value_change import ValueChange
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_type import find_common_type, find_value_type
from numdaplot.errors.duplicate_value_error import DuplicateValueError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.rules.rule_values import ScalarValue
from numdaplot.settings.field_types import require_field_types

CHANGE_ITEM_NAME = "value change"
MAPPING_OPERATION = "ValueMapping"


@dataclass(frozen=True)
class ValueMapping:
	"""
	The new value of each listed value of an Array, used by ``Array.apply``, such as codes replaced by labels.

	A missing value stays missing. The new values share one type, which the result takes: integers and decimals
	give decimals. With ``others=Unmatched.KEEP``, the result takes the type holding both the values of the Array and
	the new values.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts ``others=Unmatched.KEEP``, which keeps the values without ``ValueChange``.

	Parameters
	----------
	changes
		The ``ValueChange`` of each replaced value, at least one, each old value once. The mapping keeps its own copy
		of the list.
	others
		What happens to a value without ``ValueChange``, ``Unmatched.ERROR`` by default.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``changes`` is an empty list.
	IncompatibleTypesError
		When the old values, or the new values, mix several families of types, such as numbers and texts.
	DuplicateValueError
		When an old value appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([2, 1, 2])
	>>> sexes.apply(ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme"), ndp.ValueChange(2, "Femme")]))
	Array(['Femme', 'Homme', 'Femme'], dtype=TEXT)
	"""

	changes: list[ValueChange]
	others: Unmatched = Unmatched.ERROR

	def __post_init__(self) -> None:
		"""
		Check the changes: at least one, old and new values each of one type family, no old value twice.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``changes`` is an empty list.
		IncompatibleTypesError
			When the old values, or the new values, mix several families of types.
		DuplicateValueError
			When an old value appears twice.
		"""
		require_field_types(self)

		if self.changes == []:
			raise EmptyListError(CHANGE_ITEM_NAME)

		old_values = [change.old_value for change in self.changes]
		old_types = [find_value_type(old_value) for old_value in old_values]
		find_common_type(old_types, MAPPING_OPERATION)
		require_unique_values(old_values)
		find_new_type(self.changes)
		changes_copy = list(self.changes)
		object.__setattr__(self, "changes", changes_copy)


def require_unique_values(values: list[ScalarValue]) -> None:
	"""
	Check that no value appears twice, ``2`` and ``2.0`` being the same value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Values of one family of types.

	Raises
	------
	DuplicateValueError
		At the first value seen before.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.value_mapping import require_unique_values
	>>> try:
	... 	require_unique_values([1, 2, 2.0])
	... except ndp.DuplicateValueError as error:
	... 	print(error)
	The value 2.0 appears more than once.
	"""
	seen_values = set[ScalarValue]()
	for value in values:
		if value in seen_values:
			raise DuplicateValueError(value)

		seen_values.add(value)


def find_new_type(changes: list[ValueChange]) -> Type | None:
	"""
	Return the type shared by the new values of a mapping.

	.. versionadded:: 0.1.0

	Parameters
	----------
	changes
		The changes of a mapping.

	Returns
	-------
	Type or None
		The common type of the new values that are not None, or None when every new value is None.

	Raises
	------
	IncompatibleTypesError
		When the new values mix several families of types.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.value_mapping import find_new_type
	>>> find_new_type([ndp.ValueChange(1, 10), ndp.ValueChange(2, 2.5), ndp.ValueChange(-1, None)])
	<Type.FLOAT64: 10>
	"""
	new_types = [find_value_type(change.new_value) for change in changes if change.new_value is not None]
	if new_types == []:
		return None

	new_type = find_common_type(new_types, MAPPING_OPERATION)

	return new_type
