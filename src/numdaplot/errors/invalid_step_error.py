"""
Error raised when the step of a range is zero.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_STEP_MESSAGE = "Expected a non-zero step, got {step}."


class InvalidStepError(NumdaplotError):
	"""
	Raised when a range is given a step of zero, which would never reach its end.

	.. versionadded:: 0.1.0

	Parameters
	----------
	step
		The rejected step.

	Attributes
	----------
	step
		The rejected step.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Range(start=0, stop=10, step=0)
	Traceback (most recent call last):
	...
	numdaplot.errors.invalid_step_error.InvalidStepError: Expected a non-zero step, got 0.
	"""

	def __init__(self, step: float) -> None:
		"""
		Build the error message from the rejected step.

		.. versionadded:: 0.1.0

		Parameters
		----------
		step
			The rejected step.
		"""
		message = INVALID_STEP_MESSAGE.format(step=step)
		super().__init__(message)
		self.step = step
