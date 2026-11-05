"""
Functional tests of the arguments of the public methods and functions, as a user without a type checker writes them.

A new public method or function without the check makes this test fail.

.. versionadded:: 0.1.0
"""

# The tests write on purpose what the type checker refuses, as a user without a type checker would.
# pyright: reportArgumentType=false, reportOperatorIssue=false, reportCallIssue=false, reportUnknownLambdaType=false

import inspect
from collections.abc import Callable
from pathlib import Path

import pytest

import numdaplot as ndp

PRICES = ndp.Array.from_list([12.0, 15.5])
SALES = ndp.Table.from_arrays({"price": PRICES})
GRID = ndp.Array.from_list([[1, 2], [3, 4]])
ROW = ndp.Array.from_list([10, 20])
CHECKED_CLASSES = (ndp.Array, ndp.Table, ndp.Plot, ndp.Figure)
UNCHECKED_PARAMETERS = {"self", "cls"}
OPERATOR_NAMES = ("__add__", "__radd__", "__sub__", "__rsub__", "__mul__", "__rmul__", "__truediv__", "__rtruediv__")
MORE_OPERATOR_NAMES = ("__floordiv__", "__rfloordiv__", "__mod__", "__rmod__", "__pow__", "__rpow__")
LOGIC_OPERATOR_NAMES = ("__and__", "__rand__", "__or__", "__ror__")
MESSAGE_CASES = [
	(lambda: SALES.filter(10), "Table.filter row_filter expects a Filter, got 10."),
	(lambda: PRICES.sort(5), "Array.sort sorting expects an ArraySorting or None, got 5."),
	(lambda: PRICES.compute(ndp.Sum(), axis="x"), "Array.compute axis expects an Axis or None, got 'x'."),
	(lambda: SALES.column(5), "Table.column column_name expects a str, got 5."),
	(lambda: SALES.to_csv(5), "Table.to_csv path expects a str or a Path, got 5."),
	(lambda: ndp.Figure(5), "Figure layout expects a Layout, got 5."),
	(lambda: ndp.Array.from_list((1, 2)), "Array.from_list values expects a list, got (1, 2)."),
	(lambda: ndp.plot_missing_map(PRICES), None),
	(lambda: PRICES.select(ndp.Sum), "ndp.Sum is a class, use ndp.Sum() instead."),
	(lambda: PRICES.is_equal(ndp.Equality(other=SALES)), None),
	(lambda: PRICES + [1, 2], None),
	(lambda: [1, 2] + PRICES, None),
]


def list_public_callables() -> list[tuple[str, Callable[..., object]]]:
	"""
	Return the methods and functions of the public API that take arguments.

	.. versionadded:: 0.1.0

	Returns
	-------
	list[tuple[str, Callable[..., object]]]
		The name and the function of each one, the refusing operators left out.
	"""
	found = list[tuple[str, Callable[..., object]]]()

	for name in ndp.__all__:
		exported = getattr(ndp, name)
		if inspect.isfunction(exported):
			found.append((name, exported))

	operator_names = (*OPERATOR_NAMES, *MORE_OPERATOR_NAMES, *LOGIC_OPERATOR_NAMES)

	for checked_class in CHECKED_CLASSES:
		member_names = [name for name in dir(checked_class) if not name.startswith("_")]
		method_names = [*member_names, *operator_names]

		for method_name in method_names:
			member = inspect.getattr_static(checked_class, method_name, None)
			method = getattr(member, "__func__", member)
			if inspect.isfunction(method):
				found.append((f"{checked_class.__name__}.{method_name}", method))

	return found


def takes_arguments(function: Callable[..., object]) -> bool:
	"""
	Return whether a method or a function takes arguments, ``self`` and ``cls`` left out.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The method or the function.

	Returns
	-------
	bool
		True when it takes at least one argument.
	"""
	parameter_names = set(inspect.signature(function).parameters)
	argument_names = parameter_names - UNCHECKED_PARAMETERS

	return bool(argument_names)


PUBLIC_CALLABLES = [(name, function) for name, function in list_public_callables() if takes_arguments(function)]
CALLABLE_IDS = [name for name, _ in PUBLIC_CALLABLES]


@pytest.mark.parametrize(("name", "function"), PUBLIC_CALLABLES, ids=CALLABLE_IDS)
def test_every_public_callable_checks_its_arguments(name: str, function: Callable[..., object]) -> None:
	"""
	Check that a public method or function taking arguments has the check.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name shown when the check is missing.
	function
		The method or the function.
	"""
	assert hasattr(function, "__wrapped__"), name


def test_figure_constructor_checks_its_arguments() -> None:
	"""
	Check the constructor of Figure, the only public class built by a constructor with a check of its own.

	.. versionadded:: 0.1.0
	"""
	assert hasattr(ndp.Figure.__init__, "__wrapped__")


@pytest.mark.parametrize(("call", "expected_message"), MESSAGE_CASES)
def test_an_argument_of_the_wrong_type_is_refused(call: Callable[[], object], expected_message: str | None) -> None:
	"""
	Check that a wrong argument raises InvalidTypeError, with its message when it is short.

	.. versionadded:: 0.1.0

	Parameters
	----------
	call
		Calls a method or a function with a wrong argument.
	expected_message
		The expected message, or None when the message shows a whole object.
	"""
	with pytest.raises(ndp.InvalidTypeError) as error_info:
		call()

	message = str(error_info.value)
	if expected_message is not None:
		assert message == expected_message


def test_a_broadcast_warning_points_at_the_line_of_the_user() -> None:
	"""
	Check that the check of the arguments leaves the warning on the line of the user.

	.. versionadded:: 0.1.0
	"""
	with pytest.warns(ndp.BroadcastWarning) as caught_warnings:
		_ = GRID + ROW

	warning_file = Path(caught_warnings[0].filename)
	assert warning_file.name == Path(__file__).name
