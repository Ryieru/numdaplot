"""
The settings of a conversion of a Table column or of the values of an Array.

.. versionadded:: 0.2.0
"""

from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.table_conversion import TableConversion

type ConversionSettings = TableConversion | ArrayConversion
"""The new type and the settings of a conversion, of a Table column or of the values of an Array.

.. versionadded:: 0.2.0
"""
