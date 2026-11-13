"""
Chart coloring each value of a grid of numbers.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.plots.charts.cell_values import CellValues
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.color_scale import ColorScale
from numdaplot.tables.columns.column_names import copy_optional_column_names, require_optional_column_name


@dataclass(frozen=True)
class HeatmapChart(Chart):
	"""
	Chart drawing each value as a cell colored along a color scale, used by ``Plot.heatmap``.

	The columns are side by side and the rows go down from the first one. A color bar next to the cells shows
	the scale. A missing value leaves its cell light gray.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		For a Table, the columns drawn, holding numbers. A Table needs it, even for a single column. An Array of one or
		two dimensions takes none: when omitted, each of its columns is drawn.
	labels
		For a Table, the column labeling the rows: numbers, dates, datetimes, times of day (labeled ``HH:MM``), texts or
		booleans, the row numbers when omitted. A row whose label text is missing is left out. An Array takes none, its
		rows being numbered.
	scale
		The colors of the cells, ``ColorScale.VIRIDIS`` by default.
	values
		Whether each cell shows its value, ``CellValues.HIDDEN`` by default.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``labels`` or a name in ``columns`` is an empty text.
	EmptyListError
		When ``columns`` is an empty list.
	DuplicateColumnError
		When a column name appears twice in ``columns``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", values=ndp.CellValues.SHOWN)
	>>> plot = ndp.Plot.heatmap(temperatures, chart)
	>>> plot.show()
	"""

	columns: list[str] | None = None
	labels: str | None = None
	scale: ColorScale = ColorScale.VIRIDIS
	values: CellValues = CellValues.HIDDEN

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the chart holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``labels`` or a name in ``columns`` is an empty text.
		EmptyListError
			When ``columns`` is an empty list.
		DuplicateColumnError
			When a column name appears twice in ``columns``.
		"""
		require_field_types(self)

		require_optional_column_name(self.labels)

		columns_copy = copy_optional_column_names(self.columns)
		object.__setattr__(self, "columns", columns_copy)
