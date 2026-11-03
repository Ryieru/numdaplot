"""
Base class of every rule.

.. versionadded:: 0.1.0
"""


class Rule:
	"""
	Base class of every rule, a test applied to each value of an Array or of Table columns.

	A rule is immutable and checks its settings when it is created.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> isinstance(ndp.Greater(100), ndp.Rule)
	True
	"""
