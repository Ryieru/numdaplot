"""
Whether text comparisons distinguish upper and lower case.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Case(Enum):
	"""
	Whether text comparisons distinguish upper and lower case, used by ``Contains``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "PARIS", "Lyon"])
	>>> cities.select(ndp.Contains("paris"))
	Array([], dtype=TEXT)
	>>> cities.select(ndp.Contains("paris", case=ndp.Case.IGNORED))
	Array(['Paris', 'PARIS'], dtype=TEXT)
	"""

	SENSITIVE = auto()
	"""``"paris"`` does not match ``"Paris"``, as in Python and pandas. Default value."""

	IGNORED = auto()
	"""``"paris"`` matches ``"Paris"``, ``"PARIS"`` and ``"paris"``."""
