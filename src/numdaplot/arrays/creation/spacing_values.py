"""
Evenly spaced numbers.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.creation.spacing import Spacing
from numdaplot.rules.bounds import HIGH_INCLUDED_BOUNDS, LOW_INCLUDED_BOUNDS


def compute_spacing_values(spacing: Spacing) -> NDArray[Any]:
	"""
	Return the evenly spaced numbers of a spacing.

	The interval is cut into equal gaps: one fewer than the count when both bounds are kept,
	one more when both are dropped.

	.. versionadded:: 0.1.0

	Parameters
	----------
	spacing
		The spacing.

	Returns
	-------
	NDArray
		``count`` decimals. An included stop is exactly ``stop``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.spacing_values import compute_spacing_values
	>>> compute_spacing_values(ndp.Spacing(start=0, stop=1, count=4, bounds=ndp.Bounds.LOW_ONLY))
	array([0.  , 0.25, 0.5 , 0.75])
	"""
	includes_start = spacing.bounds in LOW_INCLUDED_BOUNDS
	includes_stop = spacing.bounds in HIGH_INCLUDED_BOUNDS

	gap_count = spacing.count + 1
	first_offset = 1
	if includes_start:
		gap_count -= 1
		first_offset = 0

	if includes_stop:
		gap_count -= 1

	distance = spacing.stop - spacing.start
	gap = distance / gap_count
	offset_limit = first_offset + spacing.count
	offsets = numpy.arange(first_offset, offset_limit)
	distances = offsets * gap
	values = spacing.start + distances
	if includes_stop:
		values[-1] = spacing.stop

	return values
