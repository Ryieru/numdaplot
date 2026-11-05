"""
Griffe extension showing a public base class in the place of a base class that numdaplot does not export.

The rules comparing each value to a reference value share ``ValueRule``, a detail of their code that has no page.
Their pages show ``Rule``, the class a reader knows. This extension runs last: it only changes what the pages show.

.. versionadded:: 0.1.0
"""

from typing import Any

import griffe

HIDDEN_BASES = {"numdaplot.rules.value_rule.ValueRule": "numdaplot.rules.rule.Rule"}
PATH_SEPARATOR = "."


def replace_hidden_bases(cls: griffe.Class, hidden_bases: dict[str, str], loader: griffe.GriffeLoader) -> None:
	"""
	Replace the base classes of a class that have no page with the public class standing for them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cls
		A class, whose bases are updated in place.
	hidden_bases
		The path of the public class standing for each hidden base class, by path.
	loader
		The loader that holds every loaded module.
	"""
	shown_bases = list[Any]()

	for base in cls.bases:
		base_path = base.canonical_path if isinstance(base, griffe.Expr) else base
		public_path = hidden_bases.get(base_path)
		if public_path is None:
			shown_bases.append(base)
			continue

		module_path, _, class_name = public_path.rpartition(PATH_SEPARATOR)
		module = loader.modules_collection.get_member(module_path)
		public_base = griffe.ExprName(class_name, parent=module)
		shown_bases.append(public_base)

	cls.bases = shown_bases


def replace_package_bases(obj: griffe.Object, hidden_bases: dict[str, str], loader: griffe.GriffeLoader) -> None:
	"""
	Replace the hidden base classes of every class in a module and everything below it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	obj
		A module or a class loaded by griffe.
	hidden_bases
		The path of the public class standing for each hidden base class, by path.
	loader
		The loader that holds every loaded module.
	"""
	if isinstance(obj, griffe.Class):
		replace_hidden_bases(obj, hidden_bases, loader)

	for member in obj.members.values():
		if isinstance(member, griffe.Module | griffe.Class):
			replace_package_bases(member, hidden_bases, loader)


class PublicBases(griffe.Extension):
	"""
	Griffe extension showing a public base class in the place of a hidden one.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler, last.

	.. versionadded:: 0.1.0
	"""

	def on_package(self, *, pkg: griffe.Module, loader: griffe.GriffeLoader, **kwargs: Any) -> None:
		"""
		Replace the hidden base classes of a loaded package.

		.. versionadded:: 0.1.0

		Parameters
		----------
		pkg
			The package griffe loaded.
		loader
			The loader that holds every loaded module.
		**kwargs
			The other arguments griffe gives to its extensions, unused.
		"""
		replace_package_bases(pkg, HIDDEN_BASES, loader)
