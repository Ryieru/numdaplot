"""
Whether Count counts the missing values.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class CountedMissing(Enum):
	"""
	Whether ``Count`` counts the missing values.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Array.from_list([4.0, None, 2.0])
	>>> answers.compute(ndp.Count(missing=ndp.CountedMissing.INCLUDED)).to_value()
	3
	"""

	EXCLUDED = auto()
	"""
	Only the present values are counted. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Array.from_list([4.0, None, 2.0])
	>>> answers.compute(ndp.Count(missing=ndp.CountedMissing.EXCLUDED)).to_value()
	2
	"""

	INCLUDED = auto()
	"""
	Every value is counted, missing or not, which gives the number of rows of a column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Array.from_list([4.0, None, 2.0])
	>>> answers.compute(ndp.Count(missing=ndp.CountedMissing.INCLUDED)).to_value()
	3
	"""
