"""
Detection of a Jupyter notebook, where Tables and Plots are shown inside the page.

.. versionadded:: 0.2.0
"""

from importlib import import_module
from importlib.util import find_spec

IPYTHON_PACKAGE = "IPython"
NOTEBOOK_KERNEL = "IPKernelApp"


def is_notebook() -> bool:
	"""
	Return whether the code runs in a Jupyter notebook.

	IPython is optional: without it, the code never runs in a notebook.

	.. versionadded:: 0.1.0

	Returns
	-------
	bool
		True inside a Jupyter kernel, False in a terminal or a script.

	Examples
	--------
	>>> from numdaplot.display.notebook import is_notebook
	>>> is_notebook()
	False
	"""
	ipython_spec = find_spec(IPYTHON_PACKAGE)
	if ipython_spec is None:
		return False

	ipython_module = import_module(IPYTHON_PACKAGE)
	shell = ipython_module.get_ipython()
	if shell is None:
		return False

	runs_in_kernel = NOTEBOOK_KERNEL in shell.config

	return runs_in_kernel
