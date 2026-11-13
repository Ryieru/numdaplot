"""
Error raised when the step of a range is zero, or goes away from its stop.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_STEP_MESSAGE = "Expected a non-zero step, got {step}."
WRONG_DIRECTION_MESSAGE = "Expected a step going from start to stop, got step {step} from {start} to {stop}."


class InvalidStepError(NumdaplotError):
	"""
	Raised when a range is given a step of zero, or a step going away from its stop, which never reach the stop.

	.. versionadded:: 0.1.0

	Parameters
	----------
	step
		The rejected step.
	start
		The start of the range when the step goes away from the stop. When omitted, the message is about a step of zero.
	stop
		The stop of the range when the step goes away from it. When omitted, the message is about a step of zero.

	Attributes
	----------
	step
		The rejected step.
	start
		The start of the range, or None for a step of zero.
	stop
		The stop of the range, or None for a step of zero.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Range(start=0, stop=10, step=0)
	... except ndp.InvalidStepError as error:
	... 	print(error)
	Expected a non-zero step, got 0.
	>>> try:
	... 	ndp.Range(start=5, stop=1)
	... except ndp.InvalidStepError as error:
	... 	print(error)
	Expected a step going from start to stop, got step 1 from 5 to 1.
	"""

	def __init__(self, step: float, start: float | None = None, stop: float | None = None) -> None:
		"""
		Build the error message from the rejected step, and the start and the stop when the step goes away.

		.. versionadded:: 0.1.0

		Parameters
		----------
		step
			The rejected step.
		start
			The start of the range when the step goes away from the stop. When omitted, the message is about a step of
			zero.
		stop
			The stop of the range when the step goes away from it. When omitted, the message is about a step of zero.
		"""
		if start is None or stop is None:
			message = INVALID_STEP_MESSAGE.format(step=step)
		else:
			message = WRONG_DIRECTION_MESSAGE.format(step=step, start=start, stop=stop)

		super().__init__(message)

		self.step = step
		self.start = start
		self.stop = stop
