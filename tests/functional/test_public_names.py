"""
Functional tests of the names shown by the package.

.. versionadded:: 0.1.0
"""

import numdaplot as ndp

INTERNAL_NAMES = {"arrays", "errors", "find_package_version", "package_version", "tables"}
FUNCTION_STYLE_PLOT_NAME = "plot_line"
VERSION_NAME = "__version__"


def test_dir_shows_every_public_name() -> None:
	"""
	Check that every name of ``ndp.__all__`` is shown.

	.. versionadded:: 0.1.0
	"""
	shown_names = dir(ndp)
	public_names = set(ndp.__all__)

	assert public_names.issubset(shown_names)


def test_dir_shows_the_version() -> None:
	"""
	Check that ``__version__`` is shown, even if it is not an object of the API.

	.. versionadded:: 0.1.0
	"""
	shown_names = dir(ndp)

	assert VERSION_NAME in shown_names


def test_dir_hides_the_internal_names() -> None:
	"""
	Check that the modules and the functions loaded by the imports of the package are not shown.

	.. versionadded:: 0.1.0
	"""
	shown_names = dir(ndp)
	shown_internal_names = INTERNAL_NAMES.intersection(shown_names)

	assert shown_internal_names == set()


def test_changing_the_result_of_dir_changes_nothing() -> None:
	"""
	Check that the list returned by ``__dir__`` is not ``__all__`` itself.

	.. versionadded:: 0.1.0
	"""
	shown_names = ndp.__dir__()
	public_name_count = len(ndp.__all__)

	shown_names.clear()

	assert len(ndp.__all__) == public_name_count


def test_plots_are_only_created_from_the_plot_class() -> None:
	"""
	Check that the package has no plot creation of its own besides ``ndp.Plot``.

	.. versionadded:: 0.1.0
	"""
	has_function_style_name = hasattr(ndp, FUNCTION_STYLE_PLOT_NAME)

	assert not has_function_style_name
