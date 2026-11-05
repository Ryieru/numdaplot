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
		When ``step`` is zero, or goes away from ``stop``, such as a step of 1 from 5 to 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_range(ndp.Range(start=0, stop=10, step=2))
	Array([ 0,  2,  4,  6,  8, 10], dtype=INT64)
	>>> scores = ndp.Array.from_list([10, 20, 30, 40])
	>>> scores.take(ndp.Region(rows=ndp.Range(start=1, stop=2)))
	Array([20, 30], dtype=INT64)
	"""

	start: int | float
	stop: int | float
	step: int | float = DEFAULT_STEP
	bounds: Bounds = Bounds.INCLUDED

	def __post_init__(self) -> None:
		"""
		Check that the step is not zero and goes from the start to the stop.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidStepError
			When ``step`` is zero, or goes away from ``stop``.
		"""
		if self.step == FORBIDDEN_STEP:
			raise InvalidStepError(self.step)

		distance = self.stop - self.start
		signed_progress = distance * self.step
		goes_away = signed_progress < 0
		if goes_away:
			raise InvalidStepError(self.step, self.start, self.stop)
