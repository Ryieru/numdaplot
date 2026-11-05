"""
Settings of the preview of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.creation.random_values import require_valid_seed
from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.preview.side import Side

DEFAULT_PREVIEW_COUNT = 5
MINIMUM_PREVIEW_COUNT = 1
SEED_SETTING = "seed"
SIDE_OWNER = "Side.{side_name}"


@dataclass(frozen=True)
class Preview:
	"""
	How many rows of a Table to show, and which ones, used by ``Table.preview``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	count
		The number of rows, 5 by default. A shorter Table shows all its rows.
	side
		The first rows, ``Side.START`` by default, the last rows, ``Side.END``, or rows drawn at random,
		``Side.RANDOM``.
	seed
		The seed of the random draw, to show the same rows each time, other rows at each call when omitted. Only
		``Side.RANDOM`` accepts it.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidCountError
		When ``count`` is lower than 1.
	InvalidSeedError
		When ``seed`` is negative.
	RefusedSettingError
		When ``seed`` is given with ``Side.START`` or ``Side.END``, which draw nothing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.preview(ndp.Preview(count=2))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	count: int = DEFAULT_PREVIEW_COUNT
	side: Side = Side.START
	seed: int | None = None

	def __post_init__(self) -> None:
		"""
		Check the side, the count and the seed, which only a random draw uses.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidCountError
			When ``count`` is lower than 1.
		InvalidSeedError
			When ``seed`` is negative.
		RefusedSettingError
			When ``seed`` is given with ``Side.START`` or ``Side.END``.
		"""
		require_field_types(self)

		if self.count < MINIMUM_PREVIEW_COUNT:
			raise InvalidCountError(self.count, MINIMUM_PREVIEW_COUNT)

		if self.seed is None:
			return

		require_valid_seed(self.seed)
		if self.side != Side.RANDOM:
			side_owner = SIDE_OWNER.format(side_name=self.side.name)
			raise RefusedSettingError(SEED_SETTING, side_owner)
