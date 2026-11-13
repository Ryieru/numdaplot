"""
Numbers of a regular sequence.

.. versionadded:: 0.1.0
"""

import math
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.positions.range import Range
from numdaplot.rules.bounds import HIGH_INCLUDED_BOUNDS, LOW_INCLUDED_BOUNDS

# Decimal steps accumulate rounding errors, so the end of a range is compared with a tolerance.
STEP_TOLERANCE = 1e-9


def compute_range_values(sequence: Range) -> NDArray[Any]:
	"""
	Return the numbers of a regular sequence.

	A stop reached within a tiny fraction of a step counts as reached, so ``Range(0, 1, 0.1)``
	ends with exactly 1.0 when the stop is included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sequence
		The sequence. ``LOW_ONLY`` keeps its start and drops its stop, ``HIGH_ONLY`` the opposite.

	Returns
	-------
	NDArray
		Integers when the start and the step are integers, decimals otherwise.
		Empty when the excluded bounds leave no number, such as from 1 to 1 with ``Bounds.EXCLUDED``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.range_values import compute_range_values
	>>> compute_range_values(ndp.Range(start=0, stop=10, step=5))
	array([ 0,  5, 10])
	"""
	distance = sequence.stop - sequence.start
	step_count = distance / sequence.step
	nearest_step_count = round(step_count)
	step_count_error = abs(step_count - nearest_step_count)
	reaches_stop = step_count_error <= STEP_TOLERANCE
	tolerated_step_count = step_count + STEP_TOLERANCE

	first_index = 0
	if sequence.bounds not in LOW_INCLUDED_BOUNDS:
		first_index = 1

	last_index = math.floor(tolerated_step_count)
	includes_stop = sequence.bounds in HIGH_INCLUDED_BOUNDS
	drops_reached_stop = reaches_stop and not includes_stop
	if drops_reached_stop:
		last_index -= 1

	index_limit = last_index + 1
	indexes = numpy.arange(first_index, index_limit)
	offsets = indexes * sequence.step
	values = sequence.start + offsets
	has_values = indexes.size > 0
	ends_on_stop = reaches_stop and includes_stop and has_values
	if ends_on_stop:
		values[-1] = sequence.stop

	return values
