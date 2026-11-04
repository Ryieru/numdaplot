"""
matplotlib codes of the marker shapes.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.charts.marker_shape import MarkerShape

MARKER_CODES = {
	MarkerShape.NONE: "",
	MarkerShape.CIRCLE: "o",
	MarkerShape.SQUARE: "s",
	MarkerShape.TRIANGLE: "^",
	MarkerShape.CROSS: "x",
	MarkerShape.DIAMOND: "D",
}
"""The matplotlib code of each marker shape, an empty code drawing no marker.

.. versionadded:: 0.1.0
"""
