"""
The ``ndp.Table`` class: named columns, each holding values of one type.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.table_calculation import TableCalculation
from numdaplot.tables.table_columns import TableColumns
from numdaplot.tables.table_conversion import TableConversion
from numdaplot.tables.table_display import TableDisplay
from numdaplot.tables.table_layout import TableLayout
from numdaplot.tables.table_reading import TableReading
from numdaplot.tables.table_refusals import TableRefusals
from numdaplot.tables.table_selection import TableSelection
from numdaplot.tables.table_writing import TableWriting


class Table(
	TableReading,
	TableWriting,
	TableConversion,
	TableSelection,
	TableColumns,
	TableCalculation,
	TableLayout,
	TableDisplay,
	TableRefusals,
):
	"""
	Named columns, each holding values of one type, wrapping a pandas DataFrame.

	A Table never changes: every operation returns a new Table. Its rows are numbered from 0, and renumbered
	after a filter or a sort. Integer, boolean and text columns accept missing values.

	- Create it with ``from_csv``, ``from_json``, ``from_excel``, ``from_parquet``, ``from_stata``, ``from_sas``,
	``from_xpt``, ``from_pandas`` or ``from_arrays``.
	- Write it with ``to_csv``, ``to_json``, ``to_excel``, ``to_parquet`` or ``to_stata``.
	- Select rows with ``filter`` and ``take``, read a column with ``column``.
	- Change columns with ``choose_columns``, ``rename``, ``convert`` and ``add_column``.
	- Compute with ``aggregate`` and ``describe``.
	- Rearrange rows with ``sort`` and ``drop_duplicates``.
	- Read it with ``row_count``, ``column_names``, ``column_types``, ``to_value``, ``to_pandas`` and ``is_equal``,
	and show it with ``preview`` or ``print``.

	Comparisons, brackets, ``for``, ``in``, ``len`` and ``bool`` are refused with ``RefusedOperationError``,
	which names the method to use instead.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> total = ndp.Calculation(column="price", function=ndp.Sum())
	>>> sales.aggregate(ndp.Aggregation(calculations=[total], group_by=["city"]))
	city price_sum
	TEXT   FLOAT64
	0   Lyon      80.0
	1  Paris     270.0
	"""
