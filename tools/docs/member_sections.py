"""
Sections of the members of the Array, Table and Plot pages, taken from the classes they are built from.

Array, Table and Plot are each built from classes named after them, such as ``TableCalculation``. Each of these classes
gives one section of the page, titled after the end of its name, holding its methods in the order of the code. A new
method appears in its section on its own. A new class needs its title in ``SECTION_TITLES``, or the build stops with a
``KeyError``.

.. versionadded:: 0.2.0
"""

import inspect
from dataclasses import dataclass

# The end of the name of each class, after the name of the class it builds, and the title of its section, in the
# order of the page. The same end gives the same title on every page.
SECTION_TITLES = (
	("Creation", "Creation"),
	("SeriesCreation", "Series creation"),
	("DistributionCreation", "Distribution creation"),
	("OverviewCreation", "Overview creation"),
	("Reading", "Reading files"),
	("Writing", "Writing files"),
	("Data", "Information"),
	("Exchange", "Conversion and comparison"),
	("TypeChange", "Type change"),
	("Selection", "Selection"),
	("Columns", "Columns"),
	("Calculation", "Calculation"),
	("Layout", "Layout"),
	("Joining", "Join"),
	("Missing", "Missing values"),
	("Arithmetic", "Arithmetic operators"),
	("ReflectedArithmetic", "Arithmetic operators with a value on the left"),
	("Logic", "Logical operators"),
	("Overlays", "Charts over a Plot"),
	("Output", "Output"),
	("Display", "Display"),
	("Refusals", "Refused operations"),
)
# The creation with ndp.Array(...) is refused, and its refusal is told by the class itself.
HIDDEN_MEMBERS = frozenset({"__init__"})
SPECIAL_MARK = "__"
PRIVATE_MARK = "_"
WRAPPED_MEMBER_TYPES = (classmethod, staticmethod, property)


@dataclass(frozen=True)
class MemberSection:
	"""
	A section of a class page, and the members it documents.

	.. versionadded:: 0.2.0

	Parameters
	----------
	title
		The title of the section, such as ``Selection``.
	member_names
		The names of the methods and attributes, in the order of the code.
	"""

	title: str
	member_names: tuple[str, ...]


def find_member_sections(built_class: type) -> list[MemberSection]:
	"""
	Return the sections of the page of a class, one per class it is built from that has documented members.

	.. versionadded:: 0.2.0

	Parameters
	----------
	built_class
		A public class, such as ``Table``.

	Returns
	-------
	list[MemberSection]
		The sections in the order of ``SECTION_TITLES``, or none for a class not built from classes named after it.

	Raises
	------
	KeyError
		When a class with documented members has an end of name missing from ``SECTION_TITLES``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from member_sections import find_member_sections
	>>> find_member_sections(ndp.Plot)[-1]
	MemberSection(title='Output', member_names=('show', 'save', 'to_matplotlib'))
	>>> find_member_sections(ndp.Greater)
	[]
	"""
	part_members = find_part_members(built_class)
	known_ends = {name_end for name_end, _ in SECTION_TITLES}

	for name_end in part_members:
		if name_end not in known_ends:
			raise KeyError(built_class.__name__ + name_end)

	member_sections = list[MemberSection]()

	for name_end, title in SECTION_TITLES:
		if name_end not in part_members:
			continue

		member_names = part_members[name_end]
		member_section = MemberSection(title, member_names)
		member_sections.append(member_section)

	return member_sections


def find_part_members(built_class: type) -> dict[str, tuple[str, ...]]:
	"""
	Return the documented members of each class a class is built from, by the end of the name of that class.

	.. versionadded:: 0.2.0

	Parameters
	----------
	built_class
		A public class, such as ``Table``.

	Returns
	-------
	dict[str, tuple[str, ...]]
		For each base class named after ``built_class`` and holding documented members, such as ``TableJoining``,
		the end of its name, such as ``Joining``, and its members in the order of the code.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from member_sections import find_part_members
	>>> find_part_members(ndp.Table)["Joining"]
	('join',)
	"""
	part_members = dict[str, tuple[str, ...]]()

	for base_class in built_class.__mro__:
		is_part = base_class.__name__.startswith(built_class.__name__)
		if base_class is built_class or not is_part:
			continue

		member_names = list_documented_members(base_class)
		if not member_names:
			continue

		name_end = base_class.__name__.removeprefix(built_class.__name__)
		part_members[name_end] = member_names

	return part_members


def list_documented_members(part_class: type) -> tuple[str, ...]:
	"""
	Return the methods and attributes a class defines itself and the documentation shows, in the order of the code.

	.. versionadded:: 0.2.0

	Parameters
	----------
	part_class
		A class Array, Table or Plot is built from.

	Returns
	-------
	tuple[str, ...]
		The public methods, attributes and special methods such as ``__add__``, without ``__init__``, the private
		helpers and the plain values such as ``__array_ufunc__ = None``.

	Examples
	--------
	>>> from numdaplot.tables.table_joining import TableJoining
	>>> from member_sections import list_documented_members
	>>> list_documented_members(TableJoining)
	('join',)
	"""
	member_names = list[str]()

	for member_name, member in vars(part_class).items():
		is_documented = is_documented_member(member_name, member)
		if is_documented:
			member_names.append(member_name)

	documented_members = tuple(member_names)

	return documented_members


def is_documented_member(member_name: str, member: object) -> bool:
	"""
	Return whether the documentation shows a member of a class.

	.. versionadded:: 0.2.0

	Parameters
	----------
	member_name
		The name of the member in the class.
	member
		The member as the class stores it.

	Returns
	-------
	bool
		True for a public method or attribute, or a special method other than ``__init__``.

	Examples
	--------
	>>> from member_sections import is_documented_member
	>>> is_documented_member("__add__", lambda self, other: other)
	True
	>>> is_documented_member("_wrap", lambda self, values: values)
	False
	>>> is_documented_member("__array_ufunc__", None)
	False
	"""
	if member_name in HIDDEN_MEMBERS:
		return False

	is_special = member_name.startswith(SPECIAL_MARK) and member_name.endswith(SPECIAL_MARK)
	is_private = member_name.startswith(PRIVATE_MARK)
	if is_private and not is_special:
		return False

	is_function = inspect.isfunction(member)
	is_wrapped = isinstance(member, WRAPPED_MEMBER_TYPES)
	is_routine = is_function or is_wrapped

	return is_routine
