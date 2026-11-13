"""
Chart counting the values of each bin.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.measures.measure import Measure
from numdaplot.plots.charts.bin_count import BinCount
from numdaplot.plots.charts.bin_width import BinWidth
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.chart_settings import copy_colors
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.tables.columns.column_names import copy_optional_column_names


@dataclass(frozen=True)
class HistogramChart(Chart):
	"""
	Chart drawing how many values of each column fall in each bin, used by ``Plot.histogram``.

	Several columns share the same bins and are drawn over each other, half transparent. Missing values are
	left out.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		For a Table, the columns drawn, holding numbers or times of day, not both. A Table needs it, even for a
		single column. An Array takes none: when omitted, each of its columns is drawn.
	bins
		The bins, ``BinCount(10)`` for numbers and one bin per hour from 00:00 to 24:00 for times of day when
		omitted, or ``BinWidth`` for bins of a given width: a number for numbers, a duration for times of day.
	measure
		``Measure.COUNT`` by default for the number of values of each bin, ``Measure.RATIO`` for their share
		of the values of the column.
	colors
		One color per column, the colors of the default cycle when omitted. The chart keeps its own list.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When a name in ``columns`` is an empty text.
	EmptyListError
		When ``columns`` or ``colors`` is an empty list.
	DuplicateColumnError
		When a column name appears twice in ``columns``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices_2025 = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 15.0])
	>>> prices_2026 = ndp.Array.from_list([14.0, 17.5, 16.0, 19.0, 15.5, 18.0, 16.5, 17.0])
	>>> prices = ndp.Table.from_arrays({"2025": prices_2025, "2026": prices_2026})
	>>> chart = ndp.HistogramChart(columns=["2025", "2026"], bins=ndp.BinWidth(1.0))
	>>> plot = ndp.Plot.histogram(prices, chart)
	>>> plot.show()
	"""

	columns: list[str] | None = None
	bins: BinCount | BinWidth | None = None
	measure: Measure = Measure.COUNT
	colors: Sequence[Color | CustomColor] | None = None

	def __post_init__(self) -> None:
		"""
		Check the columns and the colors and replace them with copies that only the chart holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When a name in ``columns`` is an empty text.
		EmptyListError
			When ``columns`` or ``colors`` is an empty list.
		DuplicateColumnError
			When a column name appears twice in ``columns``.
		"""
		require_field_types(self)

		columns_copy = copy_optional_column_names(self.columns)
		colors_copy = copy_colors(self.colors)
		object.__setattr__(self, "columns", columns_copy)
		object.__setattr__(self, "colors", colors_copy)
