"""
Unit tests of convert_size_to_inches.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.plots.drawing.size_inches import convert_size_to_inches
from numdaplot.plots.style.size import Size
from numdaplot.plots.style.size_unit import SizeUnit

DEFAULT_INCHES = (6.4, 4.8)
PIXEL_SIZE = Size(width=600, height=300, unit=SizeUnit.PIXEL)
EXPECTED_PIXEL_INCHES = (6.0, 3.0)
CENTIMETER_SIZE = Size(width=2.54, height=5.08, unit=SizeUnit.CENTIMETER)
EXPECTED_CENTIMETER_INCHES = (1.0, 2.0)


def test_default_size_is_the_matplotlib_size_in_inches() -> None:
	"""
	Check that a Size without arguments is 6.4 by 4.8 inches.

	.. versionadded:: 0.1.0
	"""
	default_size = Size()

	inches = convert_size_to_inches(default_size)

	assert inches == DEFAULT_INCHES


@pytest.mark.parametrize(
	("size", "expected_inches"),
	[(PIXEL_SIZE, EXPECTED_PIXEL_INCHES), (CENTIMETER_SIZE, EXPECTED_CENTIMETER_INCHES)],
)
def test_convert_size_to_inches_converts_pixels_and_centimeters(
	size: Size,
	expected_inches: tuple[float, float],
) -> None:
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
	inches = convert_size_to_inches(size)

	assert inches == expected_inches
