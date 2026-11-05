"""
Creation of a Plot from its chart.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.plot import Plot
from numdaplot.plots.style.style import Style


def create_plot(layer: ChartLayer, style: Style | None) -> Plot:
	"""
	Return a Plot drawing one chart, with the default ``Style`` when none is given.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer
		The chart and its values.
	style
		The look of the Plot, or None for the default ``Style``.

	Returns
	-------
	Plot
		The Plot of the chart.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.plot_creation import create_plot
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> plot = create_plot(ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart")), None)
	>>> plot.to_matplotlib().axes[0].get_title()
	''
	"""
	chosen_style = style
	if chosen_style is None:
		chosen_style = Style()

	# The plot_* functions create every Plot, from outside the class.
	plot = Plot._create([layer], chosen_style)  # pyright: ignore[reportPrivateUsage]

	return plot
