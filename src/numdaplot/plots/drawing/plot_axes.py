"""
Axes a Plot is drawn on.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from matplotlib.axes import Axes


@dataclass(frozen=True, eq=False)
class PlotAxes:
	"""
	The matplotlib axes a Plot is drawn on: the main ones, and the ones of the axis on the right if any.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The main axes, measured on the left.
	right
		The axes sharing the ``x`` values and measured on the right, or None without chart on the right.
	right_label
		The default label of the axis on the right: the single column of its first chart, or None.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.plot_axes import PlotAxes
	>>> PlotAxes(Figure().add_subplot(), None, None).right is None
	True
	"""

	left: Axes
	right: Axes | None
	right_label: str | None
