"""
Unit tests of FigureStyle.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.figure.figure_style import FigureStyle
from numdaplot.plots.style.size import Size

TITLE = "Shop"
SIZE = Size(width=8, height=3)


def test_figure_style_has_no_title_and_no_size_by_default() -> None:
	"""
	Check the defaults of a FigureStyle.

	.. versionadded:: 0.1.0
	"""
	style = FigureStyle()

	assert style.title is None
	assert style.size is None


def test_figure_style_keeps_its_settings() -> None:
	"""
	Check that the given title and size are available as attributes.

	.. versionadded:: 0.1.0
	"""
	style = FigureStyle(title=TITLE, size=SIZE)

	assert style.title == TITLE
	assert style.size == SIZE
