"""
Values of a HeatmapChart.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_data import require_column_setting, require_no_column_settings
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.tables.table import Table

CHART_NAME = "HeatmapChart"
COLUMNS_SETTING = "columns"
LABELS_SETTING = "labels"


def read_heatmap_values(data: Table | Array, chart: HeatmapChart) -> ChartValues:
	"""
	Return the row labels and the columns a HeatmapChart draws.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The ``columns`` and the ``labels`` of a Table.

	Returns
	-------
	ChartValues
		The row labels as positions, and one series per column.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``columns``, or an Array has ``columns`` or ``labels``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.heatmap_values import read_heatmap_values
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	>>> try:
	... 	read_heatmap_values(grid, ndp.HeatmapChart(labels="city"))
	... except ndp.InvalidChartDataError as error:
	... 	print(error)
	HeatmapChart takes no labels for an Array.
	"""
	if isinstance(data, Array):
		column_settings = dict[str, object]({COLUMNS_SETTING: chart.columns, LABELS_SETTING: chart.labels})
		require_no_column_settings(CHART_NAME, column_settings)
		array_values = read_array_values(data, CHART_NAME)
		return array_values

	column_names = require_column_setting(CHART_NAME, COLUMNS_SETTING, chart.columns)
	table_values = read_table_values(data, chart.labels, column_names, CHART_NAME)

	return table_values
