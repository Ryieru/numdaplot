"""
Chart drawing each value as a bar.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from dataclasses import dataclass

from numdaplot.plots.charts.bar_layout import BarLayout
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.chart_settings import copy_colors, copy_columns
from numdaplot.plots.charts.orientation import Orientation
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_optional_column_name


@dataclass(frozen=True)
class BarChart(Chart):
	"""
	Chart drawing each value as a bar, used by ``plot_bar``.

	Each ``x`` value gets its own position, labeled with that value, in the order of the rows. A missing value
	draws no bar, and a row whose ``x`` text is missing is left out.

	.. versionadded:: 0.1.0

	Parameters
	----------
	x
		For a Table, the column labeling the bars: numbers, dates, datetimes or texts, the row numbers when
		omitted. An Array takes none, its rows being numbered.
	y
		For a Table, the columns drawn, holding numbers, one series of bars each. A Table needs it, even for a single
		column. An Array takes none: when omitted, each of its columns is a series.
	orientation
		The direction of the bars, ``Orientation.VERTICAL`` by default.
	layout
		How the bars of several series share a position, ``BarLayout.GROUPED`` by default.
	colors
		One color per series, the colors of the default cycle when omitted. The chart keeps its own list.

	Raises
	------
	InvalidSettingTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``x`` or a name in ``y`` is an empty text.
	EmptyListError
		When ``y`` or ``colors`` is an empty list.
	DuplicateColumnError
		When a column name appears twice in ``y``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> sales_2025 = ndp.Array.from_list([120.0, 80.0, 45.0])
	>>> sales_2026 = ndp.Array.from_list([150.0, 95.0, 40.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "2025": sales_2025, "2026": sales_2026})
	>>> chart = ndp.BarChart(x="city", y=["2025", "2026"])
	>>> plot = ndp.plot_bar(sales, chart)
	>>> plot.show()
	"""

	x: str | None = None
	y: list[str] | None = None
	orientation: Orientation = Orientation.VERTICAL
	layout: BarLayout = BarLayout.GROUPED
	colors: Sequence[Color | CustomColor] | None = None

	def __post_init__(self) -> None:
		"""
		Check the columns and the colors and replace them with copies that only the chart holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``x`` or a name in ``y`` is an empty text.
		EmptyListError
			When ``y`` or ``colors`` is an empty list.
		DuplicateColumnError
			When a column name appears twice in ``y``.
		"""
		require_field_types(self)

		require_optional_column_name(self.x)

		columns_copy = copy_columns(self.y)
		colors_copy = copy_colors(self.colors)
		object.__setattr__(self, "y", columns_copy)
		object.__setattr__(self, "colors", colors_copy)
