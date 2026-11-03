"""
Griffe extension turning the names written in code in the docstrings into links to their documentation.

Docstrings name objects in code, such as ``from_csv`` or ``ndp.Greater``, which editors show as they are.
In the documentation site, each such name that matches a documented object becomes a link to it:
a member of the class being documented, a public ``ndp.*`` name, or a member of a public class.
The links are optional, so a name without documentation stays plain code.

.. versionadded:: 0.1.0
"""

import re
from dataclasses import dataclass
from typing import Any

import griffe

CODE_SPAN = re.compile(r"(?<!`)``(?P<name>[A-Za-z_][\w.]*)(?:\(\))?``(?!`)")
PUBLIC_PREFIX = "ndp."
LINK_TEMPLATE = (
	'<span class="api-link api-link-{kind}"><autoref identifier="{identifier}" optional>{text}</autoref></span>'
)
CODE_TEMPLATE = "<code>{content}</code>"
PATH_SEPARATOR = "."


@dataclass(frozen=True)
class LinkContext:
	"""
	What the names of one docstring can link to.

	.. versionadded:: 0.1.0

	Parameters
	----------
	class_path
		The path of the documented class owning the docstring, or ``None`` outside any class.
	public_paths
		The path of each public ``ndp.*`` name, by name.
	loader
		The loader that holds every loaded module.
	"""

	class_path: str | None
	public_paths: dict[str, str]
	loader: griffe.GriffeLoader


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

	def replace_name(name_match: re.Match[str]) -> str:
		"""
		Return the link replacing one name, or the name itself when it matches no object.

		.. versionadded:: 0.1.0

		Parameters
		----------
		name_match
			The match of a name written in code.

		Returns
		-------
		str
			The link, or the original code.
		"""
		name = name_match.group("name")
		identifier = find_identifier(name, context)
		if identifier is None:
			return name_match.group(0)

		code_text = name_match.group(0).strip("`")
		links = build_links(code_text, identifier, context.loader)
		code = CODE_TEMPLATE.format(content=links)

		return code

	linked_text = CODE_SPAN.sub(replace_name, docstring_text)

	return linked_text


def build_links(code_text: str, identifier: str, loader: griffe.GriffeLoader) -> str:
	"""
	Return the links of a name: one for the whole name, or one for its owner and one for its member.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code_text
		The name as written, such as ``Conflict.ERROR``, ``ndp.Greater`` or ``from_csv()``. The ``ndp.`` prefix
		stays part of the first link.
	identifier
		The path of the object the whole name refers to.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str
		The links, joined by a dot when the name holds one.
	"""
	prefix = PUBLIC_PREFIX if code_text.startswith(PUBLIC_PREFIX) else ""
	short_text = code_text.removeprefix(PUBLIC_PREFIX)
	owner_text, separator, member_text = short_text.rpartition(PATH_SEPARATOR)
	if separator == "":
		whole_link = build_link(code_text, identifier, loader)
		return whole_link

	owner_identifier, _, _ = identifier.rpartition(PATH_SEPARATOR)
	owner_link = build_link(prefix + owner_text, owner_identifier, loader)
	member_link = build_link(member_text, identifier, loader)
	links = owner_link + PATH_SEPARATOR + member_link

	return links


def build_link(text: str, identifier: str, loader: griffe.GriffeLoader) -> str:
	"""
	Return an optional link to an object, in a span whose class names the kind of the object.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text of the link.
	identifier
		The path of the object.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str
		The link, such as ``api-link-class`` for a class, ``api-link-object`` for an unknown object.
	"""
	target = find_object(identifier, loader)
	kind = "object" if target is None else target.kind.value
	link = LINK_TEMPLATE.format(kind=kind, identifier=identifier, text=text)

	return link


def find_identifier(name: str, context: LinkContext) -> str | None:
	"""
	Return the path of the documented object a name refers to.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		A name written in code, such as ``from_csv``, ``ndp.Greater`` or ``Table.from_csv``.
	context
		What the name can link to.

	Returns
	-------
	str or None
		The path of the object: first a member of the documented class, then a public name or a member
		of a public class. ``None`` when nothing matches.
	"""
	short_name = name.removeprefix(PUBLIC_PREFIX)
	candidates = list[str]()
	if context.class_path is not None:
		candidates.append(context.class_path + PATH_SEPARATOR + short_name)

	head, _, rest = short_name.partition(PATH_SEPARATOR)
	if head in context.public_paths:
		public_path = context.public_paths[head]
		candidate = public_path if rest == "" else public_path + PATH_SEPARATOR + rest
		candidates.append(candidate)

	for candidate in candidates:
		exists = object_exists(candidate, context.loader)
		if exists:
			return candidate

	return None


def object_exists(path: str, loader: griffe.GriffeLoader) -> bool:
	"""
	Return whether griffe knows an object at a path, inherited members included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an object, such as ``numdaplot.tables.table.Table.from_csv``.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	bool
		True when the object exists.
	"""
	target = find_object(path, loader)
	exists = target is not None

	return exists


def find_object(path: str, loader: griffe.GriffeLoader) -> griffe.Object | griffe.Alias | None:
	"""
	Return the object griffe knows at a path, inherited members included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an object, such as ``numdaplot.tables.table.Table.from_csv``.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	griffe.Object, griffe.Alias or None
		The object, or ``None`` when there is none at this path.
	"""
	owner_path, _, member_name = path.rpartition(PATH_SEPARATOR)
	try:
		owner = loader.modules_collection.get_member(owner_path)
	except (KeyError, ValueError):
		return None

	if not isinstance(owner, griffe.Object):
		return None

	target = owner.all_members.get(member_name)

	return target


def find_public_paths(package: griffe.Module) -> dict[str, str]:
	"""
	Return the path of each public name of a package, by name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package
		The package whose ``__init__`` exposes the public names.

	Returns
	-------
	dict[str, str]
		The path of the object each exported alias points to.
	"""
	public_paths = dict[str, str]()

	for name, member in package.members.items():
		if isinstance(member, griffe.Alias):
			public_paths[name] = member.target_path

	return public_paths


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
		context = LinkContext(class_path, base_context.public_paths, base_context.loader)
		linked_text = link_code_names(obj.docstring.value, context)
		obj.docstring.value = linked_text

	for member in obj.members.values():
		if isinstance(member, griffe.Alias):
			continue

		link_object_docstrings(member, class_owners, base_context)


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
		public_paths = find_public_paths(pkg)
		class_owners = find_class_owners(pkg, public_paths)
		base_context = LinkContext(None, public_paths, loader)
		link_object_docstrings(pkg, class_owners, base_context)
