"""
Vertical axis a chart added to a Plot is measured on.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ValueAxis(Enum):
	"""
	Vertical axis a chart added to a Plot with ``add_line``, ``add_bar`` or ``add_scatter`` is measured on.

	A chart on the right axis gets its own scale, so values of different sizes, such as a number of sales and
	a price, can share a Plot.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> months = ndp.Array.from_list(["Jan", "Feb", "Mar", "Apr"])
	>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0])
	>>> prices = ndp.Array.from_list([12.5, 11.0, 14.0, 10.5])
	>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "price": prices})
	>>> style = ndp.Style(legend=ndp.LegendPosition.UPPER_LEFT)
	>>> plot = ndp.plot_bar(shop, ndp.BarChart(x="month", y=["sales"]), style)
	>>> line = ndp.LineChart(x="month", y=["price"], marker=ndp.MarkerShape.CIRCLE)
	>>> both = plot.add_line(shop, line, axis=ndp.ValueAxis.RIGHT)
	>>> both.show()
	"""

	LEFT = auto()
	"""
	The axis on the left, shared with the first chart of the Plot. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> months = ndp.Array.from_list(["Jan", "Feb", "Mar", "Apr"])
	>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0])
	>>> targets = ndp.Array.from_list([130.0, 130.0, 140.0, 140.0])
	>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "target": targets})
	>>> plot = ndp.plot_bar(shop, ndp.BarChart(x="month", y=["sales"]))
	>>> line = ndp.LineChart(x="month", y=["target"], line=ndp.LineType.DASHED)
	>>> both = plot.add_line(shop, line, axis=ndp.ValueAxis.LEFT)
	>>> both.show()
	"""

	RIGHT = auto()
	"""
	A second axis on the right, with its own scale and label.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> months = ndp.Array.from_list(["Jan", "Feb", "Mar", "Apr"])
	>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0])
	>>> prices = ndp.Array.from_list([12.5, 11.0, 14.0, 10.5])
	>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "price": prices})
	>>> style = ndp.Style(y_label="Sales", right_label="Price (euros)", legend=ndp.LegendPosition.UPPER_LEFT)
	>>> plot = ndp.plot_bar(shop, ndp.BarChart(x="month", y=["sales"]), style)
	>>> line = ndp.LineChart(x="month", y=["price"], marker=ndp.MarkerShape.CIRCLE)
	>>> both = plot.add_line(shop, line, axis=ndp.ValueAxis.RIGHT)
	>>> both.show()
	"""
