"""
Charts and style stored by a Plot, shared by every group of Plot methods.

.. versionadded:: 0.1.0
"""

from typing import Never, Self

from matplotlib.figure import FigureBase

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.shown_columns import require_distinct_shown_names
from numdaplot.plots.drawing.plot_drawing import FigureDrawing, draw_plot
from numdaplot.plots.drawing.size_inches import convert_size_to_inches
from numdaplot.plots.style.plot_style import PlotStyle

CONSTRUCTOR_OPERATION = "Creating a Plot with ndp.Plot(...)"
CONSTRUCTOR_ALTERNATIVE = "ndp.Plot.line, bar, scatter, histogram, box, pie, heatmap, missing_by_column or missing_map"


class PlotData:
	"""
	Charts and style stored by a Plot, shared by every group of Plot methods.

	Use ``ndp.Plot`` and its creation methods; this base class only holds the charts and the style.

	.. versionadded:: 0.1.0
	"""

	_layers: list[ChartLayer]
	_style: PlotStyle

	def __init__(self, *arguments: Never, **keyword_arguments: Never) -> None:
		"""
		Refuse the creation of a Plot by its constructor: the creation methods such as ``line`` create Plots.

		.. versionadded:: 0.1.0

		Parameters
		----------
		arguments
			Any value, refused.
		keyword_arguments
			Any named value, refused.

		Raises
		------
		RefusedOperationError
			Always, naming the creation methods.
		"""
		raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)

	@classmethod
	def _create(cls, layers: list[ChartLayer], style: PlotStyle) -> Self:
		"""
		Return a new Plot keeping the charts and the style.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layers
			The charts and their values, made by the creation methods, the first one giving the default labels.
			The Plot keeps its own copy of the list.
		style
			The look of the Plot.

		Returns
		-------
		Self
			The new Plot.

		Raises
		------
		DuplicateColumnError
			When the style shows a column under the name of another column of the charts.
		"""
		require_distinct_shown_names(layers, style.renaming)
		created_plot = cls.__new__(cls)
		created_plot._layers = list(layers)
		created_plot._style = style

		return created_plot

	@classmethod
	def _create_from_layer(cls, layer: ChartLayer, style: PlotStyle | None) -> Self:
		"""
		Return a new Plot drawing one chart, with the default ``PlotStyle`` when none is given.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layer
			The chart and its values.
		style
			The look of the Plot, or None for the default ``PlotStyle``.

		Returns
		-------
		Self
			The Plot of the chart.
		"""
		chosen_style = style
		if chosen_style is None:
			chosen_style = PlotStyle()

		created_plot = cls._create([layer], chosen_style)

		return created_plot

	def _draw_on(self, target: FigureBase) -> None:
		"""
		Draw the Plot on an empty matplotlib figure or subfigure, as ``show``, ``save`` and ``Figure`` do.

		.. versionadded:: 0.1.0

		Parameters
		----------
		target
			The figure or subfigure drawn on.
		"""
		draw_plot(target, self._layers, self._style)

	def _describe_drawing(self) -> FigureDrawing:
		"""
		Return what the Plot draws, and the size of its style.

		.. versionadded:: 0.1.0

		Returns
		-------
		FigureDrawing
			The drawing of the Plot.
		"""
		size_inches = convert_size_to_inches(self._style.size)
		drawing = FigureDrawing(self._draw_on, size_inches)

		return drawing
