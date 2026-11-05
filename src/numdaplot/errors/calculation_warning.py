"""
Warning emitted when a calculation on decimals gives NaN or an infinite value.

.. versionadded:: 0.1.0
"""


class CalculationWarning(UserWarning):
	"""
	Emitted when values of a calculation on decimals have no defined result or do not fit their type.

	The calculation still runs: these values become NaN or an infinite value. The warning points at the line of
	the calculation in the calling code.

	Silence it with the standard ``warnings`` module, for one block of code or for a whole script.

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
	>>> speeds
	Array([nan, 1.5], dtype=FLOAT64)
	>>> print(caught_warnings[0].message)
	The operation / has values without a defined result, such as 0 / 0: they became NaN.
	"""
