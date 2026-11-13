"""
Check of the settings of an object against the annotations of its fields.

The annotations are the only description of what a setting accepts, so a check and a signature never disagree.

.. versionadded:: 0.1.0
"""

import dataclasses
import functools
from dataclasses import dataclass
from typing import cast

from numdaplot.argument_checks.annotation_kinds import AcceptedKinds, read_accepted_kinds, read_annotations
from numdaplot.argument_checks.kind_descriptions import describe_kinds
from numdaplot.errors.invalid_type_error import InvalidTypeError

SETTING_NAME_FORMAT = "{owner_name} {field_name}"


@dataclass(frozen=True)
class FieldCheck:
	"""
	One field of a setting object, and what it accepts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	field_name
		The name of the field.
	setting_name
		The name shown in the error message, such as ``"Region rows"``.
	kinds
		What the field accepts.
	"""

	field_name: str
	setting_name: str
	kinds: AcceptedKinds


def require_field_types(setting: object) -> None:
	"""
	Check that every field of a setting object holds a value accepted by its annotation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting
		The dataclass instance to check.

	Raises
	------
	InvalidTypeError
		At the first field holding a value its annotation does not accept.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.field_types import require_field_types
	>>> require_field_types(ndp.Index(1))
	>>> try:
	... 	ndp.Preview(count="2")
	... except ndp.InvalidTypeError as error:
	... 	print(error)
	Preview count expects an int, got '2'.
	"""
	setting_class = type(setting)
	field_checks = find_field_checks(setting_class)

	for field_check in field_checks:
		value = getattr(setting, field_check.field_name)
		is_accepted = accepts_value(field_check.kinds, value)
		if not is_accepted:
			expected = describe_kinds(field_check.kinds, value)
			rejected_value = find_rejected_value(field_check.kinds, value)
			raise InvalidTypeError(field_check.setting_name, expected, rejected_value)


@functools.cache
def find_field_checks(setting_class: type) -> tuple[FieldCheck, ...]:
	"""
	Return the checks of the fields of a dataclass, built once for each class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_class
		The dataclass.

	Returns
	-------
	tuple[FieldCheck, ...]
		One check per field.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.field_types import find_field_checks
	>>> find_field_checks(ndp.Index)[0].setting_name
	'Index position'
	"""
	annotations = read_annotations(setting_class)
	field_checks = list[FieldCheck]()
	dataclass_fields = dataclasses.fields(setting_class)

	for dataclass_field in dataclass_fields:
		field_name = dataclass_field.name
		setting_name = SETTING_NAME_FORMAT.format(owner_name=setting_class.__name__, field_name=field_name)
		kinds = read_accepted_kinds(annotations[field_name])
		field_check = FieldCheck(field_name, setting_name, kinds)
		field_checks.append(field_check)

	return tuple(field_checks)


def accepts_value(kinds: AcceptedKinds, value: object) -> bool:
	"""
	Return whether a value is of an accepted kind, every item of a list included.

	A boolean is a Python integer, yet it is only accepted where the annotation names ``bool``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	kinds
		What the setting accepts.
	value
		The value.

	Returns
	-------
	bool
		True when the value is accepted.

	Examples
	--------
	>>> from numdaplot.argument_checks.field_types import accepts_value
	>>> from numdaplot.argument_checks.annotation_kinds import read_accepted_kinds
	>>> accepts_value(read_accepted_kinds(int), True)
	False
	>>> accepts_value(read_accepted_kinds(list[str]), ["a", 1])
	False
	"""
	if object in kinds.classes:
		return True

	if isinstance(value, bool):
		return bool in kinds.classes

	if isinstance(value, kinds.classes):
		return True

	if kinds.list_items is None or not isinstance(value, list):
		return False

	items = cast(list[object], value)

	for item in items:
		is_item_accepted = accepts_value(kinds.list_items, item)
		if not is_item_accepted:
			return False

	return True


def find_rejected_value(kinds: AcceptedKinds, value: object) -> object:
	"""
	Return what to show in the error message: the first rejected item of a list, or the rejected value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	kinds
		What the setting accepts.
	value
		The rejected value.

	Returns
	-------
	object
		The first rejected item when the value is a list of accepted kind, the value otherwise.

	Examples
	--------
	>>> from numdaplot.argument_checks.field_types import find_rejected_value
	>>> from numdaplot.argument_checks.annotation_kinds import read_accepted_kinds
	>>> find_rejected_value(read_accepted_kinds(list[str]), ["a", 1])
	1
	"""
	if kinds.list_items is None or not isinstance(value, list):
		return value

	items = cast(list[object], value)

	for item in items:
		is_item_accepted = accepts_value(kinds.list_items, item)
		if not is_item_accepted:
			return item

	return items
