"""
Base class of every chart.

.. versionadded:: 0.1.0
"""


class Chart:
	"""
	Base class of every chart, which says what a Plot draws and how its series look.

	A chart is immutable and checks its settings when it is created.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.BarChart()
	>>> isinstance(chart, ndp.Chart)
	True
	>>> plot = ndp.plot_bar(prices, chart)
	>>> plot.show()
	"""
