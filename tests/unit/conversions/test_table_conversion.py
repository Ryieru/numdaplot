"""
Unit tests of TableConversion.

.. versionadded:: 0.2.0
"""

from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.data_types.type import Type

COLUMN_NAME = "price"


def test_conversion_keeps_its_settings() -> None:
	"""
	Check that the column and the type are available as attributes.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(column=COLUMN_NAME, dtype=Type.TEXT)

	assert conversion.column == COLUMN_NAME
	assert conversion.dtype == Type.TEXT
