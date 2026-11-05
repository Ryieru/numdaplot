"""
Unit tests of CustomColor, Size, ImageOptions and Style.

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
from numdaplot.plots.style.size import Size
from numdaplot.plots.style.size_unit import SizeUnit
from numdaplot.plots.style.style import Style

COLOR_CODES = ["#ff8800", "#FF8800", "#1f77b4"]
REJECTED_CODES = ["ff8800", "#ff88", "#ff88001", "#gg8800", "", "orange"]
REJECTED_SIZES = [(0.0, 4.8), (6.4, -1.0)]
DEFAULT_INCHES = (6.4, 4.8)
PIXEL_SIZE = Size(width=600, height=300, unit=SizeUnit.PIXEL)
EXPECTED_PIXEL_INCHES = (6.0, 3.0)
CENTIMETER_SIZE = Size(width=2.54, height=5.08, unit=SizeUnit.CENTIMETER)
EXPECTED_CENTIMETER_INCHES = (1.0, 2.0)
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


def test_size_defaults_to_the_matplotlib_size_in_inches() -> None:
	"""
	Check that a Size without arguments is 6.4 by 4.8 inches.

	.. versionadded:: 0.1.0
	"""
	inches = Size().to_inches()

	assert inches == DEFAULT_INCHES


@pytest.mark.parametrize(
	("size", "expected_inches"),
	[(PIXEL_SIZE, EXPECTED_PIXEL_INCHES), (CENTIMETER_SIZE, EXPECTED_CENTIMETER_INCHES)],
)
def test_size_to_inches_converts_pixels_and_centimeters(size: Size, expected_inches: tuple[float, float]) -> None:
	"""
	Check that a pixel is a hundredth of an inch and an inch is 2.54 centimeters.

	.. versionadded:: 0.1.0

	Parameters
	----------
	size
		A size in pixels or centimeters.
	expected_inches
		The same size in inches.
	"""
	inches = size.to_inches()

	assert inches == expected_inches


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
	Check the defaults of a Style: no title or labels, grid lines, best legend and default size.

	.. versionadded:: 0.1.0
	"""
	style = Style()

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
	style = Style(x_tick_rotation=rotation)

	assert style.x_tick_rotation == rotation


@pytest.mark.parametrize("rotation", REJECTED_ROTATIONS)
def test_style_rejects_another_rotation(rotation: float) -> None:
	"""
	Check angles beyond the limits, and a value that is not a number.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidRotationError):
		Style(x_tick_rotation=rotation)


def test_style_leaves_the_rotation_to_the_values_by_default() -> None:
	"""
	Check that no angle is chosen by default.

	.. versionadded:: 0.1.0
	"""
	style = Style()

	assert style.x_tick_rotation is None


@pytest.mark.parametrize("rotation", ACCEPTED_ROTATIONS)
def test_style_accepts_a_y_rotation_from_minus_90_to_90_degrees(rotation: float) -> None:
	"""
	Check the limits and an angle between them for the ``y`` values.

	.. versionadded:: 0.1.0
	"""
	style = Style(y_tick_rotation=rotation)

	assert style.y_tick_rotation == rotation


@pytest.mark.parametrize("rotation", REJECTED_ROTATIONS)
def test_style_rejects_another_y_rotation(rotation: float) -> None:
	"""
	Check angles beyond the limits, and a value that is not a number, for the ``y`` values.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidRotationError):
		Style(y_tick_rotation=rotation)
