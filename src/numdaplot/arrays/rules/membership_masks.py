"""
Masks of the rules looking for values in a list or for a text inside each value.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.operand import convert_time_value
from numdaplot.arrays.operations.type_requirements import require_comparable, require_family
from numdaplot.arrays.rules.time_reference import remove_far_references
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.rules.case import Case
from numdaplot.rules.contains import Contains
from numdaplot.rules.is_in import IsIn
from numdaplot.types.value_family import ValueFamily

IS_IN_NAME = "IsIn"
CONTAINS_NAME = "Contains"
TEXT_FAMILIES = frozenset({ValueFamily.TEXT})
EMPTY_TEXT = ""
NOT_FOUND_POSITION = -1


def build_membership_mask(values: NDArray[Any], rule: IsIn[Any]) -> NDArray[numpy.bool_]:
	"""
	Return which values belong to the accepted values of an ``IsIn`` rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	rule
		The accepted values.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each accepted value. A missing value is never accepted.

	Raises
	------
	IncompatibleTypesError
		When the accepted values cannot be compared with the values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.membership_masks import build_membership_mask
	>>> build_membership_mask(numpy.array([1, 2, 3]), ndp.IsIn([1, 3]))
	array([ True, False,  True])
	"""
	first_accepted_value = rule.values[0]
	require_comparable(values, first_accepted_value, IS_IN_NAME)

	near_values = remove_far_references(values, rule.values)
	accepted_values = [convert_time_value(accepted_value) for accepted_value in near_values]
	matches = numpy.isin(values, accepted_values)
	missing = find_missing(values)
	present = ~missing
	mask = matches & present

	return mask


def build_contains_mask(values: NDArray[Any], rule: Contains) -> NDArray[numpy.bool_]:
	"""
	Return which texts contain the text of a ``Contains`` rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a ``TEXT`` Array.
	rule
		The searched text and whether case is ignored.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each text containing the searched text.

	Raises
	------
	IncompatibleTypesError
		When the values are not texts.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.membership_masks import build_contains_mask
	>>> build_contains_mask(numpy.array(["Paris", "Lyon"]), ndp.Contains("paris", case=ndp.Case.IGNORED))
	array([ True, False])
	"""
	require_family(values, TEXT_FAMILIES, CONTAINS_NAME)

	missing = find_missing(values)
	present = ~missing
	# numpy cannot search a missing text. The mask of the present texts removes the empty text standing for it.
	searched_values = numpy.where(missing, EMPTY_TEXT, values)
	searched_text = rule.text
	if rule.case == Case.IGNORED:
		searched_values = numpy.strings.lower(searched_values)
		searched_text = rule.text.lower()

	positions = numpy.strings.find(searched_values, searched_text)
	found = positions != NOT_FOUND_POSITION
	mask = found & present

	return mask
