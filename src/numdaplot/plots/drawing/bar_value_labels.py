"""
Values written on the bars of a BarChart.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from enum import Enum
from typing import cast

import numpy
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
from matplotlib.container import BarContainer
from numpy.typing import NDArray

from numdaplot.data_types.number_types import INTEGER_TYPES
from numdaplot.data_types.type import Type
from numdaplot.plots.charts.value_labels import ValueLabels
from numdaplot.plots.drawing.text_contrast import DARK_TEXT_COLOR, choose_text_color

BAR_LABEL_FONT_SIZE = 9
BAR_LABEL_PADDING = 3
NO_PADDING = 0
END_LABEL_TYPE = "edge"
MIDDLE_LABEL_TYPE = "center"
LABELED_BAR_ID = "numdaplot-labeled-bar"
DECIMAL_LABEL_FORMAT = "{value:.{decimals}f}"


class LabelPlace(Enum):
	"""
	Where a value is written on its bar, and the direction of the bar, kept as the id of the label.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace
	>>> LabelPlace.VERTICAL_END.value
	'numdaplot-value-vertical-end'
	"""

	VERTICAL_END = "numdaplot-value-vertical-end"
	"""
	Past the end of a vertical bar, above it or below a negative one.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, find_label_place
	>>> find_label_place(False, False)
	<LabelPlace.VERTICAL_END: 'numdaplot-value-vertical-end'>
	"""

	HORIZONTAL_END = "numdaplot-value-horizontal-end"
	"""
	Past the end of a horizontal bar, on its right or on the left of a negative one.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, find_label_place
	>>> find_label_place(True, False)
	<LabelPlace.HORIZONTAL_END: 'numdaplot-value-horizontal-end'>
	"""

	VERTICAL_MIDDLE = "numdaplot-value-vertical-middle"
	"""
	In the middle of a vertical stacked bar.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, find_label_place
	>>> find_label_place(False, True)
	<LabelPlace.VERTICAL_MIDDLE: 'numdaplot-value-vertical-middle'>
	"""

	HORIZONTAL_MIDDLE = "numdaplot-value-horizontal-middle"
	"""
	In the middle of a horizontal stacked bar.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, find_label_place
	>>> find_label_place(True, True)
	<LabelPlace.HORIZONTAL_MIDDLE: 'numdaplot-value-horizontal-middle'>
	"""


LABEL_PLACES = {
	(False, False): LabelPlace.VERTICAL_END,
	(True, False): LabelPlace.HORIZONTAL_END,
	(False, True): LabelPlace.VERTICAL_MIDDLE,
	(True, True): LabelPlace.HORIZONTAL_MIDDLE,
}
MIDDLE_PLACES = frozenset({LabelPlace.VERTICAL_MIDDLE, LabelPlace.HORIZONTAL_MIDDLE})


def find_label_place(is_horizontal: bool, is_stacked: bool) -> LabelPlace:
	"""
	Return where the values of a BarChart are written: past the end of each bar, or in the middle of stacked bars.

	.. versionadded:: 0.2.0

	Parameters
	----------
	is_horizontal
		True for horizontal bars.
	is_stacked
		True for stacked bars.

	Returns
	-------
	LabelPlace
		The place of the labels.

	Examples
	--------
	>>> from numdaplot.plots.drawing.bar_value_labels import find_label_place
	>>> find_label_place(False, True).name
	'VERTICAL_MIDDLE'
	"""
	label_place = LABEL_PLACES[(is_horizontal, is_stacked)]

	return label_place


def format_value_labels(lengths: NDArray[numpy.float64], value_labels: ValueLabels, value_type: Type) -> list[str]:
	"""
	Return the text of each value, rounded to the decimals asked, whole integers without decimals.

	.. versionadded:: 0.2.0

	Parameters
	----------
	lengths
		The values of the bars drawn, without missing value.
	value_labels
		The number of decimals.
	value_type
		The type of the values of the chart.

	Returns
	-------
	list[str]
		One text per value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.bar_value_labels import format_value_labels
	>>> format_value_labels(numpy.array([0.523, 1.0]), ndp.ValueLabels(), ndp.Type.FLOAT64)
	['0.52', '1.00']
	>>> format_value_labels(numpy.array([12.0]), ndp.ValueLabels(), ndp.Type.INT64)
	['12']
	"""
	is_integer_type = value_type in INTEGER_TYPES
	raw_values = lengths.tolist()
	# Some versions of the numpy stubs type the list of a one-dimensional array as a single float.
	values = cast(list[float], raw_values)
	label_texts = list[str]()

	for value in values:
		float_value = float(value)
		is_whole_integer = is_integer_type and float_value.is_integer()
		if is_whole_integer:
			whole_value = int(float_value)
			whole_text = str(whole_value)
			label_texts.append(whole_text)
			continue

		decimal_text = DECIMAL_LABEL_FORMAT.format(value=float_value, decimals=value_labels.decimals)
		label_texts.append(decimal_text)

	return label_texts


def write_value_labels(axes: Axes, bars: BarContainer, label_texts: list[str], label_place: LabelPlace) -> None:
	"""
	Write a text on each bar of a series, and mark the bars and their texts for the fitting after the layout.

	A text in the middle of a bar is black or white, whichever is readable over the color of the bar.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes holding the bars.
	bars
		The bars of one series.
	label_texts
		One text per bar.
	label_place
		Where the texts are written, kept as their id.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, write_value_labels
	>>> axes = Figure().add_subplot()
	>>> bars = axes.bar([0.0, 1.0], [0.52, 0.18])
	>>> write_value_labels(axes, bars, ["0.52", "0.18"], LabelPlace.VERTICAL_END)
	>>> [text.get_text() for text in axes.texts]
	['0.52', '0.18']
	"""
	bar_count = len(bars.patches)
	if bar_count == 0:
		return

	is_middle = label_place in MIDDLE_PLACES
	label_type = MIDDLE_LABEL_TYPE if is_middle else END_LABEL_TYPE
	padding = NO_PADDING if is_middle else BAR_LABEL_PADDING
	text_color = DARK_TEXT_COLOR
	if is_middle:
		first_bar = bars.patches[0]
		face_color = first_bar.get_facecolor()
		bar_color = to_rgba(face_color)
		text_color = choose_text_color(bar_color)

	axes.bar_label(
		bars,
		labels=label_texts,
		label_type=label_type,
		padding=padding,
		fontsize=BAR_LABEL_FONT_SIZE,
		color=text_color,
		gid=label_place.value,
	)

	for bar in bars.patches:
		bar.set_gid(LABELED_BAR_ID)
