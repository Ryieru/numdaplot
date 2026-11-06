"""
Reading and writing JSON files.

.. versionadded:: 0.1.0
"""

import json
from pathlib import Path
from typing import Any, cast

import pandas

from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.tables.files.json_decimals import has_decimal_column, write_exact_objects
from numdaplot.tables.files.json_layout import JsonLayout
from numdaplot.tables.files.json_options import JsonOptions

JSON_ENCODING = "utf-8"
RECORDS_ORIENTATION = "records"
ISO_DATE_FORMAT = "iso"
PYTHON_OBJECT_DTYPE = object
DECIMALS_SETTING = "decimals"
FROM_JSON_NAME = "Table.from_json"
WRITE_MODE = "w"
LINE_END = "\n"
OBJECT_SEPARATOR = ","
LIST_FORMAT = "[{objects}]"
UNCHANGED_NEWLINES = ""
EMPTY_LINES_TEXT = ""


def require_json_read_options(options: JsonOptions) -> None:
	"""
	Check that the settings of a JSON file apply to its reading.

	.. versionadded:: 0.1.0

	Parameters
	----------
	options
		The settings of the file.

	Raises
	------
	RefusedSettingError
		When ``decimals`` is given, which only applies to the writing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.json_file import require_json_read_options
	>>> try:
	... 	require_json_read_options(ndp.JsonOptions(decimals=2))
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	Table.from_json does not accept decimals.
	"""
	if options.decimals is not None:
		raise RefusedSettingError(DECIMALS_SETTING, FROM_JSON_NAME)


def read_json_file(path: Path, options: JsonOptions) -> pandas.DataFrame:
	"""
	Return the columns of a JSON file holding one object per row.

	The values are kept as Python objects, so a Table guesses each type from the values of the file
	only: a text that looks like a number or a date stays a text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing JSON file, in UTF-8.
	options
		The layout of the rows.

	Returns
	-------
	pandas.DataFrame
		One column per name found in the objects, holding Python objects.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.json_file import read_json_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.json"
	>>> _ = path.write_text('[{"city": "Paris", "count": 2}]')
	>>> read_json_file(path, ndp.JsonOptions())
	    city count
	0  Paris     2
	"""
	with path.open(encoding=JSON_ENCODING) as file:
		if options.layout == JsonLayout.LINES:
			content = file.read()
			records = read_json_lines(content)
		else:
			records = json.load(file)

	frame = pandas.DataFrame(records, dtype=PYTHON_OBJECT_DTYPE)

	return frame


def read_json_lines(content: str) -> list[Any]:
	r"""
	Return the objects of a JSON Lines text, one per line, skipping blank lines.

	.. versionadded:: 0.1.0

	Parameters
	----------
	content
		The whole text of the file.

	Returns
	-------
	list[Any]
		One decoded object per line that is not blank.

	Examples
	--------
	>>> from numdaplot.tables.files.json_file import read_json_lines
	>>> read_json_lines('{"price": 1}\n\n{"price": 2}\n')
	[{'price': 1}, {'price': 2}]
	"""
	lines = content.splitlines()
	records = list[Any]()

	for line in lines:
		stripped_line = line.strip()
		if stripped_line == "":
			continue

		record = json.loads(stripped_line)
		records.append(record)

	return records


def write_json_file(frame: pandas.DataFrame, path: Path, options: JsonOptions) -> None:
	"""
	Write the columns of a Table in a JSON file, one object per row, in UTF-8.

	Missing values are written as ``null``, dates and durations in the ISO 8601 format, and decimals with every
	digit of their value unless ``options`` gives their number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	path
		The path of the file, replaced when it exists.
	options
		The layout of the rows and the number of decimals.

	Raises
	------
	ValueConversionError
		At the first infinite value of a decimal column, which JSON cannot write.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.json_file import write_json_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.json"
	>>> write_json_file(pandas.DataFrame({"price": [1.5]}), path, ndp.JsonOptions())
	>>> path.read_text()
	'[{"price":1.5}]'
	"""
	writes_lines = options.layout == JsonLayout.LINES
	has_decimals = has_decimal_column(frame)
	if has_decimals:
		objects = write_exact_objects(frame, options.decimals)
		file_text = join_objects(objects, writes_lines)
		with path.open(WRITE_MODE, encoding=JSON_ENCODING, newline=UNCHANGED_NEWLINES) as file:
			file.write(file_text)

		return

	# Some versions of the pandas stubs leave the parameter types of to_json unknown.
	json_frame = cast(Any, frame)
	json_frame.to_json(
		path,
		orient=RECORDS_ORIENTATION,
		lines=writes_lines,
		force_ascii=False,
		date_format=ISO_DATE_FORMAT,
	)


def join_objects(objects: list[str], writes_lines: bool) -> str:
	r"""
	Return the whole text of a JSON file from its objects.

	.. versionadded:: 0.1.0

	Parameters
	----------
	objects
		One JSON object per row.
	writes_lines
		True for one object per line, False for one list holding them.

	Returns
	-------
	str
		The text of the file, each line ending with a line break in the layout of one object per line.

	Examples
	--------
	>>> from numdaplot.tables.files.json_file import join_objects
	>>> join_objects(['{"a":1}', '{"a":2}'], False)
	'[{"a":1},{"a":2}]'
	>>> join_objects(['{"a":1}', '{"a":2}'], True)
	'{"a":1}\n{"a":2}\n'
	"""
	if not writes_lines:
		joined_objects = OBJECT_SEPARATOR.join(objects)
		list_text = LIST_FORMAT.format(objects=joined_objects)
		return list_text

	if objects == []:
		return EMPTY_LINES_TEXT

	lines_text = LINE_END.join(objects) + LINE_END

	return lines_text
