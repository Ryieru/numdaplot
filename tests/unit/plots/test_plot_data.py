"""
Unit tests of the charts and the style stored by a Plot.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

import pytest

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.plot import Plot

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
LAYER = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
STYLE = ndp.PlotStyle(title="Prices")


def test_plot_refuses_its_constructor() -> None:
	"""
	Check that creating a Plot by its constructor raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedOperationError):
		Plot()


def test_plot_keeps_its_own_copy_of_the_layers() -> None:
	"""
	Check that changing the given list changes nothing in the Plot.

	.. versionadded:: 0.1.0
	"""
	layers = [LAYER]
	plot = Plot._create(layers, STYLE)

	layers.clear()

	figure = plot.to_matplotlib()
	line_count = len(figure.axes[0].lines)
	assert line_count == 1


def test_create_from_layer_uses_the_default_style_without_style() -> None:
	"""
	Check that no style gives the default one, without title.

	.. versionadded:: 0.1.0
	"""
	plot = Plot._create_from_layer(LAYER, None)

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == ""


def test_create_from_layer_uses_the_given_style() -> None:
	"""
	Check that a given style is drawn.

	.. versionadded:: 0.1.0
	"""
	plot = Plot._create_from_layer(LAYER, STYLE)

	figure = plot.to_matplotlib()
	assert figure.axes[0].get_title() == "Prices"
