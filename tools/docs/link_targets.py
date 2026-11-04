"""
What the names written in code in the documentation can link to.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

import griffe

PUBLIC_PREFIX = "ndp."
PATH_SEPARATOR = "."
PRIVATE_PREFIX = "_"


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
	enum_member_paths
		The path of each enum member that only one public class has, by name.
	"""

	class_path: str | None
	public_paths: dict[str, str]
	loader: griffe.GriffeLoader
	enum_member_paths: dict[str, str]


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


def find_unique_member_paths(public_paths: dict[str, str], loader: griffe.GriffeLoader) -> dict[str, str]:
	"""
	Return the path of each public member name that only one public class has.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_paths
		The path of each public name.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	dict[str, str]
		The path of each member, by name. A name shared by several classes, such as ``to_value``, is left out.
	"""
	paths_by_name = dict[str, list[str]]()

	for public_path in public_paths.values():
		public_object = loader.modules_collection.get_member(public_path)
		if not isinstance(public_object, griffe.Class):
			continue

		for member_name in public_object.all_members:
			if member_name.startswith(PRIVATE_PREFIX):
				continue

			member_path = public_path + PATH_SEPARATOR + member_name
			member_name_paths = paths_by_name.setdefault(member_name, [])
			member_name_paths.append(member_path)

	unique_paths = {name: paths[0] for name, paths in paths_by_name.items() if len(paths) == 1}

	return unique_paths


def find_enum_member_paths(unique_member_paths: dict[str, str]) -> dict[str, str]:
	"""
	Return the path of each enum member that only one public class has, by name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	unique_member_paths
		The path of each member name that only one public class has.

	Returns
	-------
	dict[str, str]
		The members written in capital letters, such as ``INT64``.
	"""
	enum_member_paths = {name: path for name, path in unique_member_paths.items() if name.isupper()}

	return enum_member_paths
