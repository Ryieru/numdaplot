"""
Texts read as missing values in CSV and Excel files.

.. versionadded:: 0.1.0
"""

from typing import Any

# The texts pandas reads as missing by default, written here so that the reading never depends on the pandas version.
DEFAULT_MISSING_TEXTS = (
	"",
	"#N/A",
	"#N/A N/A",
	"#NA",
	"-1.#IND",
	"-1.#QNAN",
	"-NaN",
	"-nan",
	"1.#IND",
	"1.#QNAN",
	"<NA>",
	"N/A",
	"NA",
	"NULL",
	"NaN",
	"None",
	"n/a",
	"nan",
	"null",
)
DEFAULT_MISSING_SETTING = "keep_default_na"
MISSING_VALUES_SETTING = "na_values"


def find_missing_settings(missing_texts: list[str] | None) -> dict[str, Any]:
	"""
	Return the settings of ``pandas.read_csv`` or ``pandas.read_excel`` reading exactly the given texts as missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	missing_texts
		The texts read as missing, the default texts of ``DEFAULT_MISSING_TEXTS`` when None.

	Returns
	-------
	dict[str, Any]
		The pandas settings, which never add the pandas default texts to the given ones.

	Examples
	--------
	>>> from numdaplot.tables.files.missing_texts import find_missing_settings
	>>> find_missing_settings(["N/A"])
	{'keep_default_na': False, 'na_values': ['N/A']}
	"""
	read_texts = list(DEFAULT_MISSING_TEXTS)
	if missing_texts is not None:
		read_texts = list(missing_texts)

	missing_settings = {DEFAULT_MISSING_SETTING: False, MISSING_VALUES_SETTING: read_texts}

	return missing_settings
