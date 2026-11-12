"""
Groups of number types: integers and decimals.

.. versionadded:: 0.2.0
"""

from numdaplot.data_types.type import Type

INTEGER_TYPES = frozenset(
	{Type.INT8, Type.INT16, Type.INT32, Type.INT64, Type.UINT8, Type.UINT16, Type.UINT32, Type.UINT64}
)
DECIMAL_TYPES = frozenset({Type.FLOAT32, Type.FLOAT64})
