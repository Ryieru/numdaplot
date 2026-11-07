"""
Warning emitted when a chart is likely to be hard to read.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_warning import NumdaplotWarning


class ReadabilityWarning(NumdaplotWarning):
	"""
	Emitted when a chart is likely to be hard to read, such as a ``PieChart`` of more than 5 slices.

	The Plot is still created. The warning suggests a chart that shows the same values more clearly, or a larger
	size when only some of the labels naming the values of a chart can be shown.

	Silence it with the standard ``warnings`` module, for one block of code or for a whole script, alone or with every
	``NumdaplotWarning``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import warnings
	>>> fruits = ndp.Array.from_list(["apple", "pear", "plum", "fig", "kiwi", "lime"])
	>>> sales = ndp.Array.from_list([30.0, 25.0, 15.0, 12.0, 10.0, 8.0])
	>>> shares = ndp.Table.from_arrays({"fruit": fruits, "sales": sales})
	>>> chart = ndp.PieChart(labels="fruit", values="sales")
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	plot = ndp.Plot.pie(shares, chart)
	>>> print(caught_warnings[0].message)
	A PieChart with 6 slices is hard to read. Try ndp.Plot.bar with a BarChart, it may compare them better.
	"""
