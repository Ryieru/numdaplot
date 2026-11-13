"""
Unit tests of the color of a text written over a colored area.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.plots.drawing.colors.text_contrast import DARK_TEXT_COLOR, LIGHT_TEXT_COLOR, choose_text_color

WHITE = (1.0, 1.0, 1.0, 1.0)
YELLOW = (0.99, 0.91, 0.14, 1.0)
DARK_BLUE = (0.03, 0.19, 0.42, 1.0)
BLACK = (0.0, 0.0, 0.0, 1.0)


@pytest.mark.parametrize("background", [WHITE, YELLOW])
def test_choose_text_color_writes_black_over_a_light_color(background: tuple[float, ...]) -> None:
	"""
	Check that a light background gets a black text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	background
		A light color.
	"""
	text_color = choose_text_color(background)

	assert text_color == DARK_TEXT_COLOR


@pytest.mark.parametrize("background", [DARK_BLUE, BLACK])
def test_choose_text_color_writes_white_over_a_dark_color(background: tuple[float, ...]) -> None:
	"""
	Check that a dark background gets a white text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	background
		A dark color.
	"""
	text_color = choose_text_color(background)

	assert text_color == LIGHT_TEXT_COLOR
