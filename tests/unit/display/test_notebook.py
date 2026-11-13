"""
Unit tests of the detection of a Jupyter notebook.

.. versionadded:: 0.2.0
"""

from types import SimpleNamespace
from typing import Any

import pytest

from numdaplot.display import notebook
from numdaplot.display.notebook import is_notebook

IMPORT_MODULE_NAME = "import_module"
FIND_SPEC_NAME = "find_spec"
NOTEBOOK_CONFIG = dict[str, object]({"IPKernelApp": None})
TERMINAL_CONFIG = dict[str, object]()
FOUND_PACKAGE = object()


def build_fake_ipython(config: dict[str, object] | None) -> SimpleNamespace:
	"""
	Return a fake IPython module whose shell has a configuration, or no shell.

	.. versionadded:: 0.1.0

	Parameters
	----------
	config
		The configuration of the shell, or ``None`` for no shell.

	Returns
	-------
	SimpleNamespace
		A module with a ``get_ipython`` function.
	"""
	shell = None
	if config is not None:
		shell = SimpleNamespace(config=config)

	fake_module = SimpleNamespace(get_ipython=lambda: shell)

	return fake_module


def find_no_package(package_name: str) -> None:
	"""
	Fake package lookup that finds nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The searched package, ignored.
	"""
	return None


def find_any_package(package_name: str) -> object:
	"""
	Fake package lookup that finds every package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The searched package, ignored.

	Returns
	-------
	object
		A found package.
	"""
	return FOUND_PACKAGE


def test_is_notebook_is_false_without_ipython(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a missing IPython means no notebook.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the package lookup with one that finds nothing.
	"""
	monkeypatch.setattr(notebook, FIND_SPEC_NAME, find_no_package)

	runs_in_notebook = is_notebook()

	assert not runs_in_notebook


@pytest.mark.parametrize(
	("config", "expected_answer"),
	[
		(None, False),
		(TERMINAL_CONFIG, False),
		(NOTEBOOK_CONFIG, True),
	],
)
def test_is_notebook_checks_for_a_jupyter_kernel(
	monkeypatch: pytest.MonkeyPatch,
	module_giver: Any,
	config: dict[str, object] | None,
	expected_answer: bool,
) -> None:
	"""
	Check the answer without shell, in an IPython terminal and in a Jupyter kernel.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces IPython with a fake.
	module_giver
		Builds the fake import giving the fake IPython.
	config
		The configuration of the fake shell, or None for no shell.
	expected_answer
		Whether it is a notebook.
	"""
	fake_ipython = build_fake_ipython(config)
	monkeypatch.setattr(notebook, FIND_SPEC_NAME, find_any_package)
	fake_import = module_giver(fake_ipython)
	monkeypatch.setattr(notebook, IMPORT_MODULE_NAME, fake_import)

	runs_in_notebook = is_notebook()

	assert runs_in_notebook == expected_answer
