"""
Detection of texts holding a real date beyond what a count of nanoseconds can hold.

.. versionadded:: 0.1.0
"""

import re
from datetime import datetime

from numdaplot.arrays.operations.time_bounds import is_python_time_in_range
from numdaplot.dates.custom_date_format import CustomDateFormat

NO_CLOCK_PART = "0"
DATE_PART_NAMES = ("year", "month", "day", "hour", "minute", "second")


def read_moment_text(text: str, read_pattern: str) -> datetime | None:
	r"""
	Return a text read as a datetime with a regular expression naming the parts of a date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		A text without spaces around it.
	read_pattern
		The regular expression, whose groups are named after the parts of a date. A part it leaves out counts as 0.

	Returns
	-------
	datetime or None
		The datetime, or ``None`` for a text that does not follow the pattern or is not a real date.

	Examples
	--------
	>>> from numdaplot.tables.columns.date_range import read_moment_text
	>>> read_moment_text("3000-12-31", r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
	datetime.datetime(3000, 12, 31, 0, 0)
	>>> read_moment_text("3000-02-31", r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})") is None
	True
	"""
	match = re.fullmatch(read_pattern, text)
	if match is None:
		return None

	found_parts = match.groupdict()
	part_values = list[int]()
	for part_name in DATE_PART_NAMES:
		part_text = found_parts.get(part_name) or NO_CLOCK_PART
		part_value = int(part_text)
		part_values.append(part_value)

	year, month, day, hour, minute, second = part_values
	try:
		moment = datetime(year, month, day, hour, minute, second)
	except ValueError:
		return None

	return moment


def read_custom_text(text: str, date_format: CustomDateFormat) -> datetime | None:
	"""
	Return a text read as a datetime with a custom date format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		A text without spaces around it.
	date_format
		The custom pattern.

	Returns
	-------
	datetime or None
		The datetime, or ``None`` for a text that does not follow the pattern or is not a real date.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.date_range import read_custom_text
	>>> read_custom_text("31 Dec 3000", ndp.CustomDateFormat("%d %b %Y"))
	datetime.datetime(3000, 12, 31, 0, 0)
	"""
	try:
		moment = datetime.strptime(text, date_format.pattern)
	except ValueError:
		return None

	return moment


def is_text_out_of_range(text: str, read_format: str | CustomDateFormat) -> bool:
	"""
	Return whether a text holds a real date that a count of nanoseconds cannot hold.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		A text, with or without spaces around it.
	read_format
		A regular expression naming the parts of a date, or a custom pattern.

	Returns
	-------
	bool
		True for a real date out of range, False for an accepted date or for a text that is not a date.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.date_range import is_text_out_of_range
	>>> is_text_out_of_range("31 Dec 3000", ndp.CustomDateFormat("%d %b %Y"))
	True
	>>> is_text_out_of_range("31 Dec 2026", ndp.CustomDateFormat("%d %b %Y"))
	False
	"""
	stripped_text = text.strip()
	moment = None
	if isinstance(read_format, CustomDateFormat):
		moment = read_custom_text(stripped_text, read_format)
	else:
		moment = read_moment_text(stripped_text, read_format)

	if moment is None:
		return False

	moment_in_range = is_python_time_in_range(moment)

	return not moment_in_range
