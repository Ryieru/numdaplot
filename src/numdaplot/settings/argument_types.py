"""
Check of the arguments of the public methods and functions against their annotations.

.. versionadded:: 0.1.0
"""

# typing.Self is a special form the type checker only knows inside annotations.
# pyright: reportUnknownMemberType=false

import functools
import inspect
import typing
from collections.abc import Callable
from typing import cast

from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.settings.annotation_kinds import AcceptedKinds, read_accepted_kinds, read_annotations
from numdaplot.settings.field_types import accepts_value, find_rejected_value
from numdaplot.settings.kind_descriptions import describe_kinds

INSTANCE_PARAMETER = "self"
CLASS_PARAMETER = "cls"
CONSTRUCTOR_NAME = "__init__"
TARGET_FORMAT = "{callable_name} {parameter_name}"
METHOD_NAME_FORMAT = "{owner_name}.{method_name}"
OPERATOR_NAME_FORMAT = "{owner_name} {symbol}"
OPERATOR_SYMBOLS = {
	"__add__": "+",
	"__radd__": "+",
	"__sub__": "-",
	"__rsub__": "-",
	"__mul__": "*",
	"__rmul__": "*",
	"__truediv__": "/",
	"__rtruediv__": "/",
	"__floordiv__": "//",
	"__rfloordiv__": "//",
	"__mod__": "%",
	"__rmod__": "%",
	"__pow__": "**",
	"__rpow__": "**",
	"__and__": "&",
	"__rand__": "&",
	"__or__": "|",
	"__ror__": "|",
}


def checked_arguments[**Parameters, Result](function: Callable[Parameters, Result]) -> Callable[Parameters, Result]:
	"""
	Make a method or a function check its arguments against its annotations at each call.

	The annotations are read once, at the first call. An argument left to its default is not checked.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The method or the function.

	Returns
	-------
	Callable
		The same function, with the same signature, refusing an argument of the wrong type.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([1, 2]).sort(5)
	... except ndp.InvalidTypeError as error:
	... 	print(error)
	Array.sort sorting expects an ArraySorting or None, got 5.
	"""
	parameter_names = tuple(inspect.signature(function).parameters)

	@functools.wraps(function)
	def call_after_check(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
		"""
		Check the given arguments, then call the function.

		.. versionadded:: 0.1.0

		Parameters
		----------
		args
			The positional arguments.
		kwargs
			The named arguments.

		Returns
		-------
		Result
			What the function returns.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		"""
		owner = find_owner(parameter_names, args)
		argument_kinds = find_argument_kinds(function, owner)
		named_arguments = zip(parameter_names, args, strict=False)

		for parameter_name, value in named_arguments:
			require_argument_type(function, owner, argument_kinds.get(parameter_name), (parameter_name, value))

		for parameter_name, value in kwargs.items():
			require_argument_type(function, owner, argument_kinds.get(parameter_name), (parameter_name, value))

		return function(*args, **kwargs)

	return call_after_check


def find_owner(parameter_names: tuple[str, ...], args: tuple[object, ...]) -> type | None:
	"""
	Return the class a method is called on, or None for a function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	parameter_names
		The names of the parameters of the method or the function.
	args
		The positional arguments of the call.

	Returns
	-------
	type or None
		The class of ``self``, the ``cls`` itself, or None.

	Examples
	--------
	>>> from numdaplot.settings.argument_types import find_owner
	>>> find_owner(("self", "other"), (1, 2))
	<class 'int'>
	>>> find_owner(("data",), (1,)) is None
	True
	"""
	if not parameter_names:
		return None

	first_name = parameter_names[0]
	if first_name == INSTANCE_PARAMETER:
		return type(args[0])

	if first_name == CLASS_PARAMETER:
		return cast(type, args[0])

	return None


@functools.cache
def find_argument_kinds(function: Callable[..., object], owner: type | None) -> dict[str, AcceptedKinds]:
	"""
	Return what each parameter of a method or a function accepts, read once for each class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The method or the function.
	owner
		The class it is called on, which ``Self`` names in its annotations, or None for a function.

	Returns
	-------
	dict[str, AcceptedKinds]
		What each annotated parameter accepts.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.argument_types import find_argument_kinds
	>>> find_argument_kinds(ndp.Plot.missing_map, None)["table"].names
	('Table',)
	"""
	annotations = read_annotations(function)
	annotations.pop("return", None)
	argument_kinds = dict[str, AcceptedKinds]()

	for parameter_name, annotation in annotations.items():
		owned_annotation = replace_self(annotation, owner)
		argument_kinds[parameter_name] = read_accepted_kinds(owned_annotation)

	return argument_kinds


def replace_self(annotation: object, owner: type | None) -> object:
	"""
	Return an annotation with ``Self`` replaced by the class a method is called on.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotation
		The annotation.
	owner
		The class, or None for a function.

	Returns
	-------
	object
		The annotation naming the class.

	Examples
	--------
	>>> from typing import Self
	>>> from numdaplot.settings.argument_types import replace_self
	>>> replace_self(Self | None, int) == int | None
	True
	"""
	if annotation is typing.Self:
		return owner

	members = typing.get_args(annotation)
	has_self = typing.Self in members
	if not has_self:
		return annotation

	owned_members = tuple(owner if member is typing.Self else member for member in members)
	owned_union = cast(object, typing.Union[owned_members])  # noqa: UP007

	return owned_union


def require_argument_type(
	function: Callable[..., object],
	owner: type | None,
	kinds: AcceptedKinds | None,
	argument: tuple[str, object],
) -> None:
	"""
	Check one argument of a call.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The method or the function called.
	owner
		The class it is called on, or None.
	kinds
		What the parameter accepts, or None when it has no annotation, such as ``self``.
	argument
		The name of the parameter and the given value.

	Raises
	------
	InvalidTypeError
		When the value is not of an accepted kind.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.argument_types import require_argument_type
	>>> from numdaplot.settings.annotation_kinds import read_accepted_kinds
	>>> try:
	... 	require_argument_type(ndp.Plot.line, ndp.Plot, read_accepted_kinds(str), ("chart", 5))
	... except ndp.InvalidTypeError as error:
	... 	print(error)
	Plot.line chart expects a str, got 5.
	"""
	if kinds is None:
		return

	parameter_name, value = argument
	is_accepted = accepts_value(kinds, value)
	if is_accepted:
		return

	callable_name = name_callable(function, owner)
	target_name = TARGET_FORMAT.format(callable_name=callable_name, parameter_name=parameter_name)
	expected = describe_kinds(kinds, value)
	rejected_value = find_rejected_value(kinds, value)
	raise InvalidTypeError(target_name, expected, rejected_value)


def name_callable(function: Callable[..., object], owner: type | None) -> str:
	"""
	Return the name of a method or a function, as the user writes it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The method or the function.
	owner
		The class it is called on, or None.

	Returns
	-------
	str
		``Plot.line``, ``Table.filter``, ``Array +``, or ``Figure`` for a constructor.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.argument_types import name_callable
	>>> name_callable(ndp.Array.__add__, ndp.Array)
	'Array +'
	"""
	function_name = function.__name__
	if owner is None:
		return function_name

	owner_name = owner.__name__
	if function_name == CONSTRUCTOR_NAME:
		return owner_name

	symbol = OPERATOR_SYMBOLS.get(function_name)
	if symbol is not None:
		return OPERATOR_NAME_FORMAT.format(owner_name=owner_name, symbol=symbol)

	return METHOD_NAME_FORMAT.format(owner_name=owner_name, method_name=function_name)
