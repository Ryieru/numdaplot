"""
Settings of the comparison of two Arrays or two Tables.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.arrays.type_match import TypeMatch

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array
	from numdaplot.tables.table import Table


# eq=False because comparing two settings would compare their Arrays or Tables with ==, which they refuse.
@dataclass(frozen=True, eq=False)
class Equality:
	"""
	Settings of the comparison of two Arrays or two Tables, used by ``Array.is_equal`` and ``Table.is_equal``.

	Two Arrays are equal when they have the same shape and the same values at each position.
	Two Tables are equal when they have the same columns, in the same order, with the same values.
	Two missing values at the same position are equal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	other
		The Array or the Table to compare with, of the same kind as the compared one.
	types
		Whether the types must also be the same. Only the values are compared by default.


	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> integers = ndp.Array.from_list([1, 2])
	>>> decimals = ndp.Array.from_list([1.0, 2.0])
	>>> integers.is_equal(ndp.Equality(other=decimals, types=ndp.TypeMatch.STRICT))
	False
	"""

	other: Array | Table
	types: TypeMatch = TypeMatch.IGNORED

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
