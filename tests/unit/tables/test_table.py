"""
Unit tests of Table.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.array import Array
from numdaplot.tables.sorting.sort_key import SortKey
from numdaplot.tables.sorting.sorting import Sorting
from numdaplot.tables.table import Table
from numdaplot.tables.table_calculation import TableCalculation
from numdaplot.tables.table_columns import TableColumns
from numdaplot.tables.table_conversion import TableConversion
from numdaplot.tables.table_display import TableDisplay
from numdaplot.tables.table_layout import TableLayout
from numdaplot.tables.table_reading import TableReading
from numdaplot.tables.table_refusals import TableRefusals
from numdaplot.tables.table_selection import TableSelection
from numdaplot.tables.table_writing import TableWriting

METHOD_GROUPS = [
	TableReading,
	TableWriting,
	TableConversion,
	TableSelection,
	TableColumns,
	TableCalculation,
	TableLayout,
	TableDisplay,
	TableRefusals,
]
PRICES = Array.from_list([2.0, 1.0])


@pytest.mark.parametrize("method_group", METHOD_GROUPS)
def test_table_offers_every_group_of_methods(method_group: type) -> None:
	"""
	Check that Table inherits each group of methods.

	.. versionadded:: 0.1.0

	Parameters
	----------
	method_group
		A group of Table methods.
	"""
	assert issubclass(Table, method_group)


def test_table_operations_return_tables() -> None:
	"""
	Check that an operation inherited from a group returns a Table, not the group class.

	.. versionadded:: 0.1.0
	"""
	table = Table.from_arrays({"price": PRICES})

	sorted_table = table.sort(Sorting(keys=[SortKey(column="price")]))

	assert type(sorted_table) is Table
