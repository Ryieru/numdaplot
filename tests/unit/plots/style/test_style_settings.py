"""
Unit tests of CustomColor, Size, ImageOptions and PlotStyle.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_color_error import InvalidColorError
from numdaplot.errors.invalid_resolution_error import InvalidResolutionError
from numdaplot.errors.invalid_rotation_error import InvalidRotationError
from numdaplot.errors.invalid_size_error import InvalidSizeError
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.plots.style.grid_lines import GridLines
from numdaplot.plots.style.image_options import ImageOptions
from numdaplot.plots.style.legend_position import LegendPosition
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.plots.style.size import Size

COLOR_CODES = ["#ff8800", "#FF8800", "#1f77b4"]
REJECTED_CODES = ["ff8800", "#ff88", "#ff88001", "#gg8800", "", "orange"]
REJECTED_SIZES = [(0.0, 4.8), (6.4, -1.0)]
DEFAULT_DPI = 100
REJECTED_DPI = 0
ACCEPTED_ROTATIONS = [-90, 0, 45.5, 90]
REJECTED_ROTATIONS = [-90.5, 91, float("nan")]


@pytest.mark.parametrize("code", COLOR_CODES)
def test_custom_color_keeps_a_hexadecimal_code(code: str) -> None:
	"""
	Check that ``#`` and six hexadecimal digits, in any case, are accepted as given.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code
		An accepted color code.
	"""
	color = CustomColor(code)

	assert color.code == code


@pytest.mark.parametrize("code", REJECTED_CODES)
def test_custom_color_rejects_a_code_not_written_as_rrggbb(code: str) -> None:
	"""
	Check that any other text raises InvalidColorError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code
		A rejected text.
	"""
	with pytest.raises(InvalidColorError):
		CustomColor(code)


@pytest.mark.parametrize(("width", "height"), REJECTED_SIZES)
def test_size_rejects_a_width_or_height_that_is_not_positive(width: float, height: float) -> None:
	"""
	Check that a zero or negative side raises InvalidSizeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The width given.
	height
		The height given.
	"""
	with pytest.raises(InvalidSizeError):
		Size(width=width, height=height)


def test_image_options_default_to_100_dots_per_inch() -> None:
	"""
	Check the default resolution.

	.. versionadded:: 0.1.0
	"""
	options = ImageOptions()

	assert options.dpi == DEFAULT_DPI


def test_image_options_reject_a_resolution_below_one() -> None:
	"""
	Check that a resolution of 0 raises InvalidResolutionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidResolutionError):
		ImageOptions(dpi=REJECTED_DPI)


def test_style_defaults_draw_grid_lines_and_place_the_legend_best() -> None:
	"""
	Check the defaults of a PlotStyle: no title or labels, grid lines, best legend and default size.

	.. versionadded:: 0.1.0
	"""
	style = PlotStyle()

	assert style.title is None
	assert style.x_label is None
	assert style.y_label is None
	assert style.right_label is None
	assert style.legend == LegendPosition.BEST
	assert style.grid_lines == GridLines.SHOWN
	assert style.size == Size()


@pytest.mark.parametrize("rotation", ACCEPTED_ROTATIONS)
def test_style_accepts_a_rotation_from_minus_90_to_90_degrees(rotation: float) -> None:
	"""
	Check the limits and an angle between them.

	.. versionadded:: 0.1.0
	"""
	style = PlotStyle(x_tick_rotation=rotation)

	assert style.x_tick_rotation == rotation


@pytest.mark.parametrize("rotation", REJECTED_ROTATIONS)
def test_style_rejects_another_rotation(rotation: float) -> None:
	"""
	Check angles beyond the limits, and a value that is not a number.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidRotationError):
		PlotStyle(x_tick_rotation=rotation)


def test_style_leaves_the_rotation_to_the_values_by_default() -> None:
	"""
	Check that no angle is chosen by default.

	.. versionadded:: 0.1.0
	"""
	style = PlotStyle()

	assert style.x_tick_rotation is None


@pytest.mark.parametrize("rotation", ACCEPTED_ROTATIONS)
def test_style_accepts_a_y_rotation_from_minus_90_to_90_degrees(rotation: float) -> None:
	"""
	Check the limits and an angle between them for the ``y`` values.

	.. versionadded:: 0.1.0
	"""
	style = PlotStyle(y_tick_rotation=rotation)

	assert style.y_tick_rotation == rotation


@pytest.mark.parametrize("rotation", REJECTED_ROTATIONS)
def test_style_rejects_another_y_rotation(rotation: float) -> None:
	"""
	Check angles beyond the limits, and a value that is not a number, for the ``y`` values.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidRotationError):
		PlotStyle(y_tick_rotation=rotation)


def test_plot_style_shows_every_column_under_its_name_by_default() -> None:
	"""
	Check that no renaming is given by default.

	.. versionadded:: 0.1.0
	"""
	style = PlotStyle()

	assert style.renaming is None
