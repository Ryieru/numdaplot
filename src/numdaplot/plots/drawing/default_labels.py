"""
Default labels of a chart when its data names no column for an axis.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.data.chart_values import Positions

ROW_LABEL = "Row"
COLUMN_LABEL = "Column"


def find_position_label(positions: Positions) -> str:
	"""
	Return the default label of the axis of the positions: the name of their column, else ``Row``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The positions of a chart.

	Returns
	-------
	str
		The label of the axis.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> from numdaplot.plots.drawing.default_labels import find_position_label
	>>> find_position_label(Positions(PositionKind.NUMBERS, numpy.array([0.0]), None))
	'Row'
	"""
	if positions.name is None:
		return ROW_LABEL

	return positions.name
