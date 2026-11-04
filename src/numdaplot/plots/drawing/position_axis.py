"""
Placement of the ``x`` values of a chart along its axis.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Any, cast

import numpy
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter
from numpy.typing import NDArray

from numdaplot.arrays.conversion.time_text import format_datetimes
from numdaplot.plots.data.chart_values import Positions
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.drawing.whole_numbers import place_whole_ticks

DAY_UNIT = "D"
DAY_DTYPE = numpy.dtype("datetime64[D]")
TRIMMED_ZEROS = "-"


def place_positions(axes: Axes, positions: Positions, on_vertical_axis: bool) -> NDArray[Any]:
	"""
	Return the coordinates of the ``x`` values of a line or scatter chart, and set the ticks of their axis.

	Numbers keep their value, with ticks on whole numbers only when every number is whole, moments are
	placed on a time axis, and texts are placed at 0, 1, 2 and so on, each labeled with its text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	positions
		The ``x`` values.
	on_vertical_axis
		True to place them on the vertical axis.

	Returns
	-------
	NDArray
		The coordinates given to matplotlib.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> from numdaplot.plots.drawing.position_axis import place_positions
	>>> axes = Figure().add_subplot()
	>>> place_positions(axes, Positions(PositionKind.TEXTS, numpy.array(["Paris", "Lyon"]), "city"), False)
	array([0., 1.])
	>>> [label.get_text() for label in axes.get_xticklabels()]
	['Paris', 'Lyon']
	"""
	if positions.kind == PositionKind.TEXTS:
		categories = place_categories(axes, positions, on_vertical_axis)
		return categories

	position_axis = find_axis(axes, on_vertical_axis)
	if positions.kind == PositionKind.NUMBERS:
		place_whole_ticks(position_axis, positions.values)
		return positions.values

	if positions.kind == PositionKind.MOMENTS:
		date_locator = AutoDateLocator()
		date_formatter = ConciseDateFormatter(date_locator)
		position_axis.set_major_locator(date_locator)
		position_axis.set_major_formatter(date_formatter)

	return positions.values


def place_categories(axes: Axes, positions: Positions, on_vertical_axis: bool) -> NDArray[numpy.float64]:
	"""
	Return the coordinates 0, 1, 2 and so on of the ``x`` values, each tick labeled with its value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	positions
		The ``x`` values.
	on_vertical_axis
		True to place them on the vertical axis.

	Returns
	-------
	NDArray[numpy.float64]
		One coordinate per value.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> from numdaplot.plots.drawing.position_axis import place_categories
	>>> axes = Figure().add_subplot()
	>>> place_categories(axes, Positions(PositionKind.NUMBERS, numpy.array([2025.0, 2026.0]), "year"), False)
	array([0., 1.])
	>>> [label.get_text() for label in axes.get_xticklabels()]
	['2025', '2026']
	"""
	position_count = len(positions.values)
	coordinates = numpy.arange(position_count, dtype=numpy.float64)
	labels = write_position_labels(positions)
	position_axis = find_axis(axes, on_vertical_axis)
	position_axis.set_ticks(coordinates, labels)

	return coordinates


def find_axis(axes: Axes, on_vertical_axis: bool) -> Axis:
	"""
	Return the horizontal or the vertical axis of matplotlib axes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes.
	on_vertical_axis
		True for the vertical axis.

	Returns
	-------
	matplotlib.axis.Axis
		The ``yaxis`` or the ``xaxis``.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.position_axis import find_axis
	>>> find_axis(Figure().add_subplot(), True).axis_name
	'y'
	"""
	if on_vertical_axis:
		return axes.yaxis

	return axes.xaxis


def write_position_labels(positions: Positions) -> list[str]:
	"""
	Return the text labeling each ``x`` value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The ``x`` values.

	Returns
	-------
	list[str]
		Numbers without trailing zeros, dates without time when every value is at midnight, texts as they are.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> from numdaplot.plots.drawing.position_axis import write_position_labels
	>>> days = numpy.array(["2026-01-01", "2026-01-02"], dtype="datetime64[ns]")
	>>> write_position_labels(Positions(PositionKind.MOMENTS, days, "day"))
	['2026-01-01', '2026-01-02']
	"""
	if positions.kind == PositionKind.NUMBERS:
		number_labels = [numpy.format_float_positional(value, trim=TRIMMED_ZEROS) for value in positions.values]
		return number_labels

	if positions.kind == PositionKind.MOMENTS:
		moment_labels = write_moment_labels(positions.values)
		return moment_labels

	text_labels = [str(value) for value in positions.values]

	return text_labels


def write_moment_labels(moments: NDArray[numpy.datetime64]) -> list[str]:
	"""
	Return the text of each date or datetime, without time when every value is at midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	moments
		datetime64 values.

	Returns
	-------
	list[str]
		One text per value, ``NaT`` for a missing value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.position_axis import write_moment_labels
	>>> write_moment_labels(numpy.array(["2026-01-01T10:30"], dtype="datetime64[ns]"))
	['2026-01-01 10:30:00']
	"""
	days = moments.astype(DAY_DTYPE)
	day_starts = days.astype(moments.dtype)
	at_midnight = day_starts == moments
	missing = numpy.isnat(moments)
	is_whole_day = at_midnight | missing
	all_whole_days = bool(numpy.all(is_whole_day))
	if all_whole_days:
		day_texts = numpy.datetime_as_string(days, unit=DAY_UNIT)
		# Some versions of the numpy stubs type the list of a text array as nested lists.
		day_labels = cast(list[str], day_texts.tolist())
		return day_labels

	moment_texts = format_datetimes(moments)
	moment_labels = cast(list[str], moment_texts.tolist())

	return moment_labels
