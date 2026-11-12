"""
Unit tests of the title of a Plot.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import matplotlib
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

from numdaplot.plots.drawing.plot_title import (
	LINE_BREAK,
	TITLE_SIDE_MARGIN,
	measure_text_width,
	wrap_line,
	write_title,
)

SMALL_INCHES = (3.0, 2.0)
SHORT_TITLE = "Sales"
LONG_TITLE = "Monthly sales of every shop of the company, for each product sold during the year"
GIVEN_LINES_TITLE = "Sales\nby month"
EXPECTED_GIVEN_LINES = ["Sales", "by month"]
TITLE_FONT = FontProperties(size=13.0)
NARROW_LIMIT = 100.0
LONG_WORD = "Supercalifragilisticexpialidocious"
POINTS_PER_INCH = 72.0
SIDE_COUNT = 2


def test_write_title_writes_nothing_for_an_empty_title() -> None:
	"""
	Check that an empty title leaves the Plot without title.

	.. versionadded:: 0.2.0
	"""
	figure = Figure(figsize=SMALL_INCHES)
	axes = figure.add_subplot()

	write_title(axes, "")

	plot_title = figure.get_suptitle()
	assert plot_title == ""


def test_write_title_keeps_a_short_title_on_one_line() -> None:
	"""
	Check that a title fitting the width stays as it is.

	.. versionadded:: 0.2.0
	"""
	figure = Figure(figsize=SMALL_INCHES)
	axes = figure.add_subplot()

	write_title(axes, SHORT_TITLE)

	plot_title = figure.get_suptitle()
	assert plot_title == SHORT_TITLE


def test_write_title_breaks_a_long_title_within_the_margins() -> None:
	"""
	Check that each line of a long title fits the width of the Plot less its side margins.

	.. versionadded:: 0.2.0
	"""
	figure = Figure(figsize=SMALL_INCHES)
	axes = figure.add_subplot()
	figure_points = SMALL_INCHES[0] * POINTS_PER_INCH
	margin_points = figure_points * TITLE_SIDE_MARGIN * SIDE_COUNT
	width_limit = figure_points - margin_points

	write_title(axes, LONG_TITLE)

	plot_title = figure.get_suptitle()
	title_lines = plot_title.split(LINE_BREAK)
	line_count = len(title_lines)
	title_size = matplotlib.rcParams["figure.titlesize"]
	title_font = FontProperties(size=title_size)
	line_widths = [measure_text_width(title_line, title_font) for title_line in title_lines]
	widest_line = max(line_widths)
	assert line_count > 1
	assert widest_line <= width_limit


def test_write_title_keeps_the_given_line_breaks() -> None:
	"""
	Check that a line break written in the title is kept.

	.. versionadded:: 0.2.0
	"""
	figure = Figure(figsize=SMALL_INCHES)
	axes = figure.add_subplot()

	write_title(axes, GIVEN_LINES_TITLE)

	plot_title = figure.get_suptitle()
	title_lines = plot_title.split(LINE_BREAK)
	assert title_lines == EXPECTED_GIVEN_LINES


def test_write_title_titles_the_subfigure_of_the_plot() -> None:
	"""
	Check that a Plot of a Figure is titled on its own subfigure, not on the whole figure.

	.. versionadded:: 0.2.0
	"""
	figure = Figure()
	cell_grid = figure.add_gridspec(1, 2)
	subfigure = figure.add_subfigure(cell_grid[0, 1])
	axes = subfigure.add_subplot()

	write_title(axes, SHORT_TITLE)

	plot_title = subfigure.get_suptitle()
	figure_title = figure.get_suptitle()
	assert plot_title == SHORT_TITLE
	assert figure_title == ""


def test_wrap_line_keeps_a_word_wider_than_the_limit_whole() -> None:
	"""
	Check that a single word wider than the limit is not cut.

	.. versionadded:: 0.2.0
	"""
	wrapped_line = wrap_line(LONG_WORD, TITLE_FONT, NARROW_LIMIT)

	assert wrapped_line == LONG_WORD


def test_measure_text_width_grows_with_the_font_size() -> None:
	"""
	Check that the same text is wider in a larger font.

	.. versionadded:: 0.2.0
	"""
	small_font = FontProperties(size=10.0)
	large_font = FontProperties(size=20.0)

	small_width = measure_text_width(SHORT_TITLE, small_font)
	large_width = measure_text_width(SHORT_TITLE, large_font)

	assert small_width < large_width
