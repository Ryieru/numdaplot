"""
Chart drawing each series as a line.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from dataclasses import dataclass

from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.chart_settings import copy_colors, copy_columns
from numdaplot.plots.charts.line_type import LineType
from numdaplot.plots.charts.marker_shape import MarkerShape
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_optional_column_name


@dataclass(frozen=True)
class LineChart(Chart):
	"""
	Chart drawing each series as a line joining its values, used by ``Plot.line``.

	A missing value breaks the line, which starts again at the next present value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	x
		For a Table, the column of the horizontal positions: numbers, dates, datetimes, texts or booleans, the row
		numbers when omitted. An Array takes none, its rows being numbered.
	y
		For a Table, the columns drawn, holding numbers, one line each. A Table needs it, even for a single column. An
		Array takes none: when omitted, each of its columns is a line.
	colors
		One color per line, the colors of the default cycle when omitted. The chart keeps its own list.
	line
		How the lines are drawn, ``LineType.SOLID`` by default.
	marker
		The shape drawn at each value, ``MarkerShape.NONE`` by default.

	Raises
	------
	InvalidTypeError
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
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, None, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> colors = [ndp.Color.BLUE, ndp.CustomColor("#ff8800")]
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"], colors=colors, marker=ndp.MarkerShape.CIRCLE)
	>>> plot = ndp.Plot.line(sales, chart)
	>>> plot.show()
	"""

	x: str | None = None
	y: list[str] | None = None
	colors: Sequence[Color | CustomColor] | None = None
	line: LineType = LineType.SOLID
	marker: MarkerShape = MarkerShape.NONE

	def __post_init__(self) -> None:
		"""
		Check the columns and the colors and replace them with copies that only the chart holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
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
