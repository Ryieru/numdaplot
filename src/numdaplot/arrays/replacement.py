"""
Settings of the replacement of a region of an Array.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numdaplot.positions.region import Region
from numdaplot.rules.rule_values import ScalarValue

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array


# eq=False because comparing two settings would compare their Arrays with ==, which Array refuses.
@dataclass(frozen=True, eq=False)
class Replacement:
	"""
	Settings of the replacement of a region of an Array, used by ``Array.replace``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	region
		The positions to replace.
	value
		A ``ScalarValue``, such as ``0`` or ``"Paris"``, written at every position of the region, or an Array of
		exactly the shape of the region. Its type must fit in the type of the Array: a decimal cannot replace
		an integer.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> scores = ndp.Array.from_list([10, 20, 30])
	>>> first_score = ndp.Region(rows=ndp.Index(0))
	>>> scores.replace(ndp.Replacement(region=first_score, value=0))
	Array([ 0, 20, 30], dtype=INT64)
	"""

	region: Region
	value: ScalarValue | Array
