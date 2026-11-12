"""
Unit tests of the griffe extension leaving out the docstrings of the ``__init__`` methods.

.. versionadded:: 0.2.0
"""

import griffe
from init_docstrings import InitDocstrings, is_class_init

CLASS_NAME = "Sale"
MODULE_NAME = "sales"
INIT_NAME = "__init__"
METHOD_NAME = "total"
INIT_TEXT = "Keep the price.\n\nParameters\n----------\nprice\n    The price."
METHOD_TEXT = "Return the total."


def create_class_methods() -> tuple[griffe.Function, griffe.Function]:
	"""
	Return the ``__init__`` method and another method of a class, both documented.

	.. versionadded:: 0.2.0

	Returns
	-------
	tuple[griffe.Function, griffe.Function]
		The ``__init__`` method, then the ``total`` method, both members of the class ``Sale``.
	"""
	init_docstring = griffe.Docstring(INIT_TEXT)
	method_docstring = griffe.Docstring(METHOD_TEXT)
	init_function = griffe.Function(INIT_NAME, docstring=init_docstring)
	method_function = griffe.Function(METHOD_NAME, docstring=method_docstring)
	sale = griffe.Class(CLASS_NAME)
	sale.set_member(INIT_NAME, init_function)
	sale.set_member(METHOD_NAME, method_function)

	return init_function, method_function


def test_is_class_init_finds_the_init_method_of_a_class() -> None:
	"""
	Check that the ``__init__`` method of a class is recognized.

	.. versionadded:: 0.2.0
	"""
	init_function, _ = create_class_methods()

	is_init = is_class_init(init_function)

	assert is_init


def test_is_class_init_skips_another_method() -> None:
	"""
	Check that a method with another name is not an ``__init__`` method.

	.. versionadded:: 0.2.0
	"""
	_, method_function = create_class_methods()

	is_init = is_class_init(method_function)

	assert not is_init


def test_is_class_init_skips_a_module_function_named_init() -> None:
	"""
	Check that a function named ``__init__`` outside a class is not an ``__init__`` method.

	.. versionadded:: 0.2.0
	"""
	module = griffe.Module(MODULE_NAME)
	module_function = griffe.Function(INIT_NAME)
	module.set_member(INIT_NAME, module_function)

	is_init = is_class_init(module_function)

	assert not is_init


def test_init_docstrings_remove_the_docstring_of_an_init_method() -> None:
	"""
	Check that the extension leaves the ``__init__`` method of a class without docstring.

	.. versionadded:: 0.2.0
	"""
	init_function, _ = create_class_methods()
	extension = InitDocstrings()

	extension.on_object(obj=init_function)

	assert init_function.docstring is None


def test_init_docstrings_keep_the_docstring_of_another_method() -> None:
	"""
	Check that the extension keeps the docstring of a method other than ``__init__``.

	.. versionadded:: 0.2.0
	"""
	_, method_function = create_class_methods()
	extension = InitDocstrings()

	extension.on_object(obj=method_function)

	method_docstring = method_function.docstring
	assert method_docstring is not None
	assert method_docstring.value == METHOD_TEXT
