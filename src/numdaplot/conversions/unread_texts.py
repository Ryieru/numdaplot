"""
The first text a conversion was given but could not read.

.. versionadded:: 0.2.0
"""

import numpy
from numpy.typing import NDArray

from numdaplot.column_storage.column import Column


def find_first_unread_text(text_column: Column, read_values: Column, missing: NDArray[numpy.bool_]) -> str | None:
	"""
	Return the first text that was given but read as a missing value, which the conversion must refuse.

	.. versionadded:: 0.2.0

	Parameters
	----------
	text_column
		The texts given to the conversion.
	read_values
		The values read from them, missing where a text could not be read.
	missing
		Where the texts themselves are missing, which are not reading failures.

	Returns
	-------
	str or None
		The first text not read, or None when every given text was read.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.conversions.unread_texts import find_first_unread_text
	>>> texts = pandas.Series(["12:30", "noon", None], dtype="string")
	>>> times = pandas.Series([pandas.Timedelta(hours=12, minutes=30), None, None])
	>>> find_first_unread_text(texts, times, texts.isna().to_numpy())
	'noon'
	"""
	unread_values = read_values.isna()
	unread = unread_values.to_numpy(dtype=numpy.bool_)
	rejected = unread & ~missing
	has_rejected = bool(rejected.any())
	if not has_rejected:
		return None

	rejected_texts = text_column[rejected]
	first_rejected_text = str(rejected_texts.iloc[0])

	return first_rejected_text
