"""
Whether a ColumnChoice keeps or drops its columns.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ColumnMode(Enum):
	"""
	Whether a ``ColumnChoice`` keeps or drops the columns it names.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.ColumnMode.DROP
	<ColumnMode.DROP: 2>
	"""

	KEEP = auto()
	"""Only the named columns remain, in the order of the list. Default value."""

	DROP = auto()
	"""The named columns are removed, the others keep their order."""
