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
	>>> ndp.Contains("paris", case=ndp.Case.IGNORED).case
	<Case.IGNORED: 2>
	"""

	SENSITIVE = auto()
	"""``"paris"`` does not match ``"Paris"``, as in Python and pandas. Default value."""

	IGNORED = auto()
	"""``"paris"`` matches ``"Paris"``, ``"PARIS"`` and ``"paris"``."""
