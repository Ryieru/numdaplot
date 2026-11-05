"""
Look of a whole Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_rotation_error import InvalidRotationError
from numdaplot.plots.style.grid_lines import GridLines
from numdaplot.plots.style.legend_position import LegendPosition
from numdaplot.plots.style.size import Size

MINIMUM_ROTATION = -90
MAXIMUM_ROTATION = 90


@dataclass(frozen=True)
class PlotStyle:
	"""
	Look of a whole Plot: title, axis labels, rotation of the values, legend, grid lines and size.

	The look of the series, such as their colors, belongs to the chart drawing them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	title
		The title above the axes, no title when omitted.
	x_label
		The label of the axis of the ``x`` values, the name of the ``x`` column when omitted. An empty text draws no
		label.
	y_label
		The label of the axis of the ``y`` values: when omitted, the name of the ``y`` column when the chart draws a
		single one, no label otherwise, the legend naming the series. An empty text draws no label.
	right_label
		The label of the axis on the right, drawn when a chart is added with ``ValueAxis.RIGHT``: when omitted, the name
		of the column of the first chart on the right when it draws a single one. An empty text draws no label. It has
		no effect while no chart is on the right.
	x_tick_rotation
		The angle of the labels of the ``x`` values, in degrees from -90 to 90. When omitted, 45 degrees for texts,
		dates and datetimes, and no rotation for numbers and for the texts on the left of horizontal bars.
	y_tick_rotation
		The angle of the labels of the ``y`` values, in degrees from -90 to 90, no rotation when omitted. The values of
		the axis on the right keep no rotation.
	legend
		Where the legend is placed, ``LegendPosition.BEST`` by default. It is only drawn for several series, so never on
		a pie or a heatmap.
	grid_lines
		Whether light grid lines are drawn behind the values, ``GridLines.SHOWN`` by default. A pie and a heatmap have
		none.
	size
		The width and the height, 6.4 by 4.8 inches by default. A Plot placed in a ``Figure`` takes the size of
		its cells instead.

	Raises
	------
	InvalidRotationError
		When ``x_tick_rotation`` or ``y_tick_rotation`` is outside -90 to 90 degrees.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(title="Sales", x_label="Day", y_label="Euros", legend=ndp.LegendPosition.OUTSIDE_RIGHT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()

	The labels of the ``x`` values can take another angle.

	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Marseille"])
	>>> totals = ndp.Array.from_list([120.0, 80.0, 95.0])
	>>> city_sales = ndp.Table.from_arrays({"city": cities, "total": totals})
	>>> city_chart = ndp.BarChart(x="city", y=["total"])
	>>> city_plot = ndp.plot_bar(city_sales, city_chart, ndp.PlotStyle(x_tick_rotation=90))
	>>> city_plot.show()
	"""

	title: str | None = None
	x_label: str | None = None
	y_label: str | None = None
	right_label: str | None = None
	x_tick_rotation: float | None = None
	y_tick_rotation: float | None = None
	legend: LegendPosition = LegendPosition.BEST
	grid_lines: GridLines = GridLines.SHOWN
	size: Size = Size()

	def __post_init__(self) -> None:
		"""
		Check the rotations of the labels of the values.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidRotationError
			When ``x_tick_rotation`` or ``y_tick_rotation`` is outside -90 to 90 degrees.
		"""
		for rotation in (self.x_tick_rotation, self.y_tick_rotation):
			if rotation is None:
				continue

			is_accepted = MINIMUM_ROTATION <= rotation <= MAXIMUM_ROTATION
			if not is_accepted:
				raise InvalidRotationError(rotation)
