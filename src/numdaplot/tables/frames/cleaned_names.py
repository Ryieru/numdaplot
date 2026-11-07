r"""
Cleaning of the column names a Table reads.

.. versionadded:: 0.1.0
"""

from collections.abc import Hashable

import pandas

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.tables.files.column_names import ColumnNames


def clean_frame_names(frame: pandas.DataFrame, column_names: ColumnNames) -> pandas.DataFrame:
	r"""
	Return a DataFrame read from outside numdaplot, with its column names cleaned when asked.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		A DataFrame read from a file or given by the user. It is not changed.
	column_names
		``CLEANED`` to remove the spaces, tabs and line breaks at the start and the end of each name, ``KEPT`` to
		keep the names as written.

	Returns
	-------
	pandas.DataFrame
		The DataFrame with the cleaned names, or the same DataFrame when the names are kept.

	Raises
	------
	DuplicateColumnError
		When two different names become the same once cleaned.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.cleaned_names import clean_frame_names
	>>> frame = pandas.DataFrame({"id_vehicule\n": [1], " speed ": [50]})
	>>> clean_frame_names(frame, ndp.ColumnNames.CLEANED).columns.tolist()
	['id_vehicule', 'speed']
	"""
	if column_names == ColumnNames.KEPT:
		return frame

	raw_names = list[Hashable](frame.columns)
	cleaned_names = clean_names(raw_names)
	require_distinct_cleaned_names(raw_names, cleaned_names)
	cleaned_frame = frame.copy(deep=False)
	cleaned_frame.columns = pandas.Index(cleaned_names)

	return cleaned_frame


def clean_names(names: list[Hashable]) -> list[Hashable]:
	r"""
	Return column names without the spaces, tabs and line breaks at their start and end.

	A name that is not a text is kept, so that the check of the column names refuses it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	names
		The column names.

	Returns
	-------
	list[Hashable]
		The cleaned names, in the same order.

	Examples
	--------
	>>> from numdaplot.tables.frames.cleaned_names import clean_names
	>>> clean_names(["id_vehicule\n", " speed", 2024])
	['id_vehicule', 'speed', 2024]
	"""
	cleaned_names = list[Hashable]()
	for name in names:
		cleaned_name = name
		if isinstance(name, str):
			cleaned_name = name.strip()

		cleaned_names.append(cleaned_name)

	return cleaned_names


def require_distinct_cleaned_names(raw_names: list[Hashable], cleaned_names: list[Hashable]) -> None:
	r"""
	Check that two different names do not become the same once cleaned.

	A name written twice the same way is left to the check of the column names, which names it alone.

	.. versionadded:: 0.1.0

	Parameters
	----------
	raw_names
		The column names as written.
	cleaned_names
		The same names once cleaned, in the same order.

	Raises
	------
	DuplicateColumnError
		At the first cleaned name coming from two different names, with both of them.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.cleaned_names import require_distinct_cleaned_names
	>>> try:
	... 	require_distinct_cleaned_names(["id", "id\n"], ["id", "id"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column names 'id' and 'id\n' both become 'id' once cleaned. Use ColumnNames.KEPT to keep them as written.
	"""
	first_raw_names = dict[Hashable, Hashable]()
	for raw_name, cleaned_name in zip(raw_names, cleaned_names, strict=True):
		first_raw_name = first_raw_names.setdefault(cleaned_name, raw_name)
		if first_raw_name == raw_name:
			continue

		original_names = [str(first_raw_name), str(raw_name)]
		raise DuplicateColumnError(str(cleaned_name), original_names)
