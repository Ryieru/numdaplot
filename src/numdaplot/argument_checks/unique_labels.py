"""
Check that labels are all different, such as the slices of a PieChart or the brackets of Brackets.

.. versionadded:: 0.1.0
"""

from collections.abc import Iterable

from numdaplot.errors.plots.duplicate_label_error import DuplicateLabelError


def require_unique_labels(labels: Iterable[str]) -> None:
	"""
	Check that every labeled value has its own label, such as the slices of a PieChart or the brackets of Brackets.

	.. versionadded:: 0.1.0

	Parameters
	----------
	labels
		The label of each value.

	Raises
	------
	DuplicateLabelError
		At the first label already seen.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.argument_checks.unique_labels import require_unique_labels
	>>> try:
	... 	require_unique_labels(numpy.array(["Paris", "Lyon", "Paris"], dtype=object))
	... except ndp.DuplicateLabelError as error:
	... 	print(error)
	The label 'Paris' appears more than once.
	"""
	seen_labels = set[str]()

	for label in labels:
		if label in seen_labels:
			raise DuplicateLabelError(label)

		seen_labels.add(label)
