"""
Sections of the navigation of the API pages, and the groups of methods of the Array, Table and Plot pages.

The navigation places each public class in the first section whose prefix matches its module. A new package needs its
own section here, or the build stops with a ``KeyError``.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

PATH_SEPARATOR = "."


@dataclass(frozen=True)
class Section:
	"""
	Where the classes of a module family are placed in the navigation.

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


# The first section whose prefix matches a module wins, so the most precise prefixes come first.
SECTIONS = (
	Section("numdaplot.arrays.creation", "Arrays", "arrays", "Creation settings"),
	Section("numdaplot.arrays.math_functions", "Arrays", "arrays", "Math functions"),
	Section("numdaplot.arrays.mapping", "Arrays", "arrays", "Value mapping"),
	Section("numdaplot.arrays", "Arrays", "arrays"),
	Section("numdaplot.tables.files", "Tables", "tables", "File settings"),
	Section("numdaplot.tables.conflict", "Tables", "tables", "File settings"),
	Section("numdaplot.tables.filtering", "Tables", "tables", "Filter settings"),
	Section("numdaplot.tables.aggregation", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.pivot", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.description", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.value_counts", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.columns", "Tables", "tables", "Column settings"),
	Section("numdaplot.tables.sorting", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.duplicates", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.preview", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.missing", "Tables", "tables", "Missing value settings"),
	Section("numdaplot.tables.joining", "Tables", "tables", "Join settings"),
	Section("numdaplot.tables", "Tables", "tables"),
	Section("numdaplot.conversions", "Conversions", "conversions"),
	Section("numdaplot.dates", "Dates", "dates"),
	Section("numdaplot.data_types", "Types", "types"),
	Section("numdaplot.rules", "Rules", "rules"),
	Section("numdaplot.statistics", "Statistics", "statistics"),
	Section("numdaplot.shapes", "Shapes", "shapes"),
	Section("numdaplot.positions", "Positions", "positions"),
	Section("numdaplot.ordering", "Sort settings", "ordering"),
	Section("numdaplot.ratios", "Measures", "measures"),
	Section("numdaplot.plots.charts", "Plots", "plots", "Chart settings"),
	Section("numdaplot.plots.style", "Plots", "plots", "Style settings"),
	Section("numdaplot.plots.figure", "Plots", "plots", "Figures"),
	Section("numdaplot.plots", "Plots", "plots"),
	Section("numdaplot.errors", "Errors", "errors"),
)
SECTION_TITLES = tuple(dict.fromkeys(section.title for section in SECTIONS))
# Classes without group come first in their section, then the groups in the order of SECTIONS.
GROUP_ORDER = (None, *dict.fromkeys(section.group for section in SECTIONS if section.group is not None))
MEMBER_SECTIONS = {
	"Array": (
		("Creation", ("from_list", "from_numpy", "filled", "from_range", "from_spacing", "from_date_parts", "random")),
		("Information", ("shape", "dtype")),
		("Conversion and comparison", ("convert", "to_list", "to_value", "to_numpy", "is_equal")),
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
	"Plot": (
		(
			"Creation",
			("line", "bar", "scatter", "histogram", "box", "pie", "heatmap", "missing_by_column", "missing_map"),
		),
		("Charts over a Plot", ("add_line", "add_bar", "add_scatter")),
		("Output", ("show", "save", "to_matplotlib")),
	),
	"Table": (
		(
			"Reading files",
			("from_csv", "from_json", "from_excel", "from_parquet", "from_stata", "from_sas", "from_xpt"),
		),
		("Writing files", ("to_csv", "to_json", "to_excel", "to_parquet", "to_stata")),
		("Conversion and comparison", ("from_pandas", "from_arrays", "to_pandas", "column", "to_value", "is_equal")),
		("Information", ("shape", "row_count", "column_count", "column_names", "column_types", "column_time_zones")),
		("Selection", ("filter", "take", "check")),
		("Columns", ("choose_columns", "rename", "convert", "add_column")),
		("Statistics", ("aggregate", "describe", "count_values")),
		("Order and duplicates", ("sort", "drop_duplicates")),
		("Missing values", ("count_missing", "preview_missing", "drop_missing")),
		("Display", ("preview", "__repr__")),
		("Refused operations", ("__eq__", "__lt__", "__getitem__", "__iter__", "__contains__", "__len__", "__bool__")),
	),
}


def find_section(module_name: str) -> Section:
	"""
	Return the section of the navigation where the classes of a module are placed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	module_name
		The module defining a public class, such as ``numdaplot.rules.greater``.

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
	>>> from api_sections import find_section
	>>> find_section("numdaplot.tables.files.csv_read_options").group
	'File settings'
	"""
	for section in SECTIONS:
		package_prefix = section.module_prefix + PATH_SEPARATOR
		is_in_package = module_name.startswith(package_prefix)
		is_inside = module_name == section.module_prefix or is_in_package
		if is_inside:
			return section

	raise KeyError(module_name)
