"""
MkDocs hook generating one API page per public class of numdaplot, and the navigation between them.

Every name of ``ndp.__all__`` gets a page made at build time, so no page is written by hand and a new
public class appears in the documentation on its own. The pages of ``Array`` and ``Table`` list their
methods in sections, such as "Creation". The navigation groups the pages by section, such as "Rules",
then by settings family, such as "File settings", and is placed after the home page.

.. versionadded:: 0.1.0
"""

import inspect
from dataclasses import dataclass
from typing import Any

from api_sections import GROUP_ORDER, MEMBER_SECTIONS, PATH_SEPARATOR, SECTION_TITLES, Section, find_section
from mkdocs.structure.files import File, Files
from value_types import VALUE_TYPES_PAGE_PATH, VALUE_TYPES_SECTION, VALUE_TYPES_TITLE, build_value_types_page

import numdaplot

API_FOLDER = "api"
NAV_KEY = "nav"
API_TITLE = "API"
HOME_POSITION = 1
PAGE_PATH = "{folder}/{section_folder}/{module_name}.md"
CLASS_BLOCK = "::: {identifier}\n    options:\n      heading_level: {heading_level}\n"
PAGE_HEADING_LEVEL = 1
MEMBER_HEADING_LEVEL = 3
MAIN_CLASS_OPTIONS = "      members: false\n      show_bases: false\n      show_source: false\n"
ATTRIBUTE_OPTIONS = "      show_signature_annotations: true\n"
SECTION_TITLE = "## {title} {{ .api-section }}\n"
BLOCK_SEPARATOR = "\n"
FIRST_CLASSES = frozenset(
	{
		"Array",
		"Table",
		"Rule",
		"Statistic",
		"NumdaplotError",
		"NumdaplotWarning",
		"MathFunction",
		"Distribution",
		"TimeFunction",
		"Plot",
		"Chart",
		"Figure",
	}
)


@dataclass(frozen=True)
class PublicObject:
	"""
	A public class of numdaplot and the page documenting it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The public name, such as ``Greater``.
	identifier
		The path of the object, such as ``numdaplot.rules.greater.Greater``.
	section
		Where the object is placed in the navigation.
	"""

	name: str
	identifier: str
	section: Section


def find_public_objects() -> list[PublicObject]:
	"""
	Return every public class of numdaplot, each with its section, in the order of the navigation.

	.. versionadded:: 0.1.0

	Returns
	-------
	list[PublicObject]
		The objects by section, then by group, the main and base classes such as ``Array`` or ``Rule``
		first, the others in alphabetical order.

	Examples
	--------
	>>> from api_pages import find_public_objects
	>>> find_public_objects()[0].name
	'Array'
	"""
	public_objects = list[PublicObject]()

	for name in numdaplot.__all__:
		exported_object = getattr(numdaplot, name)
		if not inspect.isclass(exported_object):
			continue

		module_name = exported_object.__module__
		section = find_section(module_name)
		identifier = module_name + PATH_SEPARATOR + name
		public_object = PublicObject(name, identifier, section)
		public_objects.append(public_object)

	public_objects.sort(key=order_public_object)

	return public_objects


def order_public_object(public_object: PublicObject) -> tuple[int, int, bool, str]:
	"""
	Return the sort key of a public class in the navigation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		A public class.

	Returns
	-------
	tuple[int, int, bool, str]
		The position of its section, the position of its group, whether it comes after the main classes,
		and its name. Classes without group come before the groups of their section.

	Examples
	--------
	>>> from api_pages import PublicObject, order_public_object
	>>> from api_sections import find_section
	>>> rule_section = find_section("numdaplot.rules.rule")
	>>> order_public_object(PublicObject("Rule", "numdaplot.rules.rule.Rule", rule_section))
	(5, 0, False, 'Rule')
	"""
	section_position = SECTION_TITLES.index(public_object.section.title)
	group_position = GROUP_ORDER.index(public_object.section.group)
	is_secondary = public_object.name not in FIRST_CLASSES
	sort_key = (section_position, group_position, is_secondary, public_object.name)

	return sort_key


def find_page_path(public_object: PublicObject) -> str:
	"""
	Return the path of the generated page of a public class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		A public class.

	Returns
	-------
	str
		The path inside the documentation folder, named after the module of the object.

	Examples
	--------
	>>> from api_pages import PublicObject, find_page_path
	>>> from api_sections import find_section
	>>> greater_section = find_section("numdaplot.rules.greater")
	>>> find_page_path(PublicObject("Greater", "numdaplot.rules.greater.Greater", greater_section))
	'api/rules/greater.md'
	"""
	module_path, _, _ = public_object.identifier.rpartition(PATH_SEPARATOR)
	_, _, module_name = module_path.rpartition(PATH_SEPARATOR)
	page_path = PAGE_PATH.format(
		folder=API_FOLDER, section_folder=public_object.section.folder, module_name=module_name
	)

	return page_path


def build_page_content(public_object: PublicObject) -> str:
	"""
	Return the Markdown of the page of a public class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		A public class.

	Returns
	-------
	str
		The object as the title of the page. ``Array``, ``Table`` and ``Plot`` then list their members in sections,
		attributes with their type.

	Examples
	--------
	>>> from api_pages import PublicObject, build_page_content
	>>> from api_sections import find_section
	>>> greater_section = find_section("numdaplot.rules.greater")
	>>> print(build_page_content(PublicObject("Greater", "numdaplot.rules.greater.Greater", greater_section)))
	::: numdaplot.rules.greater.Greater
	options:
	heading_level: 1
	<BLANKLINE>
	"""
	class_block = CLASS_BLOCK.format(identifier=public_object.identifier, heading_level=PAGE_HEADING_LEVEL)
	if public_object.name not in MEMBER_SECTIONS:
		return class_block

	blocks = [class_block + MAIN_CLASS_OPTIONS]

	for section_title, member_names in MEMBER_SECTIONS[public_object.name]:
		section_heading = SECTION_TITLE.format(title=section_title)
		blocks.append(section_heading)

		for member_name in member_names:
			member_block = build_member_block(public_object, member_name)
			blocks.append(member_block)

	page_content = BLOCK_SEPARATOR.join(blocks)

	return page_content


def build_member_block(public_object: PublicObject, member_name: str) -> str:
	"""
	Return the Markdown documenting one member of a class with sections.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		``Array`` or ``Table``.
	member_name
		The name of a method or an attribute.

	Returns
	-------
	str
		The member block, showing the type of an attribute in its heading.

	Examples
	--------
	>>> from api_pages import PublicObject, build_member_block
	>>> from api_sections import find_section
	>>> table_section = find_section("numdaplot.tables.table")
	>>> print(build_member_block(PublicObject("Table", "numdaplot.tables.table.Table", table_section), "filter"))
	::: numdaplot.tables.table.Table.filter
	options:
	heading_level: 3
	<BLANKLINE>
	"""
	member_identifier = public_object.identifier + PATH_SEPARATOR + member_name
	member_block = CLASS_BLOCK.format(identifier=member_identifier, heading_level=MEMBER_HEADING_LEVEL)
	class_object = getattr(numdaplot, public_object.name)
	member_object = inspect.getattr_static(class_object, member_name)
	is_attribute = isinstance(member_object, property)
	if is_attribute:
		member_block += ATTRIBUTE_OPTIONS

	return member_block


def build_api_nav(public_objects: list[PublicObject]) -> list[Any]:
	"""
	Return the navigation of the API pages, by section, then by group.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_objects
		The public classes, in the order of the navigation.

	Returns
	-------
	list[Any]
		One ``{section title: entries}`` item per section, each entry being ``{name: page path}``
		or ``{group title: entries}``, as MkDocs reads its ``nav`` setting. The page of the value types
		follows the classes of its section.

	Examples
	--------
	>>> from api_pages import build_api_nav, find_public_objects
	>>> build_api_nav(find_public_objects())[0]["Arrays"][0]
	{'Array': 'api/arrays/array.md'}
	"""
	sections = dict[str, list[Any]]()
	groups = dict[tuple[str, str], list[Any]]()

	for public_object in public_objects:
		section_entries = sections.setdefault(public_object.section.title, [])
		page_entry = {public_object.name: find_page_path(public_object)}
		group = public_object.section.group
		if group is None:
			section_entries.append(page_entry)
			continue

		group_key = (public_object.section.title, group)
		if group_key not in groups:
			groups[group_key] = []
			section_entries.append({group: groups[group_key]})

		groups[group_key].append(page_entry)

	value_types_entries = sections.setdefault(VALUE_TYPES_SECTION, [])
	value_types_entries.append({VALUE_TYPES_TITLE: VALUE_TYPES_PAGE_PATH})
	api_nav = [{title: entries} for title, entries in sections.items()]

	return api_nav


def on_config(config: Any, **kwargs: Any) -> Any:
	"""
	Insert the generated API navigation after the home page, called by MkDocs when it reads its configuration.

	.. versionadded:: 0.1.0

	Parameters
	----------
	config
		The MkDocs configuration, whose ``nav`` holds the hand-written pages.
	**kwargs
		The other arguments MkDocs gives to its hooks, unused.

	Returns
	-------
	Any
		The configuration with the API section in its navigation.
	"""
	public_objects = find_public_objects()
	api_nav = build_api_nav(public_objects)
	config[NAV_KEY].insert(HOME_POSITION, {API_TITLE: api_nav})

	return config


def on_files(files: Files, config: Any, **kwargs: Any) -> Files:
	"""
	Add the generated API pages to the documentation files, called by MkDocs before it renders them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	files
		The files of the documentation folder.
	config
		The MkDocs configuration.
	**kwargs
		The other arguments MkDocs gives to its hooks, unused.

	Returns
	-------
	Files
		The files with one generated page per public class, and the page of the value types.
	"""
	public_objects = find_public_objects()

	for public_object in public_objects:
		page_path = find_page_path(public_object)
		page_content = build_page_content(public_object)
		page_file = File.generated(config, page_path, content=page_content)
		files.append(page_file)

	value_types_content = build_value_types_page()
	value_types_file = File.generated(config, VALUE_TYPES_PAGE_PATH, content=value_types_content)
	files.append(value_types_file)

	return files
