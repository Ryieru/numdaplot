"""
Base class of every math function.

.. versionadded:: 0.1.0
"""


class MathFunction:
	"""
	Base class of every math function, applied to each value of a number Array by ``Array.apply``.

	A math function is immutable and checks its settings when it is created.

	Every math function, passed to ``Array.apply``:

	|Math function|What it gives for each value|Example|
	|---|---|---|
	|``Absolute``|Its distance to 0: -3 and 3 both give 3|``ndp.Absolute()``|
	|``SquareRoot``|Its square root: 9 gives 3|``ndp.SquareRoot()``|
	|``Exponential``|``e`` raised to the value: 0 gives 1|``ndp.Exponential()``|
	|``Logarithm``|Its logarithm: with ``base=10``, 1000 gives 3|``ndp.Logarithm(base=10)``|
	|``Round``|The value rounded to a number of decimals|``ndp.Round(decimals=2)``|
	|``Sine``|Its sine, read as an angle in radians|``ndp.Sine()``|
	|``Cosine``|Its cosine, read as an angle in radians|``ndp.Cosine()``|

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> values = ndp.Array.from_list([1.0, 4.0])
	>>> for function in [ndp.SquareRoot(), ndp.Logarithm(base=2)]:
	... 	print(values.apply(function))
	Array([1., 2.], dtype=FLOAT64)
	Array([0., 2.], dtype=FLOAT64)
	"""
