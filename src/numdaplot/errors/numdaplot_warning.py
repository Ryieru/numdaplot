"""
Base class of every numdaplot warning.

.. versionadded:: 0.1.0
"""


class NumdaplotWarning(UserWarning):
	"""
	Base class of every warning emitted by numdaplot.

	Filter it with the standard ``warnings`` module to silence, or turn into errors, every numdaplot warning at once
	and only them. Filter a precise subclass to handle only one case.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import warnings
	>>> distances = ndp.Array.from_list([0.0, 3.0])
	>>> hours = ndp.Array.from_list([0.0, 2.0])
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	speeds = distances / hours
	>>> isinstance(caught_warnings[0].message, ndp.NumdaplotWarning)
	True
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warnings.simplefilter("ignore", ndp.NumdaplotWarning)
	... 	speeds = distances / hours
	>>> caught_warnings
	[]
	"""
