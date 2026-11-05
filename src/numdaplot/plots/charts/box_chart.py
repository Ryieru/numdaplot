"""
Chart summing up the spread of values as boxes.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from dataclasses import dataclass

from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.chart_settings import copy_colors, copy_columns
from numdaplot.plots.charts.outliers import Outliers
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.settings.setting_types import require_list_not_text
from numdaplot.tables.columns.column_names import require_optional_column_name

COLUMNS_SETTING = "BoxChart columns"


@dataclass(frozen=True)
class BoxChart(Chart):
	"""
	Chart summing up the spread of the values of each column as a box, used by ``plot_box``.

	The box goes from the first to the third quartile, with a line at the median. The whiskers reach the
	furthest values within 1.5 box heights of the box, and the values beyond them are outliers. Missing values
	are left out.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		For a Table, the columns drawn, holding numbers. A Table needs it, even for a single column. An Array takes
		none: when omitted, each of its columns is drawn.
	group_by
		For a Table, a column of texts splitting the rows into groups, each drawn at its own position in alphabetical
		order, with the boxes of the columns side by side. A row whose group is missing is left out. One box per column
		when omitted.
	outliers
		Whether the outliers are drawn, ``Outliers.SHOWN`` by default.
	colors
		One color per column, the colors of the default cycle when omitted. The chart keeps its own list.

	Raises
	------
	InvalidColumnNameError
		When ``group_by`` or a name in ``columns`` is an empty text.
	InvalidSettingTypeError
		When ``columns`` is a single text instead of a list.
	EmptyListError
		When ``columns`` or ``colors`` is an empty list.
	DuplicateColumnError
		When a column name appears twice in ``columns``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris", "Lyon", "Paris", "Lyon", "Paris", "Lyon"])
	>>> prices_2025 = ndp.Array.from_list([12.0, 9.5, 14.0, 10.0, 13.5, 8.0, 15.0, 11.0])
	>>> prices_2026 = ndp.Array.from_list([14.0, 10.5, 16.0, 11.0, 15.5, 9.0, 17.0, 12.5])
	>>> prices = ndp.Table.from_arrays({"city": cities, "2025": prices_2025, "2026": prices_2026})
	>>> chart = ndp.BoxChart(columns=["2025", "2026"], group_by="city")
	>>> plot = ndp.plot_box(prices, chart)
	>>> plot.show()
	"""

	columns: list[str] | None = None
	group_by: str | None = None
	outliers: Outliers = Outliers.SHOWN
	colors: Sequence[Color | CustomColor] | None = None

	def __post_init__(self) -> None:
		"""
		Check the columns and the colors and replace them with copies that only the chart holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidColumnNameError
			When ``group_by`` or a name in ``columns`` is an empty text.
		InvalidSettingTypeError
			When ``columns`` is a single text instead of a list.
		EmptyListError
			When ``columns`` or ``colors`` is an empty list.
		DuplicateColumnError
			When a column name appears twice in ``columns``.
		"""
		require_optional_column_name(self.group_by)

		require_list_not_text(COLUMNS_SETTING, self.columns)

		columns_copy = copy_columns(self.columns)
		colors_copy = copy_colors(self.colors)
		object.__setattr__(self, "columns", columns_copy)
		object.__setattr__(self, "colors", colors_copy)
