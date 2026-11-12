"""
Unit tests of the natural order of texts.

.. versionadded:: 0.2.0
"""

from numdaplot.ordering.natural_order import find_natural_key

CLUSTER_NAMES = ["Noise", "Cluster 10", "Cluster 2", "Cluster 0"]
EXPECTED_CLUSTER_ORDER = ["Cluster 0", "Cluster 2", "Cluster 10", "Noise"]
MIXED_CASE_NAMES = ["banana", "Apple", "cherry"]
EXPECTED_CASE_ORDER = ["Apple", "banana", "cherry"]
CASE_TWINS = ["paris", "Paris"]
EXPECTED_TWIN_ORDER = ["Paris", "paris"]
PADDED_NUMBERS = ["x10", "x02", "x1"]
EXPECTED_PADDED_ORDER = ["x1", "x02", "x10"]
SUPERSCRIPT_TEXTS = ["x²", "x2"]
EXPECTED_SUPERSCRIPT_ORDER = ["x2", "x²"]
HOURS = ["10:00", "09:30", "00:05"]
EXPECTED_HOUR_ORDER = ["00:05", "09:30", "10:00"]


def test_find_natural_key_reads_numbers_as_numbers() -> None:
	"""
	Check that Cluster 2 comes before Cluster 10.

	.. versionadded:: 0.2.0
	"""
	sorted_names = sorted(CLUSTER_NAMES, key=find_natural_key)

	assert sorted_names == EXPECTED_CLUSTER_ORDER


def test_find_natural_key_ignores_case() -> None:
	"""
	Check that a capital letter does not come before every small letter.

	.. versionadded:: 0.2.0
	"""
	sorted_names = sorted(MIXED_CASE_NAMES, key=find_natural_key)

	assert sorted_names == EXPECTED_CASE_ORDER


def test_find_natural_key_orders_texts_equal_but_for_case() -> None:
	"""
	Check that texts equal but for their case keep a fixed order, whatever their order before.

	.. versionadded:: 0.2.0
	"""
	sorted_names = sorted(CASE_TWINS, key=find_natural_key)

	assert sorted_names == EXPECTED_TWIN_ORDER


def test_find_natural_key_reads_leading_zeros_as_the_same_number() -> None:
	"""
	Check that 02 counts as 2.

	.. versionadded:: 0.2.0
	"""
	sorted_names = sorted(PADDED_NUMBERS, key=find_natural_key)

	assert sorted_names == EXPECTED_PADDED_ORDER


def test_find_natural_key_keeps_other_digit_signs_as_letters() -> None:
	"""
	Check that a superscript two, which is not a decimal digit, is compared as a letter.

	.. versionadded:: 0.2.0
	"""
	sorted_names = sorted(SUPERSCRIPT_TEXTS, key=find_natural_key)

	assert sorted_names == EXPECTED_SUPERSCRIPT_ORDER


def test_find_natural_key_orders_times_of_day() -> None:
	"""
	Check that times written HH:MM follow the day.

	.. versionadded:: 0.2.0
	"""
	sorted_hours = sorted(HOURS, key=find_natural_key)

	assert sorted_hours == EXPECTED_HOUR_ORDER
