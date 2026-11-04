"""
Chart drawing where the values of a Table are missing.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.charts.chart import Chart


@dataclass(frozen=True)
class MissingMapChart(Chart):
	"""
	Chart drawing each value of a Table as a cell, dark when missing, made by ``plot_missing_map``.

	It has no setting, so ``plot_missing_map`` creates it itself.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.charts.missing_map_chart import MissingMapChart
	>>> isinstance(MissingMapChart(), ndp.Chart)
	True
	"""
