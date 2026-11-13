"""
Griffe extension turning the names written in code in the docstrings into links to their documentation.

Docstrings name objects in code, alone or in a call, which editors show as they are.
In the documentation site, each name of such code that matches a documented object becomes a link to it:
a member of the class being documented, a public ``ndp.*`` name, a member of a public class, an enum member
that only one public class has, or the argument of a call to a public class. Texts between quotes stay as they
are. The links are optional, so a name without documentation stays plain code.

.. versionadded:: 0.1.0
"""

import re
from dataclasses import replace
from typing import Any

import griffe
from code_links import link_code_tokens
from link_targets import LinkContext, find_enum_member_paths, find_public_paths, find_unique_member_paths
from value_types import find_value_type_paths, link_type_parameters

CODE_SPAN = re.compile(r"(?<!`)``(?P<code>[^`\n]+)``(?!`)")
CODE_TEMPLATE = "<code>{content}</code>"


def link_code_names(docstring_text: str, context: LinkContext) -> str:
	"""
	Return a docstring whose names written in code link to their documentation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring_text
		The text of a docstring.
	context
		What the names can link to.

	Returns
	-------
	str
		The same text, each name that matches an object written as code holding optional links, in spans
		whose class names the kind of the object, such as ``api-link-class``. A name such as
		``Conflict.ERROR`` links its class and its member separately, each with its own kind.
	"""

	def replace_code(code_match: re.Match[str]) -> str:
		"""
		Return the code with its links, or the code itself when no name matches an object.

		.. versionadded:: 0.1.0

		Parameters
		----------
		code_match
			The match of a text written in code.

		Returns
		-------
		str
			The code holding links, or the original code.
		"""
		code_text = code_match.group("code")
		links = link_code_tokens(code_text, context)
		if links is None:
			return code_match.group(0)

		code = CODE_TEMPLATE.format(content=links)

		return code

	linked_text = CODE_SPAN.sub(replace_code, docstring_text)

	return linked_text


def find_class_owners(package: griffe.Module, public_paths: dict[str, str]) -> dict[str, str]:
	"""
	Return the public class documenting each class, mixins included.

	``Table`` is documented with the methods of its mixins, such as ``TableReading``: a docstring of a mixin
	links to the members of ``Table``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package
		The loaded package.
	public_paths
		The path of each public name.

	Returns
	-------
	dict[str, str]
		The path of the public class, by path of each of its base classes and of itself.
	"""
	class_owners = dict[str, str]()

	for public_path in public_paths.values():
		public_object = package.modules_collection.get_member(public_path)
		if not isinstance(public_object, griffe.Class):
			continue

		class_owners[public_path] = public_path
		for base_class in public_object.mro():
			class_owners.setdefault(base_class.path, public_path)

	return class_owners


def link_object_docstrings(obj: griffe.Object, class_owners: dict[str, str], base_context: LinkContext) -> None:
	"""
	Link the names of the docstring of an object and of its members.

	.. versionadded:: 0.1.0

	Parameters
	----------
	obj
		A module, class, function or attribute loaded by griffe.
	class_owners
		The public class documenting each class.
	base_context
		The public names and the loader, without class.
	"""
	owning_class = obj if isinstance(obj, griffe.Class) else obj.parent
	class_path = None
	if isinstance(owning_class, griffe.Class):
		class_path = class_owners.get(owning_class.path, owning_class.path)

	if obj.docstring is not None:
		context = replace(base_context, class_path=class_path)
		linked_text = link_code_names(obj.docstring.value, context)
		obj.docstring.value = linked_text

	for member in obj.members.values():
		if isinstance(member, griffe.Alias):
			continue

		link_object_docstrings(member, class_owners, base_context)


def link_package_type_parameters(
	obj: griffe.Object, value_type_paths: dict[str, str], loader: griffe.GriffeLoader
) -> None:
	"""
	Make the type parameters named after a value type refer to it, in a module and everything below it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	obj
		A module or a class loaded by griffe.
	value_type_paths
		The path of each value type, by name.
	loader
		The loader that holds every loaded module.
	"""
	if isinstance(obj, griffe.Class):
		link_type_parameters(obj, value_type_paths, loader)

	for member in obj.members.values():
		if isinstance(member, griffe.Module | griffe.Class):
			link_package_type_parameters(member, value_type_paths, loader)


class CrossReferences(griffe.Extension):
	"""
	Griffe extension turning the names written in code into links to their documentation.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler.

	.. versionadded:: 0.1.0
	"""

	def on_package(self, *, pkg: griffe.Module, loader: griffe.GriffeLoader, **kwargs: Any) -> None:
		"""
		Link the names of every docstring of a loaded package.

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
		value_type_paths = find_value_type_paths(loader)
		public_paths = find_public_paths(pkg) | value_type_paths
		class_owners = find_class_owners(pkg, public_paths)
		unique_member_paths = find_unique_member_paths(public_paths, loader)
		enum_member_paths = find_enum_member_paths(unique_member_paths)
		base_context = LinkContext(None, public_paths, loader, enum_member_paths)
		link_object_docstrings(pkg, class_owners, base_context)
		link_package_type_parameters(pkg, value_type_paths, loader)
