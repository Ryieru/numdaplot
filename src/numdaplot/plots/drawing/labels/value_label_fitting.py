"""
Values written on bars, fitted to their bars and given room once the figure is laid out.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from numdaplot.arrays.operations.float_errors import INTERNAL_FILES
from numdaplot.errors.warnings.readability_warning import ReadabilityWarning
from numdaplot.plots.drawing.labels.bar_label_reading import BarLabel, read_bar_labels
from numdaplot.plots.drawing.labels.bar_value_labels import MIDDLE_PLACES, LabelPlace
from numdaplot.plots.drawing.labels.label_room import RIGHT_ANGLE
from numdaplot.plots.drawing.labels.value_label_room import make_label_room

HIDDEN_VALUES_MESSAGE = (
	"The values of {hidden_count} bars do not fit their bars and are not written. Give a larger ndp.Size, or fewer "
	"decimals in ValueLabels."
)


def fit_value_labels(figure: Figure) -> None:
	"""
	Fit the values written on bars to their bars, then give the values past the bars room inside the axes.

	The figure is laid out first, so that the bars and the values have their final sizes. Widening the axis of the
	values changes its numbers, so the figure is laid out again and the room checked once more. A figure without
	such a value is left as it is, without these extra layouts.

	.. versionadded:: 0.2.0

	Parameters
	----------
	figure
		A figure whose Plots are drawn.

	Warns
	-----
	ReadabilityWarning
		When some values do not fit their bars, even upright, and are not written.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.labels.value_label_fitting import fit_value_labels
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> bars = axes.bar([0.0, 1.0], [1.0, 2.0])
	>>> axes.set_ylim(0.0, 2.0)
	(0.0, 2.0)
	>>> write_value_labels(axes, bars, ["1.00", "2.00"], LabelPlace.VERTICAL_END)
	>>> fit_value_labels(figure)
	>>> bool(axes.get_ylim()[1] > 2.0)
	True
	"""
	labels_by_axes = list[tuple[Axes, list[BarLabel]]]()

	for axes in figure.axes:
		bar_labels = read_bar_labels(axes)
		if bar_labels:
			labels_by_axes.append((axes, bar_labels))

	if not labels_by_axes:
		return

	figure.draw_without_rendering()
	hidden_count = 0

	for axes, bar_labels in labels_by_axes:
		axes_hidden_count = fit_labels_to_bars(bar_labels)
		hidden_count += axes_hidden_count
		make_label_room(axes, bar_labels)

	figure.draw_without_rendering()

	for axes, bar_labels in labels_by_axes:
		make_label_room(axes, bar_labels)

	if hidden_count > 0:
		message = HIDDEN_VALUES_MESSAGE.format(hidden_count=hidden_count)
		warnings.warn(message, ReadabilityWarning, skip_file_prefixes=INTERNAL_FILES)


def fit_labels_to_bars(bar_labels: list[BarLabel]) -> int:
	"""
	Turn upright the values too wide for vertical bars, and hide the values that still do not fit.

	The values past the end of vertical bars all turn upright as soon as one is too wide, so that they read the same
	way. A value in the middle of a bar turns upright alone, and must fit inside its bar.

	.. versionadded:: 0.2.0

	Parameters
	----------
	bar_labels
		The values written on the bars of one axes, laid out.

	Returns
	-------
	int
		The number of values hidden.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.labels.bar_label_reading import read_bar_labels
	>>> from numdaplot.plots.drawing.labels.value_label_fitting import fit_labels_to_bars
	>>> figure = Figure(figsize=(2.0, 2.0))
	>>> axes = figure.add_subplot()
	>>> bars = axes.bar([float(number) for number in range(8)], [1.0] * 8)
	>>> write_value_labels(axes, bars, ["1234.56"] * 8, LabelPlace.VERTICAL_END)
	>>> figure.draw_without_rendering()
	>>> fit_labels_to_bars(read_bar_labels(axes))
	0
	>>> axes.texts[0].get_rotation()
	90.0
	"""
	end_labels = [bar_label for bar_label in bar_labels if bar_label.place == LabelPlace.VERTICAL_END]
	too_wide_labels = [bar_label for bar_label in end_labels if not fits_across(bar_label)]
	if too_wide_labels:
		for bar_label in end_labels:
			bar_label.text.set_rotation(RIGHT_ANGLE)

	hidden_count = 0

	for bar_label in bar_labels:
		is_fitted = fit_label(bar_label)
		if not is_fitted:
			bar_label.text.set_visible(False)
			hidden_count += 1

	return hidden_count


def fit_label(bar_label: BarLabel) -> bool:
	"""
	Return whether a value fits its bar, turning upright a value in the middle of a vertical bar when it needs to.

	.. versionadded:: 0.2.0

	Parameters
	----------
	bar_label
		A value written on a bar, laid out.

	Returns
	-------
	bool
		True when the value fits across the bar, and along it for a value in its middle.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.labels.bar_label_reading import read_bar_labels
	>>> from numdaplot.plots.drawing.labels.value_label_fitting import fit_label
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> bars = axes.bar([0.0], [1.0])
	>>> write_value_labels(axes, bars, ["1.00"], LabelPlace.VERTICAL_MIDDLE)
	>>> figure.draw_without_rendering()
	>>> fit_label(read_bar_labels(axes)[0])
	True
	"""
	is_middle = bar_label.place in MIDDLE_PLACES
	if not is_middle:
		fits_end = fits_across(bar_label)
		return fits_end

	fits_middle = fits_inside(bar_label)
	if fits_middle:
		return True

	if bar_label.place == LabelPlace.HORIZONTAL_MIDDLE:
		return False

	bar_label.text.set_rotation(RIGHT_ANGLE)
	fits_upright = fits_inside(bar_label)

	return fits_upright


def fits_across(bar_label: BarLabel) -> bool:
	"""
	Return whether a value is no wider than its bar, across the direction of the bar.

	.. versionadded:: 0.2.0

	Parameters
	----------
	bar_label
		A value written on a bar, laid out.

	Returns
	-------
	bool
		True when the value fits the thickness of the bar.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.labels.bar_label_reading import read_bar_labels
	>>> from numdaplot.plots.drawing.labels.value_label_fitting import fits_across
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> bars = axes.bar([0.0], [1.0])
	>>> write_value_labels(axes, bars, ["1.00"], LabelPlace.VERTICAL_END)
	>>> figure.draw_without_rendering()
	>>> fits_across(read_bar_labels(axes)[0])
	True
	"""
	bar_box = bar_label.bar.get_window_extent()
	text_box = bar_label.text.get_window_extent()
	is_horizontal = bar_label.place == LabelPlace.HORIZONTAL_END
	if is_horizontal:
		fits_height = bool(text_box.height <= bar_box.height)
		return fits_height

	fits_width = bool(text_box.width <= bar_box.width)

	return fits_width


def fits_inside(bar_label: BarLabel) -> bool:
	"""
	Return whether a value fits inside its bar, in both directions.

	.. versionadded:: 0.2.0

	Parameters
	----------
	bar_label
		A value written in the middle of a bar, laid out.

	Returns
	-------
	bool
		True when the value is no wider and no taller than the bar.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.labels.bar_label_reading import read_bar_labels
	>>> from numdaplot.plots.drawing.labels.value_label_fitting import fits_inside
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> bars = axes.bar([0.0, 1.0], [1.0, 0.001])
	>>> write_value_labels(axes, bars, ["1.00", "0.00"], LabelPlace.VERTICAL_MIDDLE)
	>>> figure.draw_without_rendering()
	>>> [fits_inside(bar_label) for bar_label in read_bar_labels(axes)]
	[True, False]
	"""
	bar_box = bar_label.bar.get_window_extent()
	text_box = bar_label.text.get_window_extent()
	fits_width = bool(text_box.width <= bar_box.width)
	fits_height = bool(text_box.height <= bar_box.height)
	fits_both = fits_width and fits_height

	return fits_both
