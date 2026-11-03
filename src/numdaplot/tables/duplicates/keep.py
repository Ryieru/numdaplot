"""
Which row of a group of duplicated rows is kept.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Keep(Enum):
	"""
	Which row of a group of duplicated rows is kept, used by ``Deduplication``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Keep.NONE
	<Keep.NONE: 3>
	"""

	FIRST = auto()
	"""The first row of each group is kept. Default value."""

	LAST = auto()
	"""The last row of each group is kept."""

	NONE = auto()
	"""No row of a duplicated group is kept, only rows that appear once remain."""
