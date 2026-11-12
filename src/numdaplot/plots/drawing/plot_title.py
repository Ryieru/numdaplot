"""
Title of a Plot, centered on the whole area of the Plot and broken into lines when it is too wide.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

from matplotlib.axes import Axes
from matplotlib.figure import Figure, SubFigure
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import text_to_path

from numdaplot.plots.drawing.label_room import POINTS_PER_INCH

# Share of the width of the Plot left free on each side of a title broken into lines.
TITLE_SIDE_MARGIN = 0.02
SIDE_COUNT = 2
LINE_BREAK = "\n"
WORD_SEPARATOR = " "


def write_title(axes: Axes, title: str) -> None:
	"""
	Write the title of a Plot above its whole area, the axes and a legend placed past them.

	A title wider than the area, less a small margin on each side, goes on several lines.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The main matplotlib axes of the Plot, in the figure or subfigure of the Plot.
	title
		The title, nothing written when it is empty.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.plot_title import write_title
	>>> figure = Figure(figsize=(3.0, 2.0))
	>>> axes = figure.add_subplot()
	>>> write_title(axes, "Monthly sales of every shop of the company")
	>>> print(figure.get_suptitle())
	Monthly sales of every shop of
	the company
	"""
	if title == "":
		return

	plot_area = cast(Figure | SubFigure, axes.get_figure(root=False))
	title_text = plot_area.suptitle(title)
	area_points = plot_area.bbox.width * POINTS_PER_INCH / plot_area.dpi
	free_points = area_points * TITLE_SIDE_MARGIN
	margin_points = free_points * SIDE_COUNT
	width_limit = area_points - margin_points
	title_font = title_text.get_fontproperties()
	given_lines = title.split(LINE_BREAK)
	wrapped_lines = [wrap_line(given_line, title_font, width_limit) for given_line in given_lines]
	wrapped_title = LINE_BREAK.join(wrapped_lines)
	title_text.set_text(wrapped_title)


def wrap_line(line: str, font: FontProperties, width_limit: float) -> str:
	"""
	Return a line broken between its words so that each part fits a width.

	.. versionadded:: 0.2.0

	Parameters
	----------
	line
		A line of the title, without line break.
	font
		The font of the title.
	width_limit
		The widest a part may be, in points.

	Returns
	-------
	str
		The parts joined by line breaks. A single word wider than the limit stays whole on its own line.

	Examples
	--------
	>>> from matplotlib.font_manager import FontProperties
	>>> from numdaplot.plots.drawing.plot_title import wrap_line
	>>> print(wrap_line("Missing ratio of the diabetics", FontProperties(size=13.0), 100.0))
	Missing ratio
	of the
	diabetics
	"""
	words = line.split(WORD_SEPARATOR)
	parts = list[str]()
	current_part = words[0]

	for word in words[1:]:
		longer_part = current_part + WORD_SEPARATOR + word
		longer_width = measure_text_width(longer_part, font)
		if longer_width <= width_limit:
			current_part = longer_part
			continue

		parts.append(current_part)
		current_part = word

	parts.append(current_part)
	wrapped_line = LINE_BREAK.join(parts)

	return wrapped_line


def measure_text_width(text: str, font: FontProperties) -> float:
	"""
	Return the width of a text written with a font.

	.. versionadded:: 0.2.0

	Parameters
	----------
	text
		A text on one line.
	font
		The font of the text.

	Returns
	-------
	float
		The width, in points.

	Examples
	--------
	>>> from matplotlib.font_manager import FontProperties
	>>> from numdaplot.plots.drawing.plot_title import measure_text_width
	>>> short_width = measure_text_width("Sales", FontProperties(size=13.0))
	>>> long_width = measure_text_width("Monthly sales", FontProperties(size=13.0))
	>>> bool(short_width < long_width)
	True
	"""
	text_width, _, _ = text_to_path.get_text_width_height_descent(text, font, ismath=False)

	return text_width
