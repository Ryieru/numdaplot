"""
Reading and writing JSON files.

.. versionadded:: 0.1.0
"""

import json
from pathlib import Path
from typing import Any, cast

import pandas

from numdaplot.tables.files.json_layout import JsonLayout
from numdaplot.tables.files.json_options import JsonOptions

JSON_ENCODING = "utf-8"
RECORDS_ORIENTATION = "records"
ISO_DATE_FORMAT = "iso"
PYTHON_OBJECT_DTYPE = object


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

	Missing values are written as ``null``, dates and durations in the ISO 8601 format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	path
		The path of the file, replaced when it exists.
	options
		The layout of the rows.

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
	# Some versions of the pandas stubs leave the parameter types of to_json unknown.
	json_frame = cast(Any, frame)
	json_frame.to_json(
		path,
		orient=RECORDS_ORIENTATION,
		lines=writes_lines,
		force_ascii=False,
		date_format=ISO_DATE_FORMAT,
	)
