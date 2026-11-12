"""
Base class of every rule.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_operation_error import RefusedOperationError

CONSTRUCTOR_OPERATION = "Creating a Rule with ndp.Rule()"
CONSTRUCTOR_ALTERNATIVE = "a rule such as ndp.Greater"


class Rule:
	"""
	Base class of every rule, a test applied to each value of an Array or of Table columns.

	A rule is immutable and checks its settings when it is created.

	Only its subclasses are created: calling ``ndp.Rule()`` raises ``RefusedOperationError``.

	Every rule, passed to ``Array.select``, ``Array.check``, ``Table.check`` and ``Condition``:

	|Rule|What it keeps|Example|
	|---|---|---|
	|``Equal``|The values equal to a reference value|``ndp.Equal("Paris")``|
	|``NotEqual``|The values different from a reference value|``ndp.NotEqual("Paris")``|
	|``Greater``|The values strictly greater than a reference value|``ndp.Greater(10)``|
	|``GreaterOrEqual``|The values greater than or equal to a reference value|``ndp.GreaterOrEqual(10)``|
	|``Less``|The values strictly less than a reference value|``ndp.Less(10)``|
	|``LessOrEqual``|The values less than or equal to a reference value|``ndp.LessOrEqual(10)``|
	|``Between``|The values inside an interval|``ndp.Between(10, 20)``|
	|``IsIn``|The values that belong to a list of accepted values|``ndp.IsIn(["Paris", "Lyon"])``|
	|``Contains``|The texts that contain a given text|``ndp.Contains("Pa")``|
	|``IsMissing``|The missing values|``ndp.IsMissing()``|
	|``IsPresent``|The values that are not missing|``ndp.IsPresent()``|

	.. versionadded:: 0.1.0

	Raises
	------
	RefusedOperationError
		When the created object is a Rule and not one of its subclasses.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([80, 120])
	>>> for rule in [ndp.Greater(100), ndp.Less(100)]:
	... 	print(prices.select(rule))
	Array([120], dtype=INT64)
	Array([80], dtype=INT64)
	"""

	def __init__(self) -> None:
		"""
		Refuse the creation of the base class itself, and let a subclass be created.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			When the created object is a Rule and not one of its subclasses.
		"""
		created_class = type(self)
		if created_class is Rule:
			raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)
