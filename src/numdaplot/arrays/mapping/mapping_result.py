"""
The new values a ValueMapping gives, before they are stored.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.data_types.type import Type


@dataclass(frozen=True)
class MappingResult:
	"""
	The new values a ``ValueMapping`` gives to flat values, and the type that stores them.

	.. versionadded:: 0.2.0

	Parameters
	----------
	new_values
		The new Python values, in order, None for a missing one.
	result_type
		The type holding every new value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import find_mapping_result
	>>> mapping = ndp.ValueMapping(changes=[ndp.ValueChange(7, None)], others=ndp.Unmatched.KEEP)
	>>> mapping_result = find_mapping_result(numpy.array([1, 7]), mapping)
	>>> mapping_result.new_values, mapping_result.result_type
	([1, None], <Type.INT64: 4>)
	"""

	new_values: list[object]
	result_type: Type
