"""
Checks of the column names of a Table.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError


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
	>>> from numdaplot.tables.columns.column_names import require_column_name
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
	>>> from numdaplot.tables.columns.column_names import require_optional_column_name
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
	>>> from numdaplot.tables.columns.column_names import require_unique_names
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
	>>> from numdaplot.tables.columns.column_names import require_column_names
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
	>>> from numdaplot.tables.columns.column_names import require_known_columns
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
