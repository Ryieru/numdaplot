"""
pytest settings shared by every test and every docstring example.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Any

import matplotlib
import numpy
import pytest
from numpy.typing import NDArray

# The examples end with ``plot.show()``: this matplotlib backend opens no window, so the tests never wait.
matplotlib.use("Agg")

PROJECT_FOLDER = Path(__file__).parent
SOURCE_FOLDER = PROJECT_FOLDER / "src"
EXAMPLE_DATA_FOLDER = PROJECT_FOLDER / "tests" / "data"
TERMINAL_WIDTH_VARIABLE = "COLUMNS"
TERMINAL_WIDTH = "100"
FAR_MICROSECONDS = numpy.array([2**62], dtype="timedelta64[us]")
WRAPPED_NANOSECONDS = numpy.array([-(2**62)], dtype="timedelta64[ns]")


class FarDurations:
	"""
	Fake numpy array of a duration beyond nanoseconds, turned into nanoseconds as one version of numpy does.

	Depending on their version, numpy raises ``OverflowError`` or wraps the value around. The fake gives both
	behaviors in every version, and acts as the real durations for anything else.

	.. versionadded:: 0.1.0
	"""

	def __init__(self, raises_overflow: bool) -> None:
		"""
		Hold a duration of 2**62 microseconds.

		.. versionadded:: 0.1.0

		Parameters
		----------
		raises_overflow
			True to raise ``OverflowError`` when turned into nanoseconds, False to give a wrapped value.
		"""
		self.values = FAR_MICROSECONDS
		self.dtype = FAR_MICROSECONDS.dtype
		self.raises_overflow = raises_overflow

	def __array__(self, dtype: Any = None, copy: Any = None) -> NDArray[Any]:
		"""
		Give the real durations to numpy functions.

		.. versionadded:: 0.1.0

		Parameters
		----------
		dtype
			Ignored.
		copy
			Ignored.

		Returns
		-------
		NDArray
			The real durations.
		"""
		return self.values

	def astype(self, dtype: numpy.dtype[Any]) -> NDArray[Any]:
		"""
		Convert the durations into nanoseconds, imitating one version of numpy.

		.. versionadded:: 0.1.0

		Parameters
		----------
		dtype
			The new type, ignored.

		Returns
		-------
		NDArray
			A wrapped value, as the code under test only converts these durations into nanoseconds.

		Raises
		------
		OverflowError
			For a fake raising.
		"""
		if self.raises_overflow:
			raise OverflowError

		return WRAPPED_NANOSECONDS


@pytest.fixture(autouse=True)
def set_terminal_width(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Give every test the same terminal width, since the text of a wide Table depends on it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Restores the variable after the test.
	"""
	monkeypatch.setenv(TERMINAL_WIDTH_VARIABLE, TERMINAL_WIDTH)


@pytest.fixture(autouse=True)
def run_examples_in_data_folder(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Run the docstring examples of numdaplot from the folder of the example files.

	The examples read the example files by their name alone, as a user reads a file of the current folder.

	.. versionadded:: 0.1.0

	Parameters
	----------
	request
		The running test.
	monkeypatch
		Restores the current folder after the test.
	"""
	test_path = request.path
	is_source_example = test_path.is_relative_to(SOURCE_FOLDER)
	if is_source_example:
		monkeypatch.chdir(EXAMPLE_DATA_FOLDER)


@pytest.fixture
def overflowing_durations() -> Any:
	"""
	Return durations beyond nanoseconds whose conversion raises ``OverflowError``, as some versions of numpy do.

	.. versionadded:: 0.1.0

	Returns
	-------
	Any
		A fake numpy array, typed Any to be given where a numpy array is expected.
	"""
	durations = FarDurations(True)

	return durations


@pytest.fixture
def wrapping_durations() -> Any:
	"""
	Return durations beyond nanoseconds whose conversion wraps around, as other versions of numpy do.

	.. versionadded:: 0.1.0

	Returns
	-------
	Any
		A fake numpy array, typed Any to be given where a numpy array is expected.
	"""
	durations = FarDurations(False)

	return durations
