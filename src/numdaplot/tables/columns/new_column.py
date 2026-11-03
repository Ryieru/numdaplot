"""
A column to add to a Table.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numdaplot.tables.columns.column_names import require_column_name
from numdaplot.tables.conflict import Conflict

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array


# eq=False because comparing two new columns would compare their Arrays with ==, which Array refuses.
@dataclass(frozen=True, eq=False)
class NewColumn:
	"""
	A column to add to a Table, used by ``Table.add_column``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name of the column, a non-empty text.
	values
		A one-dimensional Array with one value per row of the Table.
	on_conflict
		``ERROR`` refuses a name that already exists, which is the default.
		``REPLACE`` replaces the existing column, at its place.

	Raises
	------
	InvalidColumnNameError
		When ``name`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> taxed_prices = sales.column("price") * 1.2
	>>> sales.add_column(ndp.NewColumn(name="taxed_price", values=taxed_prices))
	city   price taxed_price
	TEXT FLOAT64     FLOAT64
	0  Paris   120.0       144.0
	1   Lyon    80.0        96.0
	2  Paris   150.0       180.0
	"""

	name: str
	values: Array
	on_conflict: Conflict = Conflict.ERROR

	def __post_init__(self) -> None:
		"""
		Check that the name is a non-empty text.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidColumnNameError
			When ``name`` is empty.
		"""
		require_column_name(self.name)
