"""
Checks shared by the column and color settings of the charts.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from numdaplot.argument_checks.column_names import copy_optional_column_names, require_optional_column_name
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

if TYPE_CHECKING:
	from numdaplot.plots.charts.bar_chart import BarChart
	from numdaplot.plots.charts.line_chart import LineChart

COLOR_ITEM_NAME = "color"


def copy_colors(colors: Sequence[Color | CustomColor] | None) -> list[Color | CustomColor] | None:
	"""
	Check the colors of the series of a chart and return a copy that only the chart holds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	colors
		One color per series, in a list or another sequence, or None for the colors of the default cycle.

	Returns
	-------
	list[Color | CustomColor] or None
		A copy of the colors, or None.

	Raises
	------
	EmptyListError
		When the list is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.charts.chart_settings import copy_colors
	>>> try:
	... 	copy_colors([])
	... except ndp.EmptyListError as error:
	... 	print(error)
	Expected at least one color, got an empty list.
	"""
	if colors is None:
		return None

	color_count = len(colors)
	if color_count == 0:
		raise EmptyListError(COLOR_ITEM_NAME)

	colors_copy = list(colors)

	return colors_copy


def copy_series_settings(chart: BarChart | LineChart) -> None:
	"""
	Check the columns and the colors of a chart drawing series, and replace them with copies that only it holds.

	.. versionadded:: 0.2.0

	Parameters
	----------
	chart
		A chart whose ``x`` column labels the positions, whose ``y`` columns are the series and whose ``colors`` are
		one per series.

	Raises
	------
	InvalidColumnNameError
		When ``x`` or a name in ``y`` is an empty text.
	EmptyListError
		When ``y`` or ``colors`` is an empty list.
	DuplicateColumnError
		When a column name appears twice in ``y``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.charts.chart_settings import copy_series_settings
	>>> chart = ndp.LineChart(x="day", y=["price"])
	>>> copy_series_settings(chart)
	>>> chart.y
	['price']
	"""
	require_optional_column_name(chart.x)
	columns_copy = copy_optional_column_names(chart.y)
	colors_copy = copy_colors(chart.colors)
	object.__setattr__(chart, "y", columns_copy)
	object.__setattr__(chart, "colors", colors_copy)
