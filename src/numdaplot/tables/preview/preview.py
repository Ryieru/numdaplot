"""
Settings of the preview of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.creation.random_values import require_valid_seed
from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.settings.setting_types import require_setting_type
from numdaplot.tables.preview.side import Side

DEFAULT_PREVIEW_COUNT = 5
MINIMUM_PREVIEW_COUNT = 1
SIDE_SETTING = "Preview side"
SIDE_EXPECTED = "a Side such as Side.END"
SIDE_TYPES = (Side,)


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
		The seed of the random draw, to show the same rows each time, other rows at each call when omitted. Only used
		with ``Side.RANDOM``.

	Raises
	------
	InvalidSettingTypeError
		When ``side`` is not a ``Side``, such as the text ``"end"``.
	InvalidCountError
		When ``count`` is lower than 1.
	InvalidSeedError
		When ``seed`` is negative.

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
		Check the side, the count and the seed.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When ``side`` is not a ``Side``.
		InvalidCountError
			When ``count`` is lower than 1.
		InvalidSeedError
			When ``seed`` is negative.
		"""
		require_setting_type(SIDE_SETTING, SIDE_EXPECTED, self.side, SIDE_TYPES)

		if self.count < MINIMUM_PREVIEW_COUNT:
			raise InvalidCountError(self.count, MINIMUM_PREVIEW_COUNT)

		if self.seed is not None:
			require_valid_seed(self.seed)
