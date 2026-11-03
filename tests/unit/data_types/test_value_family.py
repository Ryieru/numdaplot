"""
Unit tests of ValueFamily and find_family.

.. versionadded:: 0.1.0
"""

from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family


def test_find_family_groups_integers_and_decimals_as_numbers() -> None:
	"""
	Check that an unsigned integer and a decimal are both numbers.

	.. versionadded:: 0.1.0
	"""
	integer_family = find_family(Type.UINT8)
	decimal_family = find_family(Type.FLOAT32)

	assert integer_family == ValueFamily.NUMBER
	assert decimal_family == ValueFamily.NUMBER


def test_find_family_groups_dates_and_datetimes_as_moments() -> None:
	"""
	Check that dates and datetimes belong to the same family.

	.. versionadded:: 0.1.0
	"""
	date_family = find_family(Type.DATE)
	datetime_family = find_family(Type.DATETIME)

	assert date_family == ValueFamily.MOMENT
	assert datetime_family == ValueFamily.MOMENT


def test_find_family_groups_categories_with_texts() -> None:
	"""
	Check that a category is compared like a text.

	.. versionadded:: 0.1.0
	"""
	category_family = find_family(Type.CATEGORY)

	assert category_family == ValueFamily.TEXT


def test_find_family_classifies_every_type() -> None:
	"""
	Check that every member of Type has a family.

	.. versionadded:: 0.1.0
	"""
	families = [find_family(data_type) for data_type in Type]

	family_count = len(families)
	type_count = len(Type)
	assert family_count == type_count
