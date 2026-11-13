"""
Reading of an annotation as the values a setting accepts: classes, None, lists and their items.

.. versionadded:: 0.2.0
"""

import importlib
import types
import typing
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, cast

import numpy

PACKAGE_NAME = "numdaplot"
NONE_NAME = "None"
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


def read_annotations(annotated: Any) -> dict[str, Any]:
	"""
	Return the annotations of a class or a function, resolving the names only known to the type checker.

	Array and its settings refer to each other, so some annotations are texts naming a class that their module
	cannot import. Those names are looked up in numdaplot at the first call, when it is entirely imported.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotated
		The class or the function.

	Returns
	-------
	dict[str, Any]
		The annotation of each field or parameter.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.annotation_kinds import read_annotations
	>>> read_annotations(ndp.Index)["position"]
	<class 'int'>
	"""
	try:
		annotations = typing.get_type_hints(annotated)
	except NameError:
		package = importlib.import_module(PACKAGE_NAME)
		package_names = vars(package)
		annotations = typing.get_type_hints(annotated, localns=package_names)

	return annotations


def read_accepted_kinds(annotation: object, open_aliases: frozenset[object] = frozenset()) -> AcceptedKinds:
	"""
	Return what an annotation accepts, going through its aliases, its type parameters and its unions.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotation
		The annotation of a field.
	open_aliases
		The aliases being expanded, none by default.

	Returns
	-------
	AcceptedKinds
		The accepted classes, and what the items of a list accept.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.annotation_kinds import read_accepted_kinds
	>>> read_accepted_kinds(ndp.Side | None).names
	('Side', 'None')
	"""
	classes = list[type]()
	names = list[str]()
	list_items = None
	expanded_aliases = open_aliases
	if isinstance(annotation, typing.TypeAliasType):
		expanded_aliases = open_aliases | {annotation}

	members = list_annotation_members(annotation, open_aliases)

	for member in members:
		origin = typing.get_origin(member)
		if origin in LIST_ORIGINS:
			member_arguments = typing.get_args(member)
			item_annotation = member_arguments[0]
			list_items = read_accepted_kinds(item_annotation, expanded_aliases)
			continue

		member_classes = find_member_classes(member)
		classes.extend(member_classes)
		member_name = find_member_name(member)
		names.append(member_name)

	class_tuple = tuple(classes)
	name_tuple = tuple(names)
	accepted_kinds = AcceptedKinds(class_tuple, list_items, name_tuple)

	return accepted_kinds


def list_annotation_members(annotation: object, open_aliases: frozenset[object] = frozenset()) -> list[object]:
	"""
	Return the members of an annotation, with its aliases, its type parameters and its unions expanded.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotation
		The annotation.
	open_aliases
		The aliases being expanded, none by default.

	Returns
	-------
	list[object]
		The classes and the list annotations it accepts.

	Examples
	--------
	>>> from numdaplot.settings.annotation_kinds import list_annotation_members
	>>> list_annotation_members(int | None)
	[<class 'int'>, <class 'NoneType'>]
	"""
	if isinstance(annotation, typing.TypeAliasType):
		# An alias referring to itself accepts anything at its deeper levels.
		if annotation in open_aliases:
			return [typing.Any]

		aliased_members = list_annotation_members(annotation.__value__, open_aliases | {annotation})
		return aliased_members

	nested_annotations = None
	if isinstance(annotation, typing.TypeVar):
		# A type parameter without constraint accepts anything.
		nested_annotations = annotation.__constraints__ or (typing.Any,)

	origin = typing.get_origin(annotation)
	if isinstance(origin, typing.TypeAliasType):
		nested_annotations = (origin.__value__,)

	if origin in UNION_ORIGINS:
		nested_annotations = typing.get_args(annotation)

	if nested_annotations is None:
		return [annotation]

	members = list[object]()

	for nested_annotation in nested_annotations:
		nested_members = list_annotation_members(nested_annotation, open_aliases)
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
	>>> from numdaplot.settings.annotation_kinds import find_member_classes
	>>> find_member_classes(str)
	(<class 'str'>,)
	"""
	if member is typing.Any:
		return (object,)

	if member in NUMBER_CLASSES:
		return NUMBER_CLASSES[member]

	origin = typing.get_origin(member)
	if origin is not None:
		return (cast(type, origin),)

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
	>>> from numdaplot.settings.annotation_kinds import find_member_name
	>>> find_member_name(type(None))
	'None'
	"""
	if member is types.NoneType:
		return NONE_NAME

	origin = typing.get_origin(member)
	named_member = member if origin is None else origin
	member_text = str(named_member)
	member_name = getattr(named_member, "__name__", member_text)

	return member_name
