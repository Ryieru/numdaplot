"""
Ticks of an axis holding whole numbers only.

.. versionadded:: 0.1.0
"""

import numpy
from matplotlib.axis import Axis
from matplotlib.ticker import MaxNLocator
from numpy.typing import NDArray


def has_only_whole_numbers(numbers: NDArray[numpy.float64]) -> bool:
	"""
	Return whether every present number is a whole number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		float64 numbers, NaN where a value is missing.

	Returns
	-------
	bool
		True when no present number has a fraction, such as days or counts.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.axes.whole_numbers import has_only_whole_numbers
	>>> has_only_whole_numbers(numpy.array([1.0, numpy.nan, 3.0]))
	True
	"""
	present = ~numpy.isnan(numbers)
	present_numbers = numbers[present]
	rounded_numbers = numpy.round(present_numbers)
	is_whole = rounded_numbers == present_numbers
	all_whole = bool(numpy.all(is_whole))

	return all_whole


def place_whole_ticks(axis: Axis, numbers: NDArray[numpy.float64]) -> None:
	"""
	Place the ticks of an axis on whole numbers only, when every number it shows is whole.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		A matplotlib axis.
	numbers
		The numbers shown along the axis.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.axes.whole_numbers import place_whole_ticks
	>>> axes = Figure().add_subplot()
	>>> lines = axes.plot([1.0, 2.0], [5.0, 6.0])
	>>> place_whole_ticks(axes.xaxis, numpy.array([1.0, 2.0]))
	>>> all(float(tick).is_integer() for tick in axes.get_xticks())
	True
	"""
	all_whole = has_only_whole_numbers(numbers)
	if all_whole:
		whole_locator = MaxNLocator(integer=True)
		axis.set_major_locator(whole_locator)
