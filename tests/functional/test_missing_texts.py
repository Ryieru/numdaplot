"""
Functional tests of the texts read as missing values in CSV and Excel files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import numdaplot as ndp

SEMICOLON = ";"
CSV_NAME = "places.csv"
PLACES_CSV = "road;width\nN/A;1.5\nA1;\nNA;3.0\n"
EXPECTED_DEFAULT_ROADS = [None, "A1", None]
EXPECTED_MISSING_WIDTHS = [False, True, False]
EXPECTED_GIVEN_ROADS = ["N/A", "A1", "NA"]
EXPECTED_TEXT_WIDTHS = ["1.5", "", "3.0"]
EMPTY_ONLY = [""]
NO_MISSING_TEXT = list[str]()
EXCEL_NAME = "places.xlsx"
NAMED_LIKE_MISSING = "NA"
WIDTHS = [1.5, 3.0]


def read_places(tmp_path: Path, missing_texts: list[str] | None) -> ndp.Table:
	"""
	Write the places CSV file and read it with given missing texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	missing_texts
		The texts read as missing, the default ones when None.

	Returns
	-------
	ndp.Table
		The Table read.
	"""
	path = tmp_path / CSV_NAME
	path.write_text(PLACES_CSV)
	options = ndp.CsvReadOptions(separator=SEMICOLON, missing_texts=missing_texts)
	places = ndp.Table.from_csv(path, options)

	return places


def test_usual_missing_texts_are_read_as_missing_by_default(tmp_path: Path) -> None:
	"""
	Check that N/A, NA and an empty value are missing when no text is given.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	places = read_places(tmp_path, None)

	road_column = places.column("road")
	roads = road_column.to_list()
	width_column = places.column("width")
	missing_widths = width_column.check(ndp.IsMissing())
	is_width_missing = missing_widths.to_list()
	assert roads == EXPECTED_DEFAULT_ROADS
	assert is_width_missing == EXPECTED_MISSING_WIDTHS


def test_given_missing_texts_replace_the_default_ones(tmp_path: Path) -> None:
	"""
	Check that N/A and NA stay texts when only the empty text is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	places = read_places(tmp_path, EMPTY_ONLY)

	road_column = places.column("road")
	roads = road_column.to_list()
	assert roads == EXPECTED_GIVEN_ROADS


def test_no_missing_text_reads_an_empty_number_as_a_text(tmp_path: Path) -> None:
	"""
	Check that without missing text, a column of numbers with an empty value is read as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	places = read_places(tmp_path, NO_MISSING_TEXT)

	width_type = places.column_types["width"]
	width_column = places.column("width")
	widths = width_column.to_list()
	assert width_type == ndp.Type.TEXT
	assert widths == EXPECTED_TEXT_WIDTHS


def test_an_excel_column_named_like_a_missing_text_keeps_its_name(tmp_path: Path) -> None:
	"""
	Check that an Excel column named NA is read with its name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / EXCEL_NAME
	widths = ndp.Array.from_list(WIDTHS)
	places = ndp.Table.from_arrays({NAMED_LIKE_MISSING: widths})
	places.to_excel(path)

	read_places = ndp.Table.from_excel(path)

	assert read_places.column_names == [NAMED_LIKE_MISSING]
