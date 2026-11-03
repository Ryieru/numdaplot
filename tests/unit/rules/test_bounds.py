"""
Unit tests of the bound inclusion settings.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.bounds import HIGH_INCLUDED_BOUNDS, LOW_INCLUDED_BOUNDS, Bounds


def test_low_included_bounds_keep_the_low_bound() -> None:
	"""
	Check that INCLUDED and LOW_ONLY are the settings keeping the low bound.

	.. versionadded:: 0.1.0
	"""
	assert LOW_INCLUDED_BOUNDS == {Bounds.INCLUDED, Bounds.LOW_ONLY}


def test_high_included_bounds_keep_the_high_bound() -> None:
	"""
	Check that INCLUDED and HIGH_ONLY are the settings keeping the high bound.

	.. versionadded:: 0.1.0
	"""
	assert HIGH_INCLUDED_BOUNDS == {Bounds.INCLUDED, Bounds.HIGH_ONLY}
