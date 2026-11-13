"""
Sections of the navigation of the API pages.

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
	Section("numdaplot.math_functions", "Arrays", "arrays", "Math functions"),
	Section("numdaplot.arrays.mapping", "Arrays", "arrays", "Value mapping"),
	Section("numdaplot.brackets.unmatched", "Arrays", "arrays", "Value mapping"),
	Section("numdaplot.arrays", "Arrays", "arrays"),
	Section("numdaplot.tables.files", "Tables", "tables", "File settings"),
	Section("numdaplot.files.conflict", "Tables", "tables", "File settings"),
	Section("numdaplot.tables.filtering", "Tables", "tables", "Filter settings"),
	Section("numdaplot.tables.aggregation", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.pivot", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.description", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.value_counts", "Tables", "tables", "Statistic settings"),
	Section("numdaplot.tables.columns", "Tables", "tables", "Column settings"),
	Section("numdaplot.brackets", "Tables", "tables", "Column settings"),
	Section("numdaplot.tables.sorting", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.duplicates", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.preview", "Tables", "tables", "Sort, duplicate and preview settings"),
	Section("numdaplot.tables.missing", "Tables", "tables", "Missing value settings"),
	Section("numdaplot.tables.joining", "Tables", "tables", "Join settings"),
	Section("numdaplot.tables", "Tables", "tables"),
	Section("numdaplot.conversions", "Conversions", "conversions"),
	Section("numdaplot.dates", "Dates", "dates"),
	Section("numdaplot.types", "Types", "types"),
	Section("numdaplot.rules", "Rules", "rules"),
	Section("numdaplot.statistics", "Statistics", "statistics"),
	Section("numdaplot.positions.shape", "Shapes", "shapes"),
	Section("numdaplot.positions", "Positions", "positions"),
	Section("numdaplot.ordering", "Sort settings", "ordering"),
	Section("numdaplot.measures", "Measures", "measures"),
	Section("numdaplot.plots.charts", "Plots", "plots", "Chart settings"),
	Section("numdaplot.plots.style", "Plots", "plots", "Style settings"),
	Section("numdaplot.plots.figure", "Plots", "plots", "Figures"),
	Section("numdaplot.plots", "Plots", "plots"),
	Section("numdaplot.errors", "Errors", "errors"),
)
UNIQUE_SECTION_TITLES = dict.fromkeys(section.title for section in SECTIONS)
SECTION_TITLES = tuple(UNIQUE_SECTION_TITLES)
# Classes without group come first in their section, then the groups in the order of SECTIONS.
GROUP_ORDER = (None, *dict.fromkeys(section.group for section in SECTIONS if section.group is not None))


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
