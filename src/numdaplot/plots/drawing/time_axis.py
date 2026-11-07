"""
Axes of times of day, counted in hours since midnight and labeled ``HH:MM``.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from matplotlib.axis import Axis
from matplotlib.ticker import FuncFormatter, MultipleLocator
from numpy.typing import NDArray

MINUTES_PER_HOUR = 60
HOUR_LABEL = "{hour:02d}:{minute:02d}"
# The step between two labels, in hours, for the widest span of times it fits, in hours.
HOUR_STEPS = ((1.0, 0.25), (3.0, 0.5), (6.0, 1.0), (12.0, 2.0))
LONGEST_HOUR_STEP = 3.0


def format_hour(hours: float, _position: object = None) -> str:
	"""
	Return a number of hours since midnight as ``HH:MM``, rounded to the minute.

	.. versionadded:: 0.1.0

	Parameters
	----------
	hours
		The hours since midnight, such as 15.5.
	_position
		The position of the label, given by matplotlib and not used.

	Returns
	-------
	str
		The time, such as ``15:30``.

	Examples
	--------
	>>> from numdaplot.plots.drawing.time_axis import format_hour
	>>> format_hour(15.5), format_hour(0.0), format_hour(24.0)
	('15:30', '00:00', '24:00')
	"""
	minutes = hours * MINUTES_PER_HOUR
	whole_minutes = round(minutes)
	hour, minute = divmod(whole_minutes, MINUTES_PER_HOUR)
	hour_label = HOUR_LABEL.format(hour=hour, minute=minute)

	return hour_label


def choose_hour_step(hours: NDArray[numpy.float64]) -> float:
	"""
	Return the step between two labels of an axis of times, from the span of the times.

	.. versionadded:: 0.1.0

	Parameters
	----------
	hours
		The hours since midnight shown on the axis, NaN where missing.

	Returns
	-------
	float
		A quarter of an hour for an hour or less, then half an hour, one, two or three hours.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.time_axis import choose_hour_step
	>>> choose_hour_step(numpy.array([8.0, 23.0])), choose_hour_step(numpy.array([8.0, 8.5]))
	(3.0, 0.25)
	"""
	present_hours = hours[~numpy.isnan(hours)]
	if present_hours.size == 0:
		return LONGEST_HOUR_STEP

	earliest_hour = present_hours.min()
	latest_hour = present_hours.max()
	span = float(latest_hour - earliest_hour)
	for widest_span, step in HOUR_STEPS:
		if span <= widest_span:
			return step

	return LONGEST_HOUR_STEP


def place_hour_ticks(axis: Axis, hours: NDArray[Any]) -> None:
	"""
	Place labels ``HH:MM`` on an axis counted in hours since midnight, at a regular step.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		A matplotlib axis.
	hours
		The hours since midnight shown on the axis.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.time_axis import place_hour_ticks
	>>> axes = Figure().add_subplot()
	>>> _ = axes.plot([8.0, 14.0], [1.0, 2.0])
	>>> place_hour_ticks(axes.xaxis, numpy.array([8.0, 14.0]))
	>>> axes.figure.canvas.draw()
	>>> [label.get_text() for label in axes.get_xticklabels()][1:4]
	['08:00', '09:00', '10:00']
	"""
	step = choose_hour_step(hours)
	locator = MultipleLocator(step)
	formatter = FuncFormatter(format_hour)
	axis.set_major_locator(locator)
	axis.set_major_formatter(formatter)
