"""
Kind of object a display shows: a Plot or a Figure.

.. versionadded:: 0.1.0
"""

from enum import Enum


class ShownObject(Enum):
	"""
	Kind of object a display shows, named in the message of a ``DisplayWarning``.

	The value is the name of the class.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from numdaplot.plots.output.shown_object import ShownObject
	>>> ShownObject.FIGURE.value
	'Figure'
	"""

	PLOT = "Plot"
	"""
	A Plot, shown with ``Plot.show``.

	Examples
	--------
	>>> from numdaplot.plots.output.shown_object import ShownObject
	>>> ShownObject.PLOT.value
	'Plot'
	"""

	FIGURE = "Figure"
	"""
	A Figure, shown with ``Figure.show``.

	Examples
	--------
	>>> from numdaplot.plots.output.shown_object import ShownObject
	>>> ShownObject.FIGURE.value
	'Figure'
	"""
