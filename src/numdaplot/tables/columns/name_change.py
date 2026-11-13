"""
A new name for one column of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_column_name


@dataclass(frozen=True)
class NameChange:
	"""
	A new name for one column of a Table, used by ``Renaming``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	old_name
		The current name of the column.
	new_name
		Its new name, a non-empty text.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``old_name`` or ``new_name`` is an empty text.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.rename(ndp.Renaming(changes=[ndp.NameChange(old_name="city", new_name="town")]))
	    town   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	2  Paris   150.0
	"""

	old_name: str
	new_name: str

	def __post_init__(self) -> None:
		"""
		Check that both names are non-empty texts.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``old_name`` or ``new_name`` is an empty text.
		"""
		require_field_types(self)

		require_column_name(self.old_name)
		require_column_name(self.new_name)
