"""
The ``ndp.Plot`` class: a drawn view of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.plot_distribution_creation import PlotDistributionCreation
from numdaplot.plots.plot_output import PlotOutput
from numdaplot.plots.plot_overlays import PlotOverlays
from numdaplot.plots.plot_overview_creation import PlotOverviewCreation
from numdaplot.plots.plot_series_creation import PlotSeriesCreation


class Plot(PlotSeriesCreation, PlotDistributionCreation, PlotOverviewCreation, PlotOverlays, PlotOutput):
	"""
	A drawn view of a Table or an Array, made by creation methods such as ``Plot.line``.

	A Plot is immutable: it keeps the values it was made from, so changing the data afterwards never changes it.
	It is only displayed by ``show``, never on its own in a notebook.

	Calling ``ndp.Plot(...)`` is refused with ``RefusedOperationError``, which names the methods to use instead.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> plot = ndp.Plot.line(prices)
	>>> plot.show()
	"""
