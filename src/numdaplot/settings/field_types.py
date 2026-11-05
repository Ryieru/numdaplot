"""
Check of the settings of an object against the annotations of its fields.

The annotations are the only description of what a setting accepts, so a check and a signature never disagree.

.. versionadded:: 0.1.0
"""

import dataclasses
import functools
import importlib
import types
import typing
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, cast

import numpy

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError

PACKAGE_NAME = "numdaplot"
NONE_NAME = "None"
VOWELS = "aeiouAEIOU"
ARTICLE_FORMAT = "{article} {name}"
NAMES_SEPARATOR = ", "
LAST_NAME_FORMAT = "{names} or {last_name}"
LIST_OF_FORMAT = "a list of {names}"
LIST_SUCH_AS_FORMAT = "a list such as [{text!r}]"
SETTING_NAME_FORMAT = "{owner_name} {field_name}"
NUMBER_CLASSES = dict[object, tuple[type, ...]](
	{
		bool: (bool, numpy.bool_),
		int: (int, numpy.integer),
		float: (int, float, numpy.integer, numpy.floating),
	}
)
UNION_ORIGINS = (typing.Union, types.UnionType)
LIST_ORIGINS = (list, Sequence)


@dataclass(frozen=True)
class AcceptedKinds:
	"""
	What a setting accepts, read from its annotation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	classes
		The accepted classes.
	list_items
		What the items of a list accept, or None when a list is not accepted.
	names
		The names of the accepted classes, in the order of the annotation, a list being left out.
	"""

	classes: tuple[type, ...]
	list_items: "AcceptedKinds | None"
	names: tuple[str, ...]


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
	InvalidSettingTypeError
		At the first field holding a value its annotation does not accept.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.field_types import require_field_types
	>>> require_field_types(ndp.Index(1))
	>>> try:
	... 	ndp.Preview(count="2")
	... except ndp.InvalidSettingTypeError as error:
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
			raise InvalidSettingTypeError(field_check.setting_name, expected, rejected_value)


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
	>>> from numdaplot.settings.field_types import find_field_checks
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


def read_annotations(setting_class: type) -> dict[str, Any]:
	"""
	Return the annotations of a class, resolving the names only known to the type checker.

	Array and its settings refer to each other, so some annotations are texts naming a class that their module
	cannot import. Those names are looked up in numdaplot at the first call, when it is entirely imported.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_class
		The class.

	Returns
	-------
	dict[str, Any]
		The annotation of each field.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.field_types import read_annotations
	>>> read_annotations(ndp.Index)["position"]
	<class 'int'>
	"""
	try:
		annotations = typing.get_type_hints(setting_class)
	except NameError:
		package = importlib.import_module(PACKAGE_NAME)
		package_names = vars(package)
		annotations = typing.get_type_hints(setting_class, localns=package_names)

	return annotations


def read_accepted_kinds(annotation: object) -> AcceptedKinds:
	"""
	Return what an annotation accepts, going through its aliases, its type parameters and its unions.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotation
		The annotation of a field.

	Returns
	-------
	AcceptedKinds
		The accepted classes, and what the items of a list accept.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.field_types import read_accepted_kinds
	>>> read_accepted_kinds(ndp.Side | None).names
	('Side', 'None')
	"""
	classes = list[type]()
	names = list[str]()
	list_items = None
	members = list_annotation_members(annotation)

	for member in members:
		origin = typing.get_origin(member)
		if origin in LIST_ORIGINS:
			item_annotation = typing.get_args(member)[0]
			list_items = read_accepted_kinds(item_annotation)
			continue

		member_classes = find_member_classes(member)
		classes.extend(member_classes)
		member_name = find_member_name(member)
		names.append(member_name)

	return AcceptedKinds(tuple(classes), list_items, tuple(names))


def list_annotation_members(annotation: object) -> list[object]:
	"""
	Return the members of an annotation, with its aliases, its type parameters and its unions expanded.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotation
		The annotation.

	Returns
	-------
	list[object]
		The classes and the list annotations it accepts.

	Examples
	--------
	>>> from numdaplot.settings.field_types import list_annotation_members
	>>> list_annotation_members(int | None)
	[<class 'int'>, <class 'NoneType'>]
	"""
	if isinstance(annotation, typing.TypeAliasType):
		aliased_members = list_annotation_members(annotation.__value__)
		return aliased_members

	nested_annotations = None
	if isinstance(annotation, typing.TypeVar):
		# A type parameter without constraint accepts anything.
		nested_annotations = annotation.__constraints__ or (typing.Any,)

	origin = typing.get_origin(annotation)
	if origin in UNION_ORIGINS:
		nested_annotations = typing.get_args(annotation)

	if nested_annotations is None:
		return [annotation]

	members = list[object]()

	for nested_annotation in nested_annotations:
		nested_members = list_annotation_members(nested_annotation)
		members.extend(nested_members)

	return members


def find_member_classes(member: object) -> tuple[type, ...]:
	"""
	Return the classes a member of an annotation accepts: numbers from numpy count as Python numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	member
		A class, or ``typing.Any`` which accepts everything.

	Returns
	-------
	tuple[type, ...]
		The accepted classes.

	Examples
	--------
	>>> from numdaplot.settings.field_types import find_member_classes
	>>> find_member_classes(str)
	(<class 'str'>,)
	"""
	if member is typing.Any:
		return (object,)

	if member in NUMBER_CLASSES:
		return NUMBER_CLASSES[member]

	return (cast(type, member),)


def find_member_name(member: object) -> str:
	"""
	Return the name of a member of an annotation, as shown in the error message.

	.. versionadded:: 0.1.0

	Parameters
	----------
	member
		A class, or ``typing.Any``.

	Returns
	-------
	str
		The name of the class, ``None`` for the type of None.

	Examples
	--------
	>>> from numdaplot.settings.field_types import find_member_name
	>>> find_member_name(type(None))
	'None'
	"""
	if member is types.NoneType:
		return NONE_NAME

	member_name = getattr(member, "__name__", str(member))

	return member_name


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
	>>> from numdaplot.settings.field_types import accepts_value, read_accepted_kinds
	>>> accepts_value(read_accepted_kinds(int), True)
	False
	>>> accepts_value(read_accepted_kinds(list[str]), ["a", 1])
	False
	"""
	if isinstance(value, bool):
		return bool in kinds.classes or object in kinds.classes

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
	>>> from numdaplot.settings.field_types import find_rejected_value, read_accepted_kinds
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


def describe_kinds(kinds: AcceptedKinds, value: object) -> str:
	"""
	Return what a setting accepts, as written in the error message.

	A text given in place of a list is shown inside a list, the most likely thing to write.

	.. versionadded:: 0.1.0

	Parameters
	----------
	kinds
		What the setting accepts.
	value
		The rejected value.

	Returns
	-------
	str
		The description, such as ``an Index, a Range or None``.

	Examples
	--------
	>>> from numdaplot.settings.field_types import describe_kinds, read_accepted_kinds
	>>> describe_kinds(read_accepted_kinds(list[str]), "price")
	"a list such as ['price']"
	>>> describe_kinds(read_accepted_kinds(int | None), "2")
	'an int or None'
	"""
	if kinds.list_items is not None and isinstance(value, str):
		return LIST_SUCH_AS_FORMAT.format(text=value)

	descriptions = [add_article(name) for name in kinds.names]
	if kinds.list_items is not None:
		item_names = join_names(kinds.list_items.names)
		list_description = LIST_OF_FORMAT.format(names=item_names)
		descriptions.append(list_description)

	description = join_names(descriptions)

	return description


def add_article(name: str) -> str:
	"""
	Return the name of a class with its article, None staying as it is.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name of a class.

	Returns
	-------
	str
		The name with ``a`` or ``an``.

	Examples
	--------
	>>> from numdaplot.settings.field_types import add_article
	>>> add_article("Index"), add_article("Range"), add_article("None")
	('an Index', 'a Range', 'None')
	"""
	if name == NONE_NAME:
		return name

	article = "an" if name[0] in VOWELS else "a"

	return ARTICLE_FORMAT.format(article=article, name=name)


def join_names(names: Sequence[str]) -> str:
	"""
	Return names separated by commas, the last one after ``or``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	names
		The names, at least one.

	Returns
	-------
	str
		The joined names.

	Examples
	--------
	>>> from numdaplot.settings.field_types import join_names
	>>> join_names(["an Index", "a Range", "None"])
	'an Index, a Range or None'
	"""
	first_names = names[:-1]
	last_name = names[-1]
	if not first_names:
		return last_name

	joined_names = NAMES_SEPARATOR.join(first_names)

	return LAST_NAME_FORMAT.format(names=joined_names, last_name=last_name)
