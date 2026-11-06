"""
Unit tests of the check of the arguments against their annotations.

.. versionadded:: 0.1.0
"""

from typing import Self

import pytest

import numdaplot as ndp
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.settings.argument_types import (
	checked_arguments,
	find_argument_kinds,
	find_owner,
	name_callable,
	replace_self,
	require_argument_type,
)
from numdaplot.settings.field_types import read_accepted_kinds

ANSWER = 42
DOUBLED_ANSWER = 84
EXPECTED_FUNCTION_MESSAGE = "double value expects an int, got 'a'."
EXPECTED_METHOD_MESSAGE = "ProbeOwner.keep other expects a ProbeOwner, got 5."


@checked_arguments
def double(value: int = ANSWER) -> int:
	"""
	Return the double of a number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The number, 42 by default.

	Returns
	-------
	int
		The double.
	"""
	return value * 2


class ProbeOwner:
	"""
	A class with a checked method naming its own class.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def keep(self, other: Self) -> Self:
		"""
		Return the other object.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An object of the same class.

		Returns
		-------
		Self
			The other object.
		"""
		return other


def test_checked_arguments_lets_accepted_arguments_through() -> None:
	"""
	Check that positional and named arguments reach the function.

	.. versionadded:: 0.1.0
	"""
	assert double(ANSWER) == DOUBLED_ANSWER
	assert double(value=ANSWER) == DOUBLED_ANSWER


def test_checked_arguments_leaves_a_default_unchecked() -> None:
	"""
	Check that a call without argument uses the default.

	.. versionadded:: 0.1.0
	"""
	assert double() == DOUBLED_ANSWER


@pytest.mark.parametrize("call_with_text", [lambda: double("a"), lambda: double(value="a")])  # pyright: ignore[reportArgumentType]
def test_checked_arguments_refuses_a_positional_or_named_argument(call_with_text: object) -> None:
	"""
	Check the message for a positional and for a named argument.

	.. versionadded:: 0.1.0

	Parameters
	----------
	call_with_text
		Calls the function with a text.
	"""
	assert callable(call_with_text)

	with pytest.raises(InvalidTypeError) as error_info:
		call_with_text()

	message = str(error_info.value)
	assert message == EXPECTED_FUNCTION_MESSAGE


def test_checked_arguments_replaces_self_by_the_class_of_the_object() -> None:
	"""
	Check that Self names the class the method is called on.

	.. versionadded:: 0.1.0
	"""
	probe = ProbeOwner()

	with pytest.raises(InvalidTypeError) as error_info:
		probe.keep(5)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert probe.keep(probe) is probe
	assert message == EXPECTED_METHOD_MESSAGE


def test_find_owner_finds_the_class_of_a_method() -> None:
	"""
	Check self, cls and a function.

	.. versionadded:: 0.1.0
	"""
	assert find_owner(("self",), (ANSWER,)) is int
	assert find_owner(("cls",), (str,)) is str
	assert find_owner(("value",), (ANSWER,)) is None
	assert find_owner((), ()) is None


def test_find_argument_kinds_reads_the_annotations_once() -> None:
	"""
	Check that a function gets the same result at each call.

	.. versionadded:: 0.1.0
	"""
	first_kinds = find_argument_kinds(double, None)
	second_kinds = find_argument_kinds(double, None)

	assert first_kinds is second_kinds


def test_replace_self_keeps_an_annotation_without_self() -> None:
	"""
	Check that another annotation stays as it is.

	.. versionadded:: 0.1.0
	"""
	assert replace_self(int | None, str) == int | None


def test_require_argument_type_ignores_a_parameter_without_annotation() -> None:
	"""
	Check that a parameter without kinds, such as self, passes.

	.. versionadded:: 0.1.0
	"""
	require_argument_type(double, None, None, ("self", ANSWER))


def test_require_argument_type_refuses_another_type() -> None:
	"""
	Check that a value of another type raises InvalidTypeError.

	.. versionadded:: 0.1.0
	"""
	kinds = read_accepted_kinds(int)

	with pytest.raises(InvalidTypeError):
		require_argument_type(double, None, kinds, ("value", "a"))


@pytest.mark.parametrize(
	("function", "owner", "expected"),
	[
		(double, None, "double"),
		(ndp.Plot.line, ndp.Plot, "Plot.line"),
		(ndp.Table.filter, ndp.Table, "Table.filter"),
		(ndp.Array.__add__, ndp.Array, "Array +"),
		(ndp.Figure.__init__, ndp.Figure, "Figure"),
	],
)
def test_name_callable_writes_the_name_a_user_knows(function: object, owner: type | None, expected: str) -> None:
	"""
	Check a function, a method, an operator and a constructor.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The method or the function.
	owner
		The class, or None.
	expected
		The expected name.
	"""
	assert callable(function)

	callable_name = name_callable(function, owner)

	assert callable_name == expected
