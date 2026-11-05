"""
Labels of a time axis, with a corner label giving the period of the drawn values.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the arguments of the date functions and of the shared axes untyped.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from typing import cast

from matplotlib.axes import Axes
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, num2date

# strftime turns each %% into %, so the corner label matplotlib writes is the format to read the period with.
PERIOD_FORMATS = ["", "%%Y", "%%Y-%%b", "%%Y-%%b-%%d", "%%Y-%%b-%%d", "%%Y-%%b-%%d %%H:%%M"]
PERIOD_TEXT = "{start} to {stop}"


class MomentPeriodFormatter(ConciseDateFormatter):
	"""
	The concise labels of matplotlib, with a corner label giving the period of the visible values.

	matplotlib writes the date of the last tick in that corner, which can be a month without any value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	locator
		The locator choosing the ticks of the axis.
	axes
		The matplotlib axes drawn on.
	on_vertical_axis
		True when the moments are on the vertical axis.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.dates import AutoDateLocator
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.moment_period_formatter import MomentPeriodFormatter
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> days = numpy.array(["2019-03-01", "2019-03-31"], dtype="datetime64[ns]")
	>>> _ = axes.plot(days, [1.0, 2.0])
	>>> locator = AutoDateLocator()
	>>> axes.xaxis.set_major_locator(locator)
	>>> axes.xaxis.set_major_formatter(MomentPeriodFormatter(locator, axes, False))
	>>> figure.draw_without_rendering()
	>>> axes.xaxis.get_offset_text().get_text()
	'2019-Mar'
	"""

	def __init__(self, locator: AutoDateLocator, axes: Axes, on_vertical_axis: bool) -> None:
		super().__init__(locator, offset_formats=PERIOD_FORMATS)
		self.drawn_axes = axes
		self.on_vertical_axis = on_vertical_axis

	def get_offset(self) -> str:
		"""
		Return the text of the corner label.

		.. versionadded:: 0.1.0

		Returns
		-------
		str
			The period of the visible values, as one value or as two values separated by ``to``,
			and an empty text when the ticks already give it.

		Examples
		--------
		>>> import numpy
		>>> from matplotlib.dates import AutoDateLocator
		>>> from matplotlib.figure import Figure
		>>> from numdaplot.plots.drawing.moment_period_formatter import MomentPeriodFormatter
		>>> figure = Figure()
		>>> axes = figure.add_subplot()
		>>> days = numpy.array(["2019-03-15", "2019-05-15"], dtype="datetime64[ns]")
		>>> _ = axes.plot(days, [1.0, 2.0])
		>>> locator = AutoDateLocator()
		>>> axes.xaxis.set_major_locator(locator)
		>>> formatter = MomentPeriodFormatter(locator, axes, False)
		>>> axes.xaxis.set_major_formatter(formatter)
		>>> figure.draw_without_rendering()
		>>> formatter.get_offset()
		'2019-Mar to 2019-May'
		"""
		period_format = super().get_offset()
		if period_format == "":
			return ""

		start, stop = find_visible_period(self.drawn_axes, self.on_vertical_axis)
		period_text = write_period(start, stop, period_format)

		return period_text


def find_visible_period(axes: Axes, on_vertical_axis: bool) -> tuple[float, float]:
	"""
	Return the first and the last visible coordinates holding values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	on_vertical_axis
		True when the moments are on the vertical axis.

	Returns
	-------
	tuple[float, float]
		The start and the stop of the visible values, or of the visible axis when it shows no value.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.moment_period_formatter import find_visible_period
	>>> axes = Figure().add_subplot()
	>>> _ = axes.plot([10.0, 20.0], [1.0, 2.0])
	>>> find_visible_period(axes, False)
	(10.0, 20.0)
	"""
	view_start, view_stop = find_view_bounds(axes, on_vertical_axis)
	data_start, data_stop = find_data_bounds(axes, on_vertical_axis)
	visible_start = max(view_start, data_start)
	visible_stop = min(view_stop, data_stop)
	if visible_start > visible_stop:
		return view_start, view_stop

	return visible_start, visible_stop


def find_data_bounds(axes: Axes, on_vertical_axis: bool) -> tuple[float, float]:
	"""
	Return the lowest and the highest coordinates of the values of axes and of the axes sharing their axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	on_vertical_axis
		True when the moments are on the vertical axis.

	Returns
	-------
	tuple[float, float]
		The two bounds. The low bound is above the high bound without any value.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.moment_period_formatter import find_data_bounds
	>>> axes = Figure().add_subplot()
	>>> right_axes = axes.twinx()
	>>> _ = axes.plot([10.0, 20.0], [1.0, 2.0])
	>>> _ = right_axes.plot([15.0, 30.0], [1.0, 2.0])
	>>> find_data_bounds(axes, False)
	(10.0, 30.0)
	"""
	shared_axes = axes.get_shared_y_axes() if on_vertical_axis else axes.get_shared_x_axes()
	sibling_axes = cast(list[Axes], shared_axes.get_siblings(axes))
	data_limits = [sibling.dataLim for sibling in sibling_axes]
	low_bounds = [limits.y0 if on_vertical_axis else limits.x0 for limits in data_limits]
	high_bounds = [limits.y1 if on_vertical_axis else limits.x1 for limits in data_limits]
	lowest_bound = min(low_bounds)
	highest_bound = max(high_bounds)
	low_bound = float(lowest_bound)
	high_bound = float(highest_bound)

	return low_bound, high_bound


def find_view_bounds(axes: Axes, on_vertical_axis: bool) -> tuple[float, float]:
	"""
	Return the lowest and the highest visible coordinates of an axis, even when it is inverted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	on_vertical_axis
		True for the vertical axis.

	Returns
	-------
	tuple[float, float]
		The two bounds.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.moment_period_formatter import find_view_bounds
	>>> axes = Figure().add_subplot()
	>>> axes.set_xlim(20.0, 10.0)
	(20.0, 10.0)
	>>> find_view_bounds(axes, False)
	(10.0, 20.0)
	"""
	first_bound, second_bound = axes.get_ybound() if on_vertical_axis else axes.get_xbound()
	low_bound = float(first_bound)
	high_bound = float(second_bound)

	return low_bound, high_bound


def write_period(start: float, stop: float, period_format: str) -> str:
	"""
	Return the text of a period, as one value when both ends read the same.

	.. versionadded:: 0.1.0

	Parameters
	----------
	start
		The matplotlib date number of the start.
	stop
		The matplotlib date number of the stop.
	period_format
		The strftime format of each end.

	Returns
	-------
	str
		The text of the period.

	Examples
	--------
	>>> from datetime import date
	>>> from matplotlib.dates import date2num
	>>> from numdaplot.plots.drawing.moment_period_formatter import write_period
	>>> write_period(date2num(date(2019, 3, 1)), date2num(date(2019, 3, 31)), "%Y-%b")
	'2019-Mar'
	>>> write_period(date2num(date(2019, 11, 1)), date2num(date(2020, 2, 15)), "%Y-%b")
	'2019-Nov to 2020-Feb'
	"""
	start_date = num2date(start)
	stop_date = num2date(stop)
	start_text = start_date.strftime(period_format)
	stop_text = stop_date.strftime(period_format)
	if start_text == stop_text:
		return start_text

	period_text = PERIOD_TEXT.format(start=start_text, stop=stop_text)

	return period_text
