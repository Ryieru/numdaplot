"""
Warnings about the values of a calculation that become NaN or an infinite value.

.. versionadded:: 0.1.0
"""

import os
import warnings
from pathlib import Path
from types import TracebackType

import numpy

from numdaplot.errors.warnings.calculation_warning import CalculationWarning

CALL_MODE = "call"
IGNORE_MODE = "ignore"
PACKAGE_LEVEL = 2
PACKAGE_DIRECTORY = str(Path(__file__).parents[PACKAGE_LEVEL]) + os.sep
INTERNAL_FILES = (PACKAGE_DIRECTORY,)
# The keys are the names numpy gives to its floating point errors.
FLOAT_ERROR_MESSAGES = {
	"invalid value": "The operation {operation_name} has values without a defined result, such as 0 / 0: "
	"they became NaN.",
	"divide by zero": "The operation {operation_name} divides by zero: these values became inf.",
	"overflow": "The operation {operation_name} has values too large for their type: they became inf.",
}
# A duration too large is refused before it is computed, so a calculation on times only meets these two errors.
TIME_ERROR_MESSAGES = {
	"invalid value": "The operation {operation_name} has values without a defined result, such as 0 / 0: "
	"they became missing.",
	"divide by zero": "The operation {operation_name} divides by zero: these values became missing.",
}


class FloatErrorWarnings:
	"""
	Context giving the numpy floating point errors of a block as ``CalculationWarning``, at the calling code.

	Each kind of error gives one warning when the block ends, and none when the block raises an error.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation_name
		The operator or the function shown in the message, such as ``/`` or ``Sum``.

	Examples
	--------
	>>> import numpy
	>>> import warnings
	>>> from numdaplot.arrays.operations.float_errors import FloatErrorWarnings
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	with FloatErrorWarnings("/"):
	... 		numpy.array([1.0]) / numpy.array([0.0])
	array([inf])
	>>> print(caught_warnings[0].message)
	The operation / divides by zero: these values became inf.
	"""

	messages = FLOAT_ERROR_MESSAGES

	def __init__(self, operation_name: str) -> None:
		"""
		Prepare the numpy settings recording the errors of the block.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation_name
			The operator or the function shown in the message, such as ``/`` or ``Sum``.
		"""
		self.operation_name = operation_name
		self.met_errors = set[str]()
		self.numpy_settings = numpy.errstate(
			divide=CALL_MODE,
			invalid=CALL_MODE,
			over=CALL_MODE,
			under=IGNORE_MODE,
			call=self.record_float_error,
		)

	def record_float_error(self, error_name: str, _error_flag: int) -> None:
		"""
		Remember a floating point error, as numpy reports it during the block.

		.. versionadded:: 0.1.0

		Parameters
		----------
		error_name
			The name numpy gives to the error.
		_error_flag
			The numpy code of the error, not used.
		"""
		self.met_errors.add(error_name)

	def __enter__(self) -> None:
		"""
		Start recording the errors.

		.. versionadded:: 0.1.0
		"""
		self.numpy_settings.__enter__()

	def __exit__(
		self,
		error_type: type[BaseException] | None,
		error: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""
		Stop recording the errors, and warn once per kind of error unless the block raised one.

		.. versionadded:: 0.1.0

		Parameters
		----------
		error_type
			The type of the error raised by the block, or None.
		error
			The error raised by the block, or None.
		traceback
			Its traceback, or None.

		Warns
		-----
		CalculationWarning
			Once per kind of error met in the block.
		"""
		self.numpy_settings.__exit__(error_type, error, traceback)
		if error_type is not None:
			return

		for error_name, message_format in self.messages.items():
			if error_name in self.met_errors:
				message = message_format.format(operation_name=self.operation_name)
				warnings.warn(message, CalculationWarning, skip_file_prefixes=INTERNAL_FILES)


class TimeErrorWarnings(FloatErrorWarnings):
	"""
	Context giving the numpy floating point errors of a calculation on times, whose values become missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation_name
		The operator shown in the message, such as ``/``.

	Examples
	--------
	>>> import numpy
	>>> import warnings
	>>> from numdaplot.arrays.operations.float_errors import TimeErrorWarnings
	>>> durations = numpy.array([1], dtype="timedelta64[ns]")
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	with TimeErrorWarnings("/"):
	... 		durations / numpy.array([0.0])
	array(['NaT'], dtype='timedelta64[ns]')
	>>> print(caught_warnings[0].message)
	The operation / divides by zero: these values became missing.
	"""

	messages = TIME_ERROR_MESSAGES
