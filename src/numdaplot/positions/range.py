"""
A regular sequence of numbers between two bounds.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_step_error import InvalidStepError
from numdaplot.rules.bounds import Bounds

DEFAULT_STEP = 1
FORBIDDEN_STEP = 0


@dataclass(frozen=True)
class Range:
	"""
	A regular sequence of numbers from ``start`` to ``stop``, every ``step``.

	It selects positions in ``Region`` and creates values in ``Array.from_range``.
	Unlike the Python ``range``, the end is included by default, as in ``Between``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	start
		First number of the sequence.
	stop
		Last number of the sequence, reached only when it falls on a step.
	step
		Gap between two numbers, 1 by default. A negative step goes downwards.
	bounds
		Which of ``start`` and ``stop`` are part of the sequence. Both are included by default.

	Raises
	------
	InvalidStepError
		When ``step`` is zero.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Range(start=0, stop=10, step=2)
	Range(start=0, stop=10, step=2, bounds=<Bounds.INCLUDED: 1>)
	"""

	start: int | float
	stop: int | float
	step: int | float = DEFAULT_STEP
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check that the step is not zero.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidStepError
			When ``step`` is zero.
		"""
		if self.step == FORBIDDEN_STEP:
			raise InvalidStepError(self.step)
