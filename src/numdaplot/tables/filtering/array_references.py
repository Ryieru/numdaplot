"""
Rules comparing a Table column with an Array, kept to the rows of the column that hold a value.

.. versionadded:: 0.2.0
"""

import dataclasses
from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array import create_array
from numdaplot.arrays.array_data import ArrayData, read_stored_values
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.rules.rule import Rule
from numdaplot.rules.value_rule import ValueRule

ARRAY_REFERENCE_OPERATION = "A rule comparing a column with an Array"


def keep_present_reference(rule: Rule, present: NDArray[numpy.bool_], time_zone: TimeZone | None) -> Rule:
	"""
	Return a rule whose Array of reference values only keeps the rows where the column holds a value.

	The values of a column are tested without their missing values, so the reference values must follow the same
	rows. A rule without Array is returned as it is.

	.. versionadded:: 0.2.0

	Parameters
	----------
	rule
		Any rule of numdaplot.
	present
		True at each row of the column holding a value.
	time_zone
		The time zone of the column, or None.

	Returns
	-------
	Rule
		The rule, its Array reduced to the rows holding a value.

	Raises
	------
	ShapeMismatchError
		When the Array does not hold one value per row of the column.
	TimeZoneMismatchError
		When the column holds datetimes with a time zone, which an Array cannot hold.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.array_references import keep_present_reference
	>>> arrivals = ndp.Array.from_list(["Pau", "Nice", "Dax"])
	>>> present = numpy.array([True, False, True])
	>>> keep_present_reference(ndp.Equal(arrivals), present, None).value
	Array(['Pau', 'Dax'], dtype=TEXT)
	"""
	if not isinstance(rule, ValueRule):
		return rule

	value_rule = cast(ValueRule[Any], rule)
	reference = value_rule.value
	if not isinstance(reference, ArrayData):
		return value_rule

	if time_zone is not None:
		raise TimeZoneMismatchError(ARRAY_REFERENCE_OPERATION, False)

	reference_values = read_stored_values(reference)
	row_count = present.size
	column_shape = (row_count,)
	if reference_values.shape != column_shape:
		raise ShapeMismatchError(column_shape, reference_values.shape)

	present_values = reference_values[present]
	present_reference = create_array(present_values)
	present_rule = dataclasses.replace(value_rule, value=present_reference)

	return present_rule
