"""
The types that the public annotations name without exporting them, and their page in the documentation.

These types are not exported: a user passes the values themselves. They still appear in the annotations and the
docstrings, so the documentation has one page defining them, and their names link to it.

.. versionadded:: 0.1.0
"""

import griffe
from link_targets import object_exists

VALUE_TYPE_PATHS = {
	"ScalarValue": "numdaplot.rules.rule_values.ScalarValue",
	"OrderedValue": "numdaplot.rules.rule_values.OrderedValue",
	"ListValue": "numdaplot.arrays.array_creation.ListValue",
	"NestedValues": "numdaplot.arrays.array_creation.NestedValues",
	"FilePath": "numdaplot.tables.files.file_paths.FilePath",
}
VALUE_TYPES_TITLE = "Value types"
VALUE_TYPES_SECTION = "Types"
VALUE_TYPES_PAGE_PATH = "api/types/value_types.md"
PAGE_INTRODUCTION = (
	"# Value types\n\n"
	"The names below appear in the annotations and in the descriptions of the parameters. numdaplot does not export "
	"them, so `ndp.ScalarValue` does not exist: a parameter of one of these types takes the value itself.\n"
)
VALUE_TYPE_BLOCK = "::: {path}\n    options:\n      heading_level: 2\n"
BLOCK_SEPARATOR = "\n"
PATH_SEPARATOR = "."


def build_value_types_page() -> str:
	"""
	Return the Markdown of the page defining every value type.

	.. versionadded:: 0.1.0

	Returns
	-------
	str
		The title and the introduction of the page, then one block per alias, read from its docstring.

	Examples
	--------
	>>> from value_types import build_value_types_page
	>>> build_value_types_page().splitlines()[0]
	'# Value types'
	"""
	blocks = [PAGE_INTRODUCTION]

	for path in VALUE_TYPE_PATHS.values():
		block = VALUE_TYPE_BLOCK.format(path=path)
		blocks.append(block)

	page_content = BLOCK_SEPARATOR.join(blocks)

	return page_content


def find_value_type_paths(loader: griffe.GriffeLoader) -> dict[str, str]:
	"""
	Return the path of each value type that a loader knows, by name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	loader
		The loader that holds every loaded module.

	Returns
	-------
	dict[str, str]
		The paths of ``VALUE_TYPE_PATHS`` found among the loaded modules.
	"""
	value_type_paths = {name: path for name, path in VALUE_TYPE_PATHS.items() if object_exists(path, loader)}

	return value_type_paths


def link_type_parameters(cls: griffe.Class, value_type_paths: dict[str, str], loader: griffe.GriffeLoader) -> None:
	"""
	Make the annotations naming a type parameter of a class that has the name of a value type refer to this alias.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cls
		A class, whose attributes are updated in place.
	value_type_paths
		The path of each value type, by name.
	loader
		The loader that holds every loaded module.
	"""
	parameter_names = {type_parameter.name for type_parameter in cls.type_parameters}
	linked_names = parameter_names & value_type_paths.keys()

	for member in cls.members.values():
		annotation = getattr(member, "annotation", None)
		if not isinstance(annotation, griffe.Expr):
			continue

		for part in annotation.iterate():
			if isinstance(part, griffe.ExprName) and part.name in linked_names:
				module_path, _, _ = value_type_paths[part.name].rpartition(PATH_SEPARATOR)
				part.parent = loader.modules_collection.get_member(module_path)
