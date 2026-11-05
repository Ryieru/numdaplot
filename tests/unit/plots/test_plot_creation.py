"""
Unit tests of the creation of a Plot from its chart.

.. versionadded:: 0.1.0
"""

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.plot_creation import create_plot

PRICES = ndp.Array.from_list([12.0, 15.5])
LAYER = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
STYLE = ndp.PlotStyle(title="Prices")


def test_create_plot_uses_the_default_style_without_style() -> None:
	"""
	Check that no style gives the default one, without title.

	.. versionadded:: 0.1.0
	"""
	plot = create_plot(LAYER, None)

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == ""


def test_create_plot_uses_the_given_style() -> None:
	"""
	Check that a given style is drawn.

	.. versionadded:: 0.1.0
	"""
	plot = create_plot(LAYER, STYLE)

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == "Prices"
