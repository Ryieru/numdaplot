"""
Griffe extension leaving out the docstrings of the ``__init__`` methods from the documentation site.

The class docstring documents the creation of an object: its parameters and the errors it raises. The docstring of
``__init__`` repeats them for editors, and mkdocstrings would add it at the end of the class page, inherited by the
subclasses that have no ``__init__`` of their own. This extension removes it when ``mkdocs`` reads the docstrings;
the source files keep it.

.. versionadded:: 0.2.0
"""

from typing import Any

import griffe

INIT_NAME = "__init__"


def is_class_init(obj: griffe.Object) -> bool:
	"""
	Return whether an object is the ``__init__`` method of a class.

	.. versionadded:: 0.2.0

	Parameters
	----------
	obj
		A module, class, function or attribute read by griffe.

	Returns
	-------
	bool
		True for a function named ``__init__`` defined in a class.

	Examples
	--------
	>>> import griffe
	>>> from init_docstrings import is_class_init
	>>> sale = griffe.Class("Sale")
	>>> sale.set_member("__init__", griffe.Function("__init__"))
	>>> is_class_init(sale.members["__init__"])
	True
	"""
	is_init_function = isinstance(obj, griffe.Function) and obj.name == INIT_NAME
	is_in_class = isinstance(obj.parent, griffe.Class)
	is_class_init_function = is_init_function and is_in_class

	return is_class_init_function


class InitDocstrings(griffe.Extension):
	"""
	Griffe extension removing the docstring of every ``__init__`` method of a class.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler.

	.. versionadded:: 0.2.0
	"""

	def on_object(self, *, obj: griffe.Object, **kwargs: Any) -> None:
		"""
		Remove the docstring of an object when it is the ``__init__`` method of a class.

		.. versionadded:: 0.2.0

		Parameters
		----------
		obj
			A module, class, function or attribute read by griffe.
		**kwargs
			The other arguments griffe gives to its extensions, unused.
		"""
		is_init = is_class_init(obj)
		if not is_init:
			return

		obj.docstring = None
