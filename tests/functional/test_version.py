"""
Functional tests of the version given by the package.

.. versionadded:: 0.1.0
"""

import tomllib
from pathlib import Path

import numdaplot as ndp

PROJECT_FILE = Path(__file__).parents[2] / "pyproject.toml"


def test_the_version_is_the_one_of_the_project() -> None:
	"""
	Check that ``ndp.__version__`` gives the version written in the project file.

	.. versionadded:: 0.1.0
	"""
	project_text = PROJECT_FILE.read_text()
	project_settings = tomllib.loads(project_text)
	project_version = project_settings["project"]["version"]

	assert ndp.__version__ == project_version


def test_the_version_stays_out_of_the_public_objects() -> None:
	"""
	Check that the version, which is a text and not an object of the API, gets no page of the documentation.

	.. versionadded:: 0.1.0
	"""
	assert "__version__" not in ndp.__all__
