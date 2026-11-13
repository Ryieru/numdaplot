"""
Shape and values of nested Python lists.

.. versionadded:: 0.1.0
"""

from typing import cast

from numdaplot.errors.positions.irregular_list_error import IrregularListError

EMPTY_LIST_DIMENSIONS = (0,)


def find_list_shape(values: list[object]) -> tuple[int, ...]:
	"""
	Return the dimensions of nested lists forming a regular block.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A list of single values, or a list of lists nested to any depth.

	Returns
	-------
	tuple[int, ...]
		The number of elements at each nesting level.

	Raises
	------
	IrregularListError
		When the lists at one level have different lengths, or mix lists and single values.

	Examples
	--------
	>>> from numdaplot.arrays.creation.list_shape import find_list_shape
	>>> find_list_shape([[1, 2, 3], [4, 5, 6]])
	(2, 3)
	"""
	value_count = len(values)
	if value_count == 0:
		return EMPTY_LIST_DIMENSIONS

	nested_lists = [cast(list[object], value) for value in values if isinstance(value, list)]
	nested_list_count = len(nested_lists)
	if nested_list_count == 0:
		return (value_count,)

	if nested_list_count != value_count:
		raise IrregularListError()

	nested_shapes = {find_list_shape(nested_list) for nested_list in nested_lists}
	shape_count = len(nested_shapes)
	if shape_count != 1:
		raise IrregularListError()

	nested_shape = nested_shapes.pop()
	dimensions = (value_count, *nested_shape)

	return dimensions


def flatten_list(values: list[object]) -> list[object]:
	"""
	Return the single values of nested lists, row after row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A list of single values, or a list of lists nested to any depth.

	Returns
	-------
	list[object]
		Every single value, in reading order.

	Examples
	--------
	>>> from numdaplot.arrays.creation.list_shape import flatten_list
	>>> flatten_list([[1, 2], [3, 4]])
	[1, 2, 3, 4]
	"""
	single_values = list[object]()

	for value in values:
		if isinstance(value, list):
			nested_list = cast(list[object], value)
			nested_values = flatten_list(nested_list)
			single_values.extend(nested_values)
			continue

		single_values.append(value)

	return single_values
