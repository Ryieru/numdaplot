"""
pytest settings shared by every test and every docstring example.

.. versionadded:: 0.1.0
"""

import matplotlib

# The examples end with ``plot.show()``: this matplotlib backend opens no window, so the tests never wait.
matplotlib.use("Agg")
