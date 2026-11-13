"""
Values whose mean is the share of the values satisfying a rule.

.. versionadded:: 0.2.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.rules.rule_mask import build_rule_mask
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.share import Share

SHARE_DTYPE = numpy.float64


def build_share_values(values: NDArray[Any], share: Share) -> NDArray[numpy.float64]:
	"""
	Return 1 where a value of an Array satisfies the rule of a share, 0 where it does not, NaN where it is not counted.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values of an Array.
	share
		The rule, and whether missing values are counted.

	Returns
	-------
	NDArray[numpy.float64]
		Values of the same shape, whose mean is the share.

	Raises
	------
	IncompatibleTypesError
		When the rule does not apply to the type of the values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.statistics.share_values import build_share_values
	>>> build_share_values(numpy.array([70.0, numpy.nan, 30.0]), ndp.Share(rule=ndp.Greater(65)))
	array([ 1., nan,  0.])
	"""
	matches = build_rule_mask(values, share.rule)
	missing = find_missing(values)
	share_values = mark_share_values(matches, missing, share.missing)

	return share_values


def mark_share_values(
	matches: NDArray[numpy.bool_],
	missing: NDArray[numpy.bool_],
	counted_missing: CountedMissing,
) -> NDArray[numpy.float64]:
	"""
	Return 1 at each match, 0 elsewhere, and NaN at each missing value when missing values are not counted.

	.. versionadded:: 0.2.0

	Parameters
	----------
	matches
		True at each value satisfying the rule.
	missing
		True at each missing value.
	counted_missing
		Whether the missing values count, as values not satisfying the rule.

	Returns
	-------
	NDArray[numpy.float64]
		Values whose mean is the share.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.statistics.share_values import mark_share_values
	>>> matches = numpy.array([True, False, False])
	>>> missing = numpy.array([False, True, False])
	>>> mark_share_values(matches, missing, ndp.CountedMissing.INCLUDED)
	array([1., 0., 0.])
	"""
	share_values = matches.astype(SHARE_DTYPE)
	if counted_missing == CountedMissing.EXCLUDED:
		share_values[missing] = numpy.nan

	return share_values
