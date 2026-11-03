"""
Type of the pandas columns a Table stores.

.. versionadded:: 0.1.0
"""

from typing import Any

import pandas

type Column = pandas.Series[Any]
"""A pandas column of a Table, stored with one of the dtypes given by ``to_pandas_dtype``.

.. versionadded:: 0.1.0
"""
