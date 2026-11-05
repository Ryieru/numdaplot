"""
Checks shared by the column and color settings of the charts.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.tables.columns.column_names import require_column_names

COLUMN_ITEM_NAME = "column"
COLOR_ITEM_NAME = "color"


def copy_columns(columns: list[str] | None) -> list[str] | None:
	"""
	Check the names of the columns a chart draws and return a copy that only the chart holds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		The names of the columns, or None for an Array.

	Returns
	-------
	list[str] or None
		A copy of the names, or None.

	Raises
	------
	EmptyListError
		When the list is empty.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.charts.chart_settings import copy_columns
	>>> try:
	... 	copy_columns(["price", "price"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'price' appears more than once.
	"""
	if columns is None:
		return None

	if columns == []:
		raise EmptyListError(COLUMN_ITEM_NAME)

	require_column_names(columns)
	columns_copy = list(columns)

	return columns_copy


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
