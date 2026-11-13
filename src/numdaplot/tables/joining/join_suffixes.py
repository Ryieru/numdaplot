"""
Suffixes telling apart the columns that two joined Tables both have.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.tables.invalid_suffixes_error import InvalidSuffixesError


@dataclass(frozen=True)
class JoinSuffixes:
	"""
	Suffixes added to the names of the columns both Tables of a join have, besides the keys, used by ``Join``.

	Only those columns get a suffix, as in pandas. A suffixed name that another column already has raises
	``DuplicateColumnError`` at the join.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The suffix of the columns of the joined Table, such as ``"_2024"``.
	right
		The suffix of the columns of the other Table, such as ``"_2025"``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidSuffixesError
		When a suffix is empty, or both suffixes are the same.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> before = ndp.Table.from_arrays({"dep": ndp.Array.from_list(["75"]), "deaths": ndp.Array.from_list([40])})
	>>> after = ndp.Table.from_arrays({"dep": ndp.Array.from_list(["75"]), "deaths": ndp.Array.from_list([35])})
	>>> years = ndp.JoinSuffixes(left="_2024", right="_2025")
	>>> before.join(ndp.Join(other=after, keys=["dep"], suffixes=years))
	   dep deaths_2024 deaths_2025
	  TEXT       INT64       INT64
	0   75          40          35
	"""

	left: str
	right: str

	def __post_init__(self) -> None:
		"""
		Check that the suffixes are not empty and differ.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidSuffixesError
			When a suffix is empty, or both suffixes are the same.
		"""
		require_field_types(self)

		has_empty_suffix = self.left == "" or self.right == ""
		are_same = self.left == self.right
		is_invalid = has_empty_suffix or are_same
		if is_invalid:
			raise InvalidSuffixesError(self.left, self.right)
