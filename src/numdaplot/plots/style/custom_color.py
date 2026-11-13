"""
A color of a chart written as ``#rrggbb``.

.. versionadded:: 0.1.0
"""

import re
from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.invalid_color_error import InvalidColorError

COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{6}")


@dataclass(frozen=True)
class CustomColor:
	"""
	A color of a chart written as ``#`` followed by its red, green and blue parts in hexadecimal.

	Accepted wherever a ``Color`` is, for the colors the named ones do not cover.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code
		The color, such as ``"#ff8800"`` for orange, in lowercase or uppercase.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColorError
		When the code is not ``#`` followed by six hexadecimal digits.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.CustomColor("#ff8800")])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	code: str

	def __post_init__(self) -> None:
		"""
		Check that the code is ``#`` followed by six hexadecimal digits.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColorError
			When the code is not ``#`` followed by six hexadecimal digits.
		"""
		require_field_types(self)

		code_match = COLOR_PATTERN.fullmatch(self.code)
		if code_match is None:
			raise InvalidColorError(self.code)
