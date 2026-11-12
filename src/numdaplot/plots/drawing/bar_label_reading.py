"""
Values written on bars, read back with their bars.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.text import Annotation

from numdaplot.plots.drawing.bar_value_labels import LABELED_BAR_ID, LabelPlace

LABEL_IDS = {label_place.value: label_place for label_place in LabelPlace}


@dataclass(frozen=True)
class BarLabel:
	"""
	A value written on a bar, with its bar and its place.

	.. versionadded:: 0.2.0

	Parameters
	----------
	bar
		The bar.
	text
		The value written, placed by matplotlib from a point of the bar.
	place
		Where the value is written on the bar.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace
	>>> from numdaplot.plots.drawing.bar_label_reading import BarLabel
	>>> axes = Figure().add_subplot()
	>>> bars = axes.bar([0.0], [2.0])
	>>> texts = axes.bar_label(bars)
	>>> BarLabel(bars.patches[0], texts[0], LabelPlace.VERTICAL_END).place.name
	'VERTICAL_END'
	"""

	bar: Patch
	text: Annotation
	place: LabelPlace


def read_bar_labels(axes: Axes) -> list[BarLabel]:
	"""
	Return the values written on the bars of an axes, each with its bar, in the order they were drawn.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		A matplotlib axes.

	Returns
	-------
	list[BarLabel]
		One label per marked bar, empty when no value is written.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.bar_label_reading import read_bar_labels
	>>> axes = Figure().add_subplot()
	>>> bars = axes.bar([0.0, 1.0], [1.0, 2.0])
	>>> write_value_labels(axes, bars, ["1.00", "2.00"], LabelPlace.VERTICAL_END)
	>>> [bar_label.text.get_text() for bar_label in read_bar_labels(axes)]
	['1.00', '2.00']
	"""
	labeled_bars = [patch for patch in axes.patches if patch.get_gid() == LABELED_BAR_ID]
	value_texts = [text for text in axes.texts if text.get_gid() in LABEL_IDS and isinstance(text, Annotation)]
	bar_labels = list[BarLabel]()

	for bar, text in zip(labeled_bars, value_texts, strict=True):
		text_id = str(text.get_gid())
		label_place = LABEL_IDS[text_id]
		bar_label = BarLabel(bar, text, label_place)
		bar_labels.append(bar_label)

	return bar_labels
