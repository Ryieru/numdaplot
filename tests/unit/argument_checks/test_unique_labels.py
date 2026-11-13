"""
Unit tests of the check that the values of a chart have different labels.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.argument_checks.unique_labels import require_unique_labels
from numdaplot.errors.plots.duplicate_label_error import DuplicateLabelError

UNIQUE_LABELS = ["Paris", "Lyon", "Pau"]
REPEATED_LABELS = ["Paris", "Lyon", "Paris", "Lyon"]


def test_require_unique_labels_accepts_different_labels() -> None:
	"""
	Check that different labels raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_unique_labels(UNIQUE_LABELS)


def test_require_unique_labels_rejects_the_first_repeated_label() -> None:
	"""
	Check that the first label seen twice raises DuplicateLabelError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateLabelError, match="'Paris'"):
		require_unique_labels(REPEATED_LABELS)


def test_require_unique_labels_accepts_no_label() -> None:
	"""
	Check that an empty list raises nothing.

	.. versionadded:: 0.1.0
	"""
	require_unique_labels([])
