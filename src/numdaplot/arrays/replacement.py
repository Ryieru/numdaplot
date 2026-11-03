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
		A single value written at every position of the region, or an Array of exactly the shape
		of the region. Its type must fit in the type of the Array: a decimal cannot replace an integer.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> first_value = ndp.Region(rows=ndp.Index(0))
	>>> ndp.Replacement(region=first_value, value=0)
	Replacement(region=Region(rows=Index(position=0), columns=None), value=0)
	"""

	region: Region
	value: ScalarValue | Array
