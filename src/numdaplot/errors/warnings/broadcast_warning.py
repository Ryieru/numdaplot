"""
Warning emitted when two Arrays of different shapes are combined.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_warning import NumdaplotWarning


class BroadcastWarning(NumdaplotWarning):
	"""
	Emitted when an operation stretches an Array to match the shape of another one.

	The operation still runs, as in numpy. The warning only signals that the shapes differ,
	which is often a mistake. It is never emitted when an Array is combined with a single value.

	Silence it with the standard ``warnings`` module, for one block of code or for a whole script, alone or with every
	``NumdaplotWarning``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import warnings
	>>> grid = ndp.Array.from_list([[1, 2], [3, 4]])
	>>> row = ndp.Array.from_list([10, 20])
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	sums = grid + row
	>>> sums
	Array([[11, 22],
	       [13, 24]], dtype=INT64)
	>>> print(caught_warnings[0].message)
	Shapes (2, 2) and (2,) differ, values are repeated to match.
	"""
