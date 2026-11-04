"""
Chart coloring each value of a grid of numbers.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.charts.cell_values import CellValues
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.chart_settings import copy_columns
from numdaplot.plots.charts.color_scale import ColorScale


@dataclass(frozen=True)
class HeatmapChart(Chart):
	"""
	Chart drawing each value as a cell colored along a color scale, used by ``plot_heatmap``.

	The columns are side by side and the rows go down from the first one. A color bar next to the cells shows
	the scale. A missing value leaves its cell light gray.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		For a Table, the columns drawn, holding numbers. A Table needs it, even for a single column.
		An Array of one or two dimensions takes none, each of its columns being drawn.
	labels
		For a Table, the column labeling the rows: numbers, dates, datetimes or texts, the row numbers when
		omitted. A row whose label text is missing is left out. An Array takes none, its rows being numbered.
	scale
		The colors of the cells, ``ColorScale.VIRIDIS`` by default.
	values
		Whether each cell shows its value, ``CellValues.HIDDEN`` by default.

	Raises
	------
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
	>>> plot = ndp.plot_heatmap(temperatures, chart)
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
		EmptyListError
			When ``columns`` is an empty list.
		DuplicateColumnError
			When a column name appears twice in ``columns``.
		"""
		columns_copy = copy_columns(self.columns)
		object.__setattr__(self, "columns", columns_copy)
