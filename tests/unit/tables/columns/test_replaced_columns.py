"""
Unit tests of the replacement of columns of a Table by a change made to each of them.

.. versionadded:: 0.2.0
"""

import pandas
import pytest

from numdaplot.column_storage.column import Column
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.tables.columns.replaced_columns import replace_frame_columns

AREA_NAME = "area"
CITY_NAME = "city"
UNKNOWN_NAME = "volume"
FRAME = pandas.DataFrame({AREA_NAME: [4.0, 9.0], CITY_NAME: ["Pau", "Dax"]})
AREA_NAMES = [AREA_NAME]
UNKNOWN_NAMES = [AREA_NAME, UNKNOWN_NAME]
REVERSED_NAMES = [CITY_NAME, AREA_NAME]
EXPECTED_COLUMN_NAMES = [AREA_NAME, CITY_NAME]
EXPECTED_DOUBLED_AREAS = [8.0, 18.0]
EXPECTED_AREAS = [4.0, 9.0]
EXPECTED_CITIES = ["Pau", "Dax"]
DOUBLING_FACTOR = 2
REFUSED_OPERATION = "Doubling"
REFUSED_TYPE_NAMES = ["FLOAT64"]


class RecordedChanges:
	"""
	Fake change of a column, recording the columns it receives.

	.. versionadded:: 0.2.0
	"""

	def __init__(self) -> None:
		"""
		Start without any recorded column.

		.. versionadded:: 0.2.0
		"""
		self.column_names = list[str]()

	def record(self, column: Column) -> Column:
		"""
		Record the name of the column and return it unchanged.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column
			The column to change.

		Returns
		-------
		Column
			The column itself.
		"""
		column_name = str(column.name)
		self.column_names.append(column_name)

		return column


def double_column(column: Column) -> Column:
	"""
	Fake change doubling the values of a column.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		A column of numbers.

	Returns
	-------
	Column
		The doubled values.
	"""
	doubled_column = column * DOUBLING_FACTOR

	return doubled_column


def refuse_column(column: Column) -> Column:
	"""
	Fake change refusing every column with a type error.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		The column, ignored.

	Returns
	-------
	Column
		Never returns.

	Raises
	------
	IncompatibleTypesError
		Always.
	"""
	raise IncompatibleTypesError(REFUSED_OPERATION, REFUSED_TYPE_NAMES)


def test_replace_frame_columns_replaces_the_listed_columns_at_their_place() -> None:
	"""
	Check that the listed column holds the change and keeps its place, the other columns unchanged.

	.. versionadded:: 0.2.0
	"""
	changed_frame = replace_frame_columns(FRAME, AREA_NAMES, double_column)

	column_names = changed_frame.columns.tolist()
	areas = changed_frame[AREA_NAME].tolist()
	cities = changed_frame[CITY_NAME].tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert areas == EXPECTED_DOUBLED_AREAS
	assert cities == EXPECTED_CITIES


def test_replace_frame_columns_leaves_the_given_columns_unchanged() -> None:
	"""
	Check that the source DataFrame keeps its values.

	.. versionadded:: 0.2.0
	"""
	replace_frame_columns(FRAME, AREA_NAMES, double_column)

	areas = FRAME[AREA_NAME].tolist()
	assert areas == EXPECTED_AREAS


def test_replace_frame_columns_checks_every_column_before_changing_one() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError before any column is changed.

	.. versionadded:: 0.2.0
	"""
	recorder = RecordedChanges()

	with pytest.raises(ColumnNotFoundError):
		replace_frame_columns(FRAME, UNKNOWN_NAMES, recorder.record)

	assert recorder.column_names == []


def test_replace_frame_columns_changes_the_columns_in_the_order_of_the_list() -> None:
	"""
	Check that each listed column goes to the change, in the order of the list.

	.. versionadded:: 0.2.0
	"""
	recorder = RecordedChanges()

	replace_frame_columns(FRAME, REVERSED_NAMES, recorder.record)

	assert recorder.column_names == REVERSED_NAMES


def test_replace_frame_columns_names_the_failing_column() -> None:
	"""
	Check that an error about the values names the column being changed.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(IncompatibleTypesError) as error_info:
		replace_frame_columns(FRAME, AREA_NAMES, refuse_column)

	assert error_info.value.column_name == AREA_NAME
