"""
Color of a text written over a colored area.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence

DARK_TEXT_COLOR = "#000000"
LIGHT_TEXT_COLOR = "#ffffff"
# Weights of the red, green and blue parts in the lightness the eye perceives.
LIGHTNESS_WEIGHTS = (0.2126, 0.7152, 0.0722)
LIGHT_BACKGROUND_THRESHOLD = 0.5


def choose_text_color(background_rgba: Sequence[float]) -> str:
	"""
	Return the color of a text that stays readable over a background: black over a light one, white over a dark one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	background_rgba
		The red, green, blue and opacity parts of the background, each from 0 to 1.

	Returns
	-------
	str
		``#000000`` or ``#ffffff``.

	Examples
	--------
	>>> from numdaplot.plots.drawing.text_contrast import choose_text_color
	>>> choose_text_color((1.0, 1.0, 0.6, 1.0)), choose_text_color((0.1, 0.1, 0.4, 1.0))
	('#000000', '#ffffff')
	"""
	red, green, blue = background_rgba[:3]
	red_weight, green_weight, blue_weight = LIGHTNESS_WEIGHTS
	lightness = red * red_weight + green * green_weight + blue * blue_weight
	if lightness > LIGHT_BACKGROUND_THRESHOLD:
		return DARK_TEXT_COLOR

	return LIGHT_TEXT_COLOR
