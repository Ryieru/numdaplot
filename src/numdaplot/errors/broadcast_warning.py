"""
Warning emitted when two Arrays of different shapes are combined.

.. versionadded:: 0.1.0
"""


class BroadcastWarning(UserWarning):
	"""
	Emitted when an operation stretches an Array to match the shape of another one.

	The operation still runs, as in numpy. The warning only signals that the shapes differ,
	which is often a mistake. It is never emitted when an Array is combined with a single value.

	Silence it with the standard ``warnings`` module, for one block of code or for a whole script.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import warnings
	>>> import numdaplot as ndp
	>>> with warnings.catch_warnings():
	... 	warnings.simplefilter("ignore", category=ndp.BroadcastWarning)
	"""
