"""
Error raised when a chart labels two values with the same text.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DUPLICATE_LABEL_MESSAGE = "The label {label!r} appears more than once."


class DuplicateLabelError(NumdaplotError):
	"""
	Raised when two slices of a ``PieChart`` have the same label, which could not tell them apart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	label
		The repeated label.

	Attributes
	----------
	label
		The repeated label.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Paris"])
	>>> sales = ndp.Array.from_list([120.0, 80.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales")
	>>> try:
	... 	ndp.Plot.pie(shares, chart)
	... except ndp.DuplicateLabelError as error:
	... 	print(error)
	The label 'Paris' appears more than once.
	"""

	def __init__(self, label: str) -> None:
		"""
		Build the error message from the label.

		.. versionadded:: 0.1.0

		Parameters
		----------
		label
			The repeated label.
		"""
		message = DUPLICATE_LABEL_MESSAGE.format(label=label)
		super().__init__(message)
		self.label = label
