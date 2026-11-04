"""
MkDocs hook generating one API page per public class or function of numdaplot, and the navigation between them.

Every name of ``ndp.__all__`` gets a page made at build time, so no page is written by hand and a new
public class or function appears in the documentation on its own. The pages of ``Array`` and ``Table`` list their
methods in sections, such as "Creation". The navigation groups the pages by section, such as "Rules",
then by settings family, such as "File settings", and is placed after the home page.

.. versionadded:: 0.1.0
"""

import inspect
from dataclasses import dataclass
from typing import Any

from mkdocs.structure.files import File, Files

import numdaplot

API_FOLDER = "api"
NAV_KEY = "nav"
API_TITLE = "API"
HOME_POSITION = 1
PAGE_PATH = "{folder}/{section_folder}/{module_name}.md"
PATH_SEPARATOR = "."
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
		"MathFunction",
		"Distribution",
		"TimeFunction",
		"Plot",
		"Chart",
	}
)


@dataclass(frozen=True)
class Section:
	"""
	Where the classes and functions of a module family are placed in the navigation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	module_prefix
		The start of the module paths of the family, such as ``numdaplot.tables.files``.
	title
		The title of the section, such as ``Tables``.
	folder
		The folder of its pages, such as ``tables``.
	group
		The title of the group inside the section, such as ``File settings``, or ``None`` at the top of it.
	"""

	module_prefix: str
	title: str
	folder: str
	group: str | None = None


@dataclass(frozen=True)
class PublicObject:
	"""
	A public class or function of numdaplot and the page documenting it.

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


# The first section whose prefix matches a module wins, so the most precise prefixes come first.
SECTIONS = (
	Section("numdaplot.arrays.creation", "Arrays", "arrays", "Creation settings"),
	Section("numdaplot.arrays.math_functions", "Arrays", "arrays", "Math functions"),
	Section("numdaplot.arrays", "Arrays", "arrays"),
	Section("numdaplot.tables.files", "Tables", "tables", "File settings"),
	Section("numdaplot.tables.conflict", "Tables", "tables", "File settings"),
	Section("numdaplot.tables.filtering", "Tables", "tables", "Filter settings"),
	Section("numdaplot.tables.aggregation", "Tables", "tables", "Aggregation and description settings"),
	Section("numdaplot.tables.description", "Tables", "tables", "Aggregation and description settings"),
	Section("numdaplot.tables.columns", "Tables", "tables", "Column settings"),
	Section("numdaplot.tables.sorting", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.duplicates", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.preview", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.missing", "Tables", "tables", "Missing value settings"),
	Section("numdaplot.ratios", "Tables", "tables", "Missing value settings"),
	Section("numdaplot.tables", "Tables", "tables"),
	Section("numdaplot.dates", "Dates", "dates"),
	Section("numdaplot.data_types", "Types", "types"),
	Section("numdaplot.rules", "Rules", "rules"),
	Section("numdaplot.statistics", "Statistics", "statistics"),
	Section("numdaplot.positions", "Positions", "positions"),
	Section("numdaplot.ordering", "Sort settings", "ordering"),
	Section("numdaplot.plots.charts", "Plots", "plots", "Chart settings"),
	Section("numdaplot.plots.style", "Plots", "plots", "Style settings"),
	Section("numdaplot.plots", "Plots", "plots"),
	Section("numdaplot.errors", "Errors", "errors"),
)
SECTION_TITLES = tuple(dict.fromkeys(section.title for section in SECTIONS))
# Classes without group come first in their section, then the groups in the order of SECTIONS.
GROUP_ORDER = (None, *dict.fromkeys(section.group for section in SECTIONS if section.group is not None))
MEMBER_SECTIONS = {
	"Array": (
		("Creation", ("from_list", "from_numpy", "filled", "from_range", "from_spacing", "random")),
		("Information", ("shape", "dtype")),
		("Conversion and comparison", ("to_list", "to_value", "to_numpy", "is_equal")),
		("Selection", ("select", "check", "take", "replace")),
		("Calculation", ("compute", "apply")),
		("Layout", ("reshape", "transpose", "flatten", "sort", "unique")),
		(
			"Arithmetic operators",
			("__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__", "__mod__", "__pow__", "__neg__"),
		),
		("Logical operators", ("__and__", "__or__", "__invert__")),
		(
			"Refused operations",
			("__eq__", "__lt__", "__getitem__", "__iter__", "__contains__", "__len__", "__bool__", "__matmul__"),
		),
	),
	"Table": (
		(
			"Reading files",
			("from_csv", "from_json", "from_excel", "from_parquet", "from_stata", "from_sas", "from_xpt"),
		),
		("Writing files", ("to_csv", "to_json", "to_excel", "to_parquet", "to_stata")),
		("Conversion and comparison", ("from_pandas", "from_arrays", "to_pandas", "column", "to_value", "is_equal")),
		("Information", ("row_count", "column_names", "column_types", "column_time_zones")),
		("Selection", ("filter", "take", "check")),
		("Columns", ("choose_columns", "rename", "convert", "add_column")),
		("Statistics", ("aggregate", "describe")),
		("Order and duplicates", ("sort", "drop_duplicates")),
		("Missing values", ("count_missing", "preview_missing", "drop_missing")),
		("Display", ("preview", "__repr__")),
		("Refused operations", ("__eq__", "__lt__", "__getitem__", "__iter__", "__contains__", "__len__", "__bool__")),
	),
}


def find_section(module_name: str) -> Section:
	"""
	Return the section of the navigation where the classes and functions of a module are placed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	module_name
		The module defining a public class or function, such as ``numdaplot.rules.greater``.

	Returns
	-------
	Section
		The first section whose prefix matches the module.

	Raises
	------
	KeyError
		When no section matches: a new package needs its own section in ``SECTIONS``.

	Examples
	--------
	>>> from api_pages import find_section
	>>> find_section("numdaplot.tables.files.csv_options").group
	'File settings'
	"""
	for section in SECTIONS:
		package_prefix = section.module_prefix + PATH_SEPARATOR
		is_in_package = module_name.startswith(package_prefix)
		is_inside = module_name == section.module_prefix or is_in_package
		if is_inside:
			return section

	raise KeyError(module_name)


def find_public_objects() -> list[PublicObject]:
	"""
	Return every public class and function of numdaplot, each with its section, in the order of the navigation.

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
		is_documented = inspect.isclass(exported_object) or inspect.isfunction(exported_object)
		if not is_documented:
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
	Return the sort key of a public class or function in the navigation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		A public class or function.

	Returns
	-------
	tuple[int, int, bool, str]
		The position of its section, the position of its group, whether it comes after the main classes,
		and its name. Classes without group come before the groups of their section.

	Examples
	--------
	>>> from api_pages import PublicObject, find_section, order_public_object
	>>> rule_section = find_section("numdaplot.rules.rule")
	>>> order_public_object(PublicObject("Rule", "numdaplot.rules.rule.Rule", rule_section))
	(4, 0, False, 'Rule')
	"""
	section_position = SECTION_TITLES.index(public_object.section.title)
	group_position = GROUP_ORDER.index(public_object.section.group)
	is_secondary = public_object.name not in FIRST_CLASSES
	sort_key = (section_position, group_position, is_secondary, public_object.name)

	return sort_key


def find_page_path(public_object: PublicObject) -> str:
	"""
	Return the path of the generated page of a public class or function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		A public class or function.

	Returns
	-------
	str
		The path inside the documentation folder, named after the module of the object.

	Examples
	--------
	>>> from api_pages import PublicObject, find_page_path, find_section
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
	Return the Markdown of the page of a public class or function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_object
		A public class or function.

	Returns
	-------
	str
		The object as the title of the page. ``Array`` and ``Table`` then list their members in sections,
		attributes with their type.

	Examples
	--------
	>>> from api_pages import PublicObject, build_page_content, find_section
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
	>>> from api_pages import PublicObject, build_member_block, find_section
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
		The public classes and functions, in the order of the navigation.

	Returns
	-------
	list[Any]
		One ``{section title: entries}`` item per section, each entry being ``{name: page path}``
		or ``{group title: entries}``, as MkDocs reads its ``nav`` setting.

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
		The files with one generated page per public class or function.
	"""
	public_objects = find_public_objects()

	for public_object in public_objects:
		page_path = find_page_path(public_object)
		page_content = build_page_content(public_object)
		page_file = File.generated(config, page_path, content=page_content)
		files.append(page_file)

	return files
