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
	>>> prices = ndp.Array.from_list([80, 120])
	>>> for rule in [ndp.Greater(100), ndp.Less(100)]:
	... 	print(prices.select(rule))
	Array([120], dtype=INT64)
	Array([80], dtype=INT64)
	"""
