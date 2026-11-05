"""
pytest settings shared by every test and every docstring example.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import matplotlib
import pytest

# The examples end with ``plot.show()``: this matplotlib backend opens no window, so the tests never wait.
matplotlib.use("Agg")

PROJECT_FOLDER = Path(__file__).parent
SOURCE_FOLDER = PROJECT_FOLDER / "src"
EXAMPLE_DATA_FOLDER = PROJECT_FOLDER / "tests" / "data"


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
