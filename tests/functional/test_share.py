"""
Functional tests of the share of the values satisfying a rule.

.. versionadded:: 0.2.0
"""

import math

import pandas
import pytest

import numdaplot as ndp

SENIOR_RULE = ndp.Between(65, 99)
SENIOR_SHARE = ndp.Share(rule=SENIOR_RULE)
EVERY_ROW_SENIOR_SHARE = ndp.Share(rule=SENIOR_RULE, missing=ndp.CountedMissing.INCLUDED)
PRESENT_SHARE = 2 / 3
EVERY_ROW_SHARE = 0.5
PEOPLE = pandas.DataFrame(
	{
		"sex": [1, 2, 2, 1, 2],
		"city": pandas.Series(["Pau", "Lyon", "Pau", "Lyon", "Pau"], dtype="string"),
		"age": [30.0, 70.0, None, 80.0, 66.0],
	}
)
EXPECTED_GROUP_SHARES = [0.5, 1.0]
EXPECTED_EVERY_ROW_GROUP_SHARES = [0.5, 2 / 3]
EXPECTED_SHARE_COLUMN = "age_share"
EXPECTED_PIVOT_SHARES = [0.0, 1.0]
EXPECTED_DESCRIBED_SHARE = 0.75


def build_people() -> ndp.Table:
	"""
	Return a Table of five people with their sex, city and age, one age missing.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The people.
	"""
	people = ndp.Table.from_pandas(PEOPLE)

	return people


def test_share_of_an_array_leaves_out_the_missing_values() -> None:
	"""
	Check the share of seniors among the known ages.

	.. versionadded:: 0.2.0
	"""
	ages = ndp.Array.from_list([30.0, 70.0, None, 80.0])

	share = ages.compute(SENIOR_SHARE)

	share_value = share.to_value()
	is_expected_share = math.isclose(share_value, PRESENT_SHARE)
	assert is_expected_share


def test_share_of_an_array_counts_the_missing_values_when_included() -> None:
	"""
	Check the share of seniors among every row, a missing age counting as not senior.

	.. versionadded:: 0.2.0
	"""
	ages = ndp.Array.from_list([30.0, 70.0, None, 80.0])

	share = ages.compute(EVERY_ROW_SENIOR_SHARE)

	share_value = share.to_value()
	assert share_value == EVERY_ROW_SHARE


def test_share_gives_the_share_of_each_group() -> None:
	"""
	Check the share of seniors of each sex, named after the column.

	.. versionadded:: 0.2.0
	"""
	people = build_people()
	senior_share = ndp.Calculation(column="age", function=SENIOR_SHARE)

	shares = people.aggregate(ndp.Aggregation(calculations=[senior_share], group_by=["sex"]))

	share_values = shares.column(EXPECTED_SHARE_COLUMN)
	share_list = share_values.to_list()
	assert share_list == EXPECTED_GROUP_SHARES


def test_share_of_each_group_counts_the_missing_values_when_included() -> None:
	"""
	Check that a missing age lowers the share of its group when missing values count.

	.. versionadded:: 0.2.0
	"""
	people = build_people()
	senior_share = ndp.Calculation(column="age", function=EVERY_ROW_SENIOR_SHARE)

	shares = people.aggregate(ndp.Aggregation(calculations=[senior_share], group_by=["sex"]))

	share_values = shares.column(EXPECTED_SHARE_COLUMN)
	share_list = share_values.to_list()
	close_shares = [
		math.isclose(share, expected_share)
		for share, expected_share in zip(share_list, EXPECTED_EVERY_ROW_GROUP_SHARES, strict=True)
	]
	assert all(close_shares)


def test_share_gives_one_cell_per_combination_in_a_pivot_table() -> None:
	"""
	Check the share of seniors of each sex in Pau, the missing age left out.

	.. versionadded:: 0.2.0
	"""
	people = build_people()
	senior_share = ndp.Calculation(column="age", function=SENIOR_SHARE)

	shares = people.pivot_table(ndp.PivotTable(rows=["sex"], columns="city", calculation=senior_share))

	pau_shares = shares.column("Pau")
	pau_list = pau_shares.to_list()
	assert pau_list == EXPECTED_PIVOT_SHARES


def test_share_is_a_row_of_a_description() -> None:
	"""
	Check the share row of a description.

	.. versionadded:: 0.2.0
	"""
	people = build_people()

	description = people.describe(ndp.Description(functions=[SENIOR_SHARE], columns=["age"]))

	described_share = description.column("age")
	share_value = described_share.to_value()
	assert share_value == EXPECTED_DESCRIBED_SHARE


def test_share_rejects_a_rule_not_applying_to_the_values() -> None:
	"""
	Check that a number interval on texts raises IncompatibleTypesError.

	.. versionadded:: 0.2.0
	"""
	cities = ndp.Array.from_list(["Pau", "Lyon"])

	with pytest.raises(ndp.IncompatibleTypesError):
		cities.compute(SENIOR_SHARE)
