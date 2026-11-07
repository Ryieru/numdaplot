"""
Names of the columns of a join that are not keys.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.tables.columns.column_names import require_unique_names
from numdaplot.tables.joining.join_suffixes import JoinSuffixes


def name_joined_columns(
	column_names: list[str], other_names: list[str], keys: list[str], suffixes: JoinSuffixes | None
) -> tuple[list[str], list[str]]:
	"""
	Return the names the columns of both Tables take in a join, besides the keys.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The column names of the joined Table.
	other_names
		The column names of the other Table.
	keys
		The names of the key columns, left out of both lists.
	suffixes
		The suffixes of the columns both Tables have, or None.

	Returns
	-------
	tuple[list[str], list[str]]
		The names of the other columns of the joined Table, then of the other Table, in their order, a suffix added
		to each name both have.

	Raises
	------
	DuplicateColumnError
		When both Tables have a column besides the keys and no suffixes are given, or a suffixed name is already the
		name of another column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.joined_names import name_joined_columns
	>>> years = ndp.JoinSuffixes(left="_2024", right="_2025")
	>>> name_joined_columns(["dep", "deaths", "area"], ["dep", "deaths"], ["dep"], years)
	(['deaths_2024', 'area'], ['deaths_2025'])
	"""
	key_names = set(keys)
	kept_names = [column_name for column_name in column_names if column_name not in key_names]
	other_kept_names = [other_name for other_name in other_names if other_name not in key_names]
	shared_names = set(kept_names) & set(other_kept_names)
	shared_name_list = [column_name for column_name in kept_names if column_name in shared_names]
	needs_suffixes = suffixes is None and shared_name_list != []
	if needs_suffixes:
		raise DuplicateColumnError(shared_name_list[0])

	joined_names = kept_names
	other_joined_names = other_kept_names
	if suffixes is not None:
		joined_names = add_suffix(kept_names, shared_names, suffixes.left)
		other_joined_names = add_suffix(other_kept_names, shared_names, suffixes.right)

	all_names = [*keys, *joined_names, *other_joined_names]
	require_unique_names(all_names)

	return joined_names, other_joined_names


def add_suffix(column_names: list[str], shared_names: set[str], suffix: str) -> list[str]:
	"""
	Return the column names with a suffix added to each name both Tables of a join have.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The column names of one Table, besides the keys.
	shared_names
		The names both Tables have, besides the keys.
	suffix
		The suffix of this Table.

	Returns
	-------
	list[str]
		The names in their order, the shared ones followed by the suffix.

	Examples
	--------
	>>> from numdaplot.tables.joining.joined_names import add_suffix
	>>> add_suffix(["deaths", "area"], {"deaths"}, "_2024")
	['deaths_2024', 'area']
	"""
	suffixed_names = list[str]()

	for column_name in column_names:
		suffixed_name = column_name
		if column_name in shared_names:
			suffixed_name = column_name + suffix

		suffixed_names.append(suffixed_name)

	return suffixed_names
