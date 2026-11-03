"""
Unit tests of compute_spacing_values.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.creation.spacing import Spacing
from numdaplot.arrays.creation.spacing_values import compute_spacing_values
from numdaplot.rules.bounds import Bounds

SPACINGS = [
	(Spacing(start=0, stop=1, count=5), [0.0, 0.25, 0.5, 0.75, 1.0]),
	(Spacing(start=0, stop=1, count=4, bounds=Bounds.LOW_ONLY), [0.0, 0.25, 0.5, 0.75]),
	(Spacing(start=0, stop=1, count=4, bounds=Bounds.HIGH_ONLY), [0.25, 0.5, 0.75, 1.0]),
	(Spacing(start=0, stop=1, count=4, bounds=Bounds.EXCLUDED), [0.2, 0.4, 0.6, 0.8]),
	(Spacing(start=1, stop=0, count=3), [1.0, 0.5, 0.0]),
]
THIRD_SPACING = Spacing(start=0, stop=1, count=4)
STOP = 1.0


@pytest.mark.parametrize(("spacing", "expected_values"), SPACINGS)
def test_compute_spacing_values_follows_the_bounds(spacing: Spacing, expected_values: list[float]) -> None:
	"""
	Check the values given by each bounds setting, and by a decreasing spacing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	spacing
		The spacing.
	expected_values
		Its values.
	"""
	values = compute_spacing_values(spacing)

	is_close = numpy.allclose(values, expected_values)
	assert is_close


def test_compute_spacing_values_ends_exactly_on_an_included_stop() -> None:
	"""
	Check that thirds of 1 end with exactly 1.0.

	.. versionadded:: 0.1.0
	"""
	values = compute_spacing_values(THIRD_SPACING)

	last_value = values[-1]
	assert last_value == STOP
