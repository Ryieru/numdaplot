"""
Unit tests of draw_random_values and require_valid_seed.

.. versionadded:: 0.1.0
"""

from typing import cast

import numpy
import pytest

from numdaplot.arrays.creation.normal import Normal
from numdaplot.arrays.creation.random_integers import RandomIntegers
from numdaplot.arrays.creation.random_values import draw_random_values, require_valid_seed
from numdaplot.arrays.creation.uniform import Uniform
from numdaplot.errors.invalid_seed_error import InvalidSeedError
from numdaplot.positions.shape import Shape
from numdaplot.rules.bounds import Bounds

SEED = 42
NEGATIVE_SEED = -1
DRAW_COUNT = 1000
DRAW_SHAPE = Shape([DRAW_COUNT])
GRID_SHAPE = Shape([2, 3])
DIE = RandomIntegers(low=1, high=6)
EXCLUSIVE_DIE = RandomIntegers(low=1, high=6, bounds=Bounds.EXCLUDED)
UNIT_INTERVAL = Uniform(low=0, high=1)
CONSTANT_NORMAL = Normal(mean=5, deviation=0)
DIE_FACES = {1, 2, 3, 4, 5, 6}
INNER_DIE_FACES = {2, 3, 4, 5}
CONSTANT_VALUE = 5.0


def test_draw_random_values_gives_the_same_values_with_the_same_seed() -> None:
	"""
	Check that a seed makes the draw reproducible.

	.. versionadded:: 0.1.0
	"""
	first_values = draw_random_values(UNIT_INTERVAL, GRID_SHAPE, SEED)
	second_values = draw_random_values(UNIT_INTERVAL, GRID_SHAPE, SEED)

	are_same = numpy.array_equal(first_values, second_values)
	assert are_same


def test_draw_random_values_draws_without_seed() -> None:
	"""
	Check that a draw without seed gives values of the distribution.

	.. versionadded:: 0.1.0
	"""
	values = draw_random_values(DIE, DRAW_SHAPE, None)

	drawn_values = cast(list[int], values.tolist())
	drawn_faces = set(drawn_values)
	assert drawn_faces <= DIE_FACES


def test_draw_random_values_follows_the_shape() -> None:
	"""
	Check that the values have the requested shape.

	.. versionadded:: 0.1.0
	"""
	values = draw_random_values(UNIT_INTERVAL, GRID_SHAPE, SEED)

	dimensions = list(values.shape)
	assert dimensions == GRID_SHAPE.dimensions


def test_draw_random_values_draws_every_face_of_a_die() -> None:
	"""
	Check that both included bounds of a die are drawn.

	.. versionadded:: 0.1.0
	"""
	values = draw_random_values(DIE, DRAW_SHAPE, SEED)

	raw_values = values.tolist()
	value_list = cast(list[int], raw_values)
	drawn_faces = set(value_list)
	assert drawn_faces == DIE_FACES


def test_draw_random_values_never_draws_an_excluded_bound() -> None:
	"""
	Check that excluded bounds of a die are never drawn.

	.. versionadded:: 0.1.0
	"""
	values = draw_random_values(EXCLUSIVE_DIE, DRAW_SHAPE, SEED)

	raw_values = values.tolist()
	value_list = cast(list[int], raw_values)
	drawn_faces = set(value_list)
	assert drawn_faces == INNER_DIE_FACES


def test_draw_random_values_draws_the_mean_with_a_zero_deviation() -> None:
	"""
	Check that a normal law without spread always gives its mean.

	.. versionadded:: 0.1.0
	"""
	values = draw_random_values(CONSTANT_NORMAL, GRID_SHAPE, SEED)

	flat_values = values.flatten()
	raw_values = flat_values.tolist()
	value_list = cast(list[float], raw_values)
	drawn_values = set(value_list)
	assert drawn_values == {CONSTANT_VALUE}


def test_require_valid_seed_rejects_a_negative_seed() -> None:
	"""
	Check that a negative seed raises InvalidSeedError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSeedError):
		require_valid_seed(NEGATIVE_SEED)


def test_draw_random_values_rejects_a_negative_seed() -> None:
	"""
	Check that the draw checks its seed.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSeedError):
		draw_random_values(DIE, GRID_SHAPE, NEGATIVE_SEED)
