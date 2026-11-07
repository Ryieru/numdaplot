"""
Join of a Table with another Table.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.joining.join import Join
from numdaplot.tables.joining.joined_frame import join_frames
from numdaplot.tables.table_data import TableData


class TableJoining(TableData):
	"""
	Join of a Table with another Table on the values of key columns, with ``join``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def join(self, join: Join) -> Self:
		"""
		Return the rows of this Table and of another Table put side by side where their keys match.

		.. versionadded:: 0.1.0

		Parameters
		----------
		join
			The other Table, the key columns, the rows kept and how the columns both Tables have are told apart.

		Returns
		-------
		Self
			A new Table: the keys, then the other columns of this Table, then those of the other Table. The rows of
			this Table come first, in their order, each once per match, then the unmatched rows of the other Table
			kept by the mode. Missing values fill the columns of a Table that has no matching row, each column
			keeping its type.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ColumnNotFoundError
			When a key is missing from one of the Tables.
		IncompatibleTypesError
			When the two columns of a key are of different families, of different types with ``KeyTypes.SAME_TYPE``,
			or a date and a datetime: convert one of them first.
		TimeZoneMismatchError
			When the two columns of a key hold datetimes of different time zones, or with and without one: change
			them first with ``TimeZoneChange``.
		DuplicateColumnError
			When both Tables have a column besides the keys and the join has no ``suffixes``, or a suffixed name is
			already the name of another column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> accidents = ndp.Table.from_arrays(
		... 	{"Num_Acc": ndp.Array.from_list([101, 102]), "dep": ndp.Array.from_list(["75", "69"])}
		... )
		>>> users = ndp.Table.from_arrays(
		... 	{"Num_Acc": ndp.Array.from_list([101, 101, 103]), "grav": ndp.Array.from_list([1, 3, 2])}
		... )
		>>> accidents.join(ndp.Join(other=users, keys=["Num_Acc"], mode=ndp.JoinMode.LEFT))
		  Num_Acc  dep  grav
		    INT64 TEXT INT64
		0     101   75     1
		1     101   75     3
		2     102   69  <NA>
		"""
		joined_frame = join_frames(self._frame, join)
		joined_table = self._wrap(joined_frame)

		return joined_table
