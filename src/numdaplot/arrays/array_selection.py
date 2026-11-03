"""
Selection of the values of an Array, by rule and by position.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.selection.region_index import build_region_index
from numdaplot.arrays.selection.replaced_values import replace_region
from numdaplot.arrays.selection.rule_mask import build_rule_mask
from numdaplot.positions.region import Region
from numdaplot.rules.rule import Rule

if TYPE_CHECKING:
	from numdaplot.arrays.replacement import Replacement


class ArraySelection(ArrayData):
	"""
	Selection of the values of an Array.

	By rule with ``select`` and ``check``, by position with ``take`` and ``replace``.

	.. versionadded:: 0.1.0
	"""

	def select(self, rule: Rule) -> Self:
		"""
		Return the values satisfying a rule, in one dimension.

		.. versionadded:: 0.1.0

		Parameters
		----------
		rule
			Any rule of numdaplot, such as ``ndp.Greater(10)``. A missing value only satisfies ``IsMissing``.

		Returns
		-------
		Self
			A new one-dimensional Array, in reading order.

		Raises
		------
		IncompatibleTypesError
			When the rule does not apply to the type of the values.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([[5, 12], [30, 8]])
		>>> prices.select(ndp.Greater(10))
		Array([12, 30], dtype=INT64)
		"""
		mask = build_rule_mask(self._values, rule)
		selected_values = self._values[mask]
		selected_array = self._wrap(selected_values)

		return selected_array

	def check(self, rule: Rule) -> Self:
		"""
		Return whether each value satisfies a rule, keeping the shape.

		Combine several checks with ``&``, ``|`` and ``~``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		rule
			Any rule of numdaplot. A missing value only satisfies ``IsMissing``.

		Returns
		-------
		Self
			A new ``BOOL`` Array of the same shape.

		Raises
		------
		IncompatibleTypesError
			When the rule does not apply to the type of the values.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
		>>> cities.check(ndp.Contains("Pa"))
		Array([ True, False,  True], dtype=BOOL)
		"""
		mask = build_rule_mask(self._values, rule)
		mask_array = self._wrap(mask)

		return mask_array

	def take(self, region: Region) -> Self:
		"""
		Return the values of a region of a one- or two-dimensional Array.

		A row or a column chosen with ``Index`` keeps its dimension: one row of a two-dimensional
		Array is still two-dimensional. Use ``to_value`` to read a single value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		region
			The rows and the columns to take, every one of a dimension when omitted.
			Negative positions count from the end.

		Returns
		-------
		Self
			A new Array with as many dimensions as this one.

		Raises
		------
		DimensionError
			When the Array has more than two dimensions, or columns are given for a one-dimensional Array.
		RefusedOperationError
			When columns are given as names, which only a Table has.
		InvalidPositionError
			When a position is not a whole number inside its dimension.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> grid = ndp.Array.from_list([[1, 2, 3], [4, 5, 6]])
		>>> grid.take(ndp.Region(rows=ndp.Index(-1), columns=ndp.Range(start=0, stop=1)))
		Array([[4, 5]], dtype=INT64)
		"""
		region_index = build_region_index(region, self._values.shape)
		region_values = self._values[region_index]
		region_array = self._wrap(region_values)

		return region_array

	def replace(self, replacement: Replacement) -> Self:
		"""
		Return a new Array whose region is replaced; this Array does not change.

		.. versionadded:: 0.1.0

		Parameters
		----------
		replacement
			The region, and a single value or an Array of exactly the shape of the region.

		Returns
		-------
		Self
			A new Array of the same shape and type.

		Raises
		------
		UnsupportedOperandError
			When the new value is neither an Array nor a single value.
		ShapeMismatchError
			When an Array of new values does not have the shape of the region.
		ValueConversionError
			When the new values cannot be stored in the type of the Array without losing information.
		DimensionError, RefusedOperationError, InvalidPositionError
			When the region does not fit the Array, as in ``take``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> scores = ndp.Array.from_list([10, 20, 30])
		>>> scores.replace(ndp.Replacement(region=ndp.Region(rows=ndp.Index(1)), value=0))
		Array([10,  0, 30], dtype=INT64)
		"""
		new_values = self._read_operand(replacement.value)
		replaced_values = replace_region(self._values, replacement.region, new_values)
		replaced_array = self._wrap(replaced_values)

		return replaced_array
