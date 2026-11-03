"""
How the conditions of a Filter combine.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class FilterMode(Enum):
	"""
	How the conditions of a ``Filter`` combine to keep a row.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.FilterMode.ANY
	<FilterMode.ANY: 2>
	"""

	ALL = auto()
	"""A row is kept when it satisfies every condition. Default value."""

	ANY = auto()
	"""A row is kept when it satisfies at least one condition."""
