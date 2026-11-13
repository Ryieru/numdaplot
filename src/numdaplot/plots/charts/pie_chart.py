"""
Chart sharing out a total as slices of a disc.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.chart_settings import copy_colors
from numdaplot.plots.charts.percentages import Percentages
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.tables.columns.column_names import require_column_name


@dataclass(frozen=True)
class PieChart(Chart):
	"""
	Chart drawing each row of a Table as a slice of a disc, sized by its share of the total, used by ``Plot.pie``.

	The slices start at the top and follow each other clockwise, in the order of the rows, each labeled with
	its text. Every value must be present and positive or 0, and every label must be different. Beyond 5 slices,
	a ``ReadabilityWarning`` suggests a ``BarChart``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	labels
		The column of texts, booleans or times of day (written ``HH:MM``) naming the slices.
	values
		The column of numbers sizing the slices.
	percentages
		Whether each slice shows its share, such as ``42.5%``, ``Percentages.SHOWN`` by default.
	colors
		One color per slice, the colors of the default cycle when omitted. The chart keeps its own list.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``labels`` or ``values`` is an empty text.
	EmptyListError
		When ``colors`` is an empty list.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> sales = ndp.Array.from_list([120.0, 80.0, 45.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales")
	>>> plot = ndp.Plot.pie(shares, chart)
	>>> plot.show()
	"""

	labels: str
	values: str
	percentages: Percentages = Percentages.SHOWN
	colors: Sequence[Color | CustomColor] | None = None

	def __post_init__(self) -> None:
		"""
		Check the colors and replace them with a copy that only the chart holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``labels`` or ``values`` is an empty text.
		EmptyListError
			When ``colors`` is an empty list.
		"""
		require_field_types(self)

		require_column_name(self.labels)
		require_column_name(self.values)

		colors_copy = copy_colors(self.colors)
		object.__setattr__(self, "colors", colors_copy)
