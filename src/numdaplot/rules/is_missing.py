"""
Rule keeping the missing values.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.rules.rule import Rule


@dataclass(frozen=True)
class IsMissing(Rule):
	"""
	Keep the missing values, whatever their type: NaN, ``pd.NA`` or ``NaT``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> temperatures = ndp.Array.from_list([12.5, None, 18.0])
	>>> temperatures.check(ndp.IsMissing())
	Array([False,  True, False], dtype=BOOL)
	"""
