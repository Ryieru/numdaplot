"""
Layouts of the rows of a JSON file.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class JsonLayout(Enum):
	"""
	Layout of the rows of a JSON file, used by ``JsonOptions``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.JsonLayout.LINES
	<JsonLayout.LINES: 2>
	"""

	RECORDS = auto()
	"""One list holding one object per row: ``[{"city": "Paris"}, {"city": "Lyon"}]``. Default value."""

	LINES = auto()
	"""One object per line, without enclosing list, also called JSON Lines."""
