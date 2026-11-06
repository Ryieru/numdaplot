"""
Unit tests of the values of the color scales.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.plots.drawing.color_scale_values import SCALE_NAMES, find_point_colors

KEPT_SCALES = [ndp.ColorScale.VIRIDIS, ndp.ColorScale.CIVIDIS, ndp.ColorScale.RED_BLUE]
SHORTENED_SCALES = [ndp.ColorScale.BLUES, ndp.ColorScale.REDS, ndp.ColorScale.GREENS, ndp.ColorScale.GRAYS]
VISIBLE_COLOR_LIMIT = 0.9


def test_every_color_scale_has_a_matplotlib_name() -> None:
	"""
	Check that a new member of the enum cannot be forgotten.

	.. versionadded:: 0.1.0
	"""
	named_scales = set(SCALE_NAMES)

	assert named_scales == set(ndp.ColorScale)


@pytest.mark.parametrize("scale", KEPT_SCALES)
def test_find_point_colors_keeps_the_scales_not_starting_white(scale: ndp.ColorScale) -> None:
	"""
	Check that these scales keep their full colors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	scale
		The scale.
	"""
	point_colors = find_point_colors(scale)

	assert point_colors.name == SCALE_NAMES[scale]


@pytest.mark.parametrize("scale", SHORTENED_SCALES)
def test_find_point_colors_skips_the_white_of_a_scale(scale: ndp.ColorScale) -> None:
	"""
	Check that the first color is visible and that the name stays.

	.. versionadded:: 0.1.0

	Parameters
	----------
	scale
		The scale.
	"""
	point_colors = find_point_colors(scale)

	first_color = point_colors(0.0)
	assert min(first_color[:3]) < VISIBLE_COLOR_LIMIT
	assert point_colors.name == SCALE_NAMES[scale]
