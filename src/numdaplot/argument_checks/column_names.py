"""
Checks of the column names given to a setting or an operation.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence

from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.tables.invalid_column_name_error import InvalidColumnNameError

COLUMN_ITEM_NAME = "column"


def require_column_name(column_name: object) -> None:
	"""
	Check that a column name is a non-empty text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		The name to check.

	Raises
	------
	InvalidColumnNameError
		When the name is not a text, or is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import require_column_name
	>>> try:
	... 	require_column_name(2024)
	... except ndp.InvalidColumnNameError as error:
	... 	print(error)
	Expected a column name as a non-empty text, got 2024.
	"""
	is_text = isinstance(column_name, str)
	if not is_text:
		raise InvalidColumnNameError(column_name)

	if column_name == "":
		raise InvalidColumnNameError(column_name)


def require_optional_column_name(column_name: object) -> None:
	"""
	Check that a column name, when given, is a non-empty text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		The name to check, or None when the setting is omitted.

	Raises
	------
	InvalidColumnNameError
		When the name is given and is not a non-empty text.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import require_optional_column_name
	>>> require_optional_column_name(None)
	>>> try:
	... 	require_optional_column_name("")
	... except ndp.InvalidColumnNameError as error:
	... 	print(error)
	Expected a column name as a non-empty text, got ''.
	"""
	if column_name is None:
		return

	require_column_name(column_name)


def require_unique_names(column_names: Sequence[str]) -> None:
	"""
	Check that no column name appears twice.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The names to check.

	Raises
	------
	DuplicateColumnError
		At the first name that appears a second time.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import require_unique_names
	>>> try:
	... 	require_unique_names(["city", "price", "city"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'city' appears more than once.
	"""
	seen_names = set[str]()

	for column_name in column_names:
		if column_name in seen_names:
			raise DuplicateColumnError(column_name)

		seen_names.add(column_name)


def require_column_names(column_names: Sequence[object]) -> None:
	"""
	Check that every column name is a non-empty text and appears once.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The names to check, such as the header of a file.

	Raises
	------
	InvalidColumnNameError
		At the first name that is not a non-empty text.
	DuplicateColumnError
		At the first name that appears a second time.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import require_column_names
	>>> try:
	... 	require_column_names(["city", ""])
	... except ndp.InvalidColumnNameError as error:
	... 	print(error)
	Expected a column name as a non-empty text, got ''.
	"""
	text_names = list[str]()

	for column_name in column_names:
		require_column_name(column_name)
		text_name = str(column_name)
		text_names.append(text_name)

	require_unique_names(text_names)


def copy_column_names(column_names: list[str]) -> list[str]:
	"""
	Return a copy of a list of column names given to a setting, after checking it.

	A setting keeps its own copy, so that changing the given list afterwards leaves the setting unchanged.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column_names
		The names given, at least one.

	Returns
	-------
	list[str]
		A new list holding the same names.

	Raises
	------
	EmptyListError
		When the list is empty.
	InvalidColumnNameError
		At the first name that is not a non-empty text.
	DuplicateColumnError
		At the first name that appears a second time.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import copy_column_names
	>>> copy_column_names(["city", "price"])
	['city', 'price']
	>>> try:
	... 	copy_column_names([])
	... except ndp.EmptyListError as error:
	... 	print(error)
	Expected at least one column, got an empty list.
	"""
	if column_names == []:
		raise EmptyListError(COLUMN_ITEM_NAME)

	require_column_names(column_names)
	names_copy = list(column_names)

	return names_copy


def copy_optional_column_names(column_names: list[str] | None) -> list[str] | None:
	"""
	Return a copy of a list of column names given to a setting, after checking it, or None when it is omitted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The names given, at least one, or None when the setting is omitted.

	Returns
	-------
	list[str] or None
		A new list holding the same names, or None.

	Raises
	------
	EmptyListError
		When the list is empty.
	InvalidColumnNameError
		At the first name that is not a non-empty text.
	DuplicateColumnError
		At the first name that appears a second time.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import copy_optional_column_names
	>>> copy_optional_column_names(None) is None
	True
	>>> try:
	... 	copy_optional_column_names(["price", "price"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'price' appears more than once.
	"""
	if column_names is None:
		return None

	names_copy = copy_column_names(column_names)

	return names_copy


def require_known_columns(requested_names: Sequence[str], column_names: Sequence[str]) -> None:
	"""
	Check that every requested column exists.

	.. versionadded:: 0.1.0

	Parameters
	----------
	requested_names
		The names given by the user.
	column_names
		The names of the columns of the Table.

	Raises
	------
	ColumnNotFoundError
		At the first requested name that matches no column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.column_names import require_known_columns
	>>> try:
	... 	require_known_columns(["prise"], ["city", "price"])
	... except ndp.ColumnNotFoundError as error:
	... 	print(error)
	No column is named 'prise'.
	"""
	known_names = set(column_names)

	for requested_name in requested_names:
		if requested_name not in known_names:
			raise ColumnNotFoundError(requested_name)
