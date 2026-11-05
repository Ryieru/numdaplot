"""
Griffe extension showing the value of the constants used as default values of parameters.

numdaplot names every default value with a constant, such as ``separator: str = DEFAULT_SEPARATOR``.
In the documentation, a reader needs the value itself, so this extension replaces such a default
with the value of the constant, ``","``, once griffe has loaded the whole package. A constant given to a call,
such as ``BinCount(DEFAULT_BIN_COUNT)``, is replaced the same way. The fields of dataclasses are resolved too,
so the ``__init__`` griffe builds from them afterwards shows the values.

.. versionadded:: 0.1.0
"""

import ast
from typing import Any

import griffe


def resolve_default_values(obj: griffe.Object, loader: griffe.GriffeLoader) -> None:
	r"""
	Replace the constants used as default values in an object and its members with their values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	obj
		A module, class or function loaded by griffe.
	loader
		The loader that holds every loaded module.

	Examples
	--------
	>>> import griffe
	>>> from default_values import resolve_default_values
	>>> code = 'LIMIT = 10\ndef cut(limit: int = LIMIT) -> int:\n    return limit'
	>>> with griffe.temporary_visited_package("sales", {"__init__.py": code}) as package:
	...     loader = griffe.GriffeLoader()
	...     loader.modules_collection.set_member(package.path, package)
	...     resolve_default_values(package, loader)
	...     print(package["cut"].parameters["limit"].default)
	10
	"""
	if isinstance(obj, griffe.Function):
		resolve_parameter_defaults(obj, loader)

	if isinstance(obj, griffe.Attribute):
		resolve_attribute_value(obj, loader)

	for member in obj.members.values():
		if isinstance(member, griffe.Alias):
			continue

		resolve_default_values(member, loader)


def resolve_parameter_defaults(function: griffe.Function, loader: griffe.GriffeLoader) -> None:
	"""
	Replace each default value of a function that names a constant with the value of that constant.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		A function or method loaded by griffe.
	loader
		The loader that holds every loaded module.
	"""
	for parameter in function.parameters:
		resolved_default = resolve_expression(parameter.default, loader)
		if resolved_default is not None:
			parameter.default = resolved_default


def resolve_attribute_value(attribute: griffe.Attribute, loader: griffe.GriffeLoader) -> None:
	"""
	Replace the value of an attribute, such as a dataclass field, with the value of the constant it names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	attribute
		An attribute loaded by griffe. Only the fields of classes are resolved.
	loader
		The loader that holds every loaded module.
	"""
	if attribute.parent is None:
		return

	if not attribute.parent.is_class:
		return

	resolved_value = resolve_expression(attribute.value, loader)
	if resolved_value is not None:
		attribute.value = resolved_value


def resolve_expression(expression: str | griffe.Expr | None, loader: griffe.GriffeLoader) -> str | griffe.Expr | None:
	"""
	Return an expression with the constants it names replaced by their values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	expression
		A default value or an attribute value, as griffe reads it.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str, griffe.Expr or None
		The value of the constant named, the call with the values of its constant arguments, or ``None`` when
		the expression holds no constant to replace.
	"""
	if isinstance(expression, griffe.ExprCall):
		resolved_call = resolve_call_arguments(expression, loader)
		return resolved_call

	constant_value = find_constant_value(expression, loader)

	return constant_value


def resolve_call_arguments(call: griffe.ExprCall, loader: griffe.GriffeLoader) -> griffe.ExprCall | None:
	"""
	Return a call with the constants given as arguments replaced by their values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	call
		A call, such as ``BinCount(DEFAULT_BIN_COUNT)``.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	griffe.ExprCall or None
		The new call, such as ``BinCount(10)``, or ``None`` when no argument names a constant.
	"""
	resolved_arguments = list[str | griffe.Expr]()
	has_constant = False

	for argument in call.arguments:
		constant_value = find_constant_value(argument, loader)
		if constant_value is None:
			resolved_arguments.append(argument)
			continue

		resolved_arguments.append(constant_value)
		has_constant = True

	if not has_constant:
		return None

	resolved_call = griffe.ExprCall(call.function, resolved_arguments)

	return resolved_call


def find_constant_value(expression: str | griffe.Expr | None, loader: griffe.GriffeLoader) -> str | None:
	"""
	Return the literal value of the constant an expression names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	expression
		A default value or an attribute value, as griffe reads it.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str or None
		The source of the literal value, such as ``','``, or ``None`` when the expression does not name
		a constant holding a literal value.
	"""
	if not isinstance(expression, griffe.ExprName):
		return None

	constant_path = expression.canonical_path
	try:
		constant = loader.modules_collection.get_member(constant_path)
	except KeyError:
		return None

	if not isinstance(constant, griffe.Attribute):
		return None

	constant_value = constant.value
	if not isinstance(constant_value, str):
		return None

	is_literal = is_python_literal(constant_value)
	if not is_literal:
		return None

	return constant_value


def is_python_literal(source: str) -> bool:
	"""
	Return whether a source text is a Python literal, such as a text, a number or ``None``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source
		The source of a value.

	Returns
	-------
	bool
		True for a literal, False for any other expression, such as a call.

	Examples
	--------
	>>> from default_values import is_python_literal
	>>> is_python_literal("','"), is_python_literal("Shape((2, 3))")
	(True, False)
	"""
	try:
		ast.literal_eval(source)
	except (ValueError, SyntaxError):
		return False

	return True


class DefaultValues(griffe.Extension):
	"""
	Griffe extension replacing the constants used as default values with their values.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler.

	.. versionadded:: 0.1.0
	"""

	def on_package(self, *, pkg: griffe.Module, loader: griffe.GriffeLoader, **kwargs: Any) -> None:
		"""
		Resolve the default values of every function of a loaded package.

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
		resolve_default_values(pkg, loader)
