"""
Rules comparing a Table column with an Array, kept to the rows of the column that hold a value.

.. versionadded:: 0.2.0
"""

import dataclasses
from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array import Array, create_array
from numdaplot.arrays.array_data import ArrayData, read_stored_values
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.rules.rule import Rule

ARRAY_REFERENCE_OPERATION = "A rule comparing a column with an Array"


def keep_present_reference(rule: Rule, present: NDArray[numpy.bool_], time_zone: TimeZone | None) -> Rule:
	"""
	Return a rule whose Arrays of reference values only keep the rows where the column holds a value.

	The values of a column are tested without their missing values, so the reference values must follow the same
	rows, such as the value of ``Equal`` or the bounds of ``Between``. A rule without Array is returned as it is.

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
		The rule, each of its Arrays reduced to the rows holding a value.

	Raises
	------
	ShapeMismatchError
		When an Array does not hold one value per row of the column.
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
	is_dataclass_rule = dataclasses.is_dataclass(rule)
	if not is_dataclass_rule:
		return rule

	rule_fields = dataclasses.fields(rule)
	present_references = dict[str, Array]()

	for rule_field in rule_fields:
		field_value = getattr(rule, rule_field.name)
		if isinstance(field_value, ArrayData):
			present_references[rule_field.name] = keep_present_rows(field_value, present)

	if not present_references:
		return rule

	if time_zone is not None:
		raise TimeZoneMismatchError(ARRAY_REFERENCE_OPERATION, False)

	dataclass_rule = cast(Any, rule)
	present_rule = dataclasses.replace(dataclass_rule, **present_references)

	return present_rule


def keep_present_rows(reference: ArrayData, present: NDArray[numpy.bool_]) -> Array:
	"""
	Return the values of a reference Array at the rows where a column holds a value.

	.. versionadded:: 0.2.0

	Parameters
	----------
	reference
		An Array with one value per row of the column.
	present
		True at each row of the column holding a value.

	Returns
	-------
	Array
		The values of the rows holding a value, in order.

	Raises
	------
	ShapeMismatchError
		When the Array does not hold one value per row of the column.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.array_references import keep_present_rows
	>>> keep_present_rows(ndp.Array.from_list([10.0, 20.0, 30.0]), numpy.array([True, False, True]))
	Array([10., 30.], dtype=FLOAT64)
	"""
	reference_values = read_stored_values(reference)
	row_count = present.size
	column_shape = (row_count,)
	if reference_values.shape != column_shape:
		raise ShapeMismatchError(column_shape, reference_values.shape)

	present_values = reference_values[present]
	present_reference = create_array(present_values)

	return present_reference
