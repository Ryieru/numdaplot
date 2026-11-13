"""The Python versions and dependency resolutions of the CI jobs, each checked in its own copy of the project."""

import shutil
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import repeat
from pathlib import Path

from check_report import CheckResult, Severity
from tool_checks import UV_COMMAND, ToolRun, run_tool
from tool_logs import LOG_FOLDER_NAME

COPIED_FOLDERS = ["src", "tests", "docs", "tools"]
COPIED_FILES = ["mkdocs.yml", "pyproject.toml", "README.md", "LICENSE", "run_tests.py", "conftest.py", "CHANGELOG.md"]
IGNORED_COPY_FILES = ("__pycache__",)
CHECK_NAME = "{step}, {configuration}"
COPY_STEP = "copy of the project"
COPY_PROBLEM = "cannot copy the project into {folder}: {error}"
CHECK_STEPS = (
	("pyright", ["pyright"]),
	("tests with coverage", ["coverage", "run", "run_tests.py", "-q"]),
	("coverage threshold", ["coverage", "report"]),
	("docs build in strict mode", ["mkdocs", "build", "--strict"]),
)


@dataclass(frozen=True)
class Configuration:
	"""
	A Python version and a resolution of the dependencies, as one CI job uses them.

	Parameters
	----------
	name
		The name of the CI job, such as ``Python 3.14 - latest dependencies``.
	folder
		The copy of the project holding the environment of the configuration.
	python_version
		The Python version given to ``uv sync``.
	resolution
		The resolution given to ``uv lock``: ``highest`` or ``lowest-direct``.
	"""

	name: str
	folder: Path
	python_version: str
	resolution: str


LATEST_313 = Configuration("Python 3.13 - latest dependencies", Path("/tmp/numdaplot-py313-latest"), "3.13", "highest")
MINIMUM_313 = Configuration(
	"Python 3.13 - minimum dependencies", Path("/tmp/numdaplot-py313-minimum"), "3.13", "lowest-direct"
)
LATEST_314 = Configuration("Python 3.14 - latest dependencies", Path("/tmp/numdaplot-py314-latest"), "3.14", "highest")
CONFIGURATIONS = (LATEST_313, MINIMUM_313, LATEST_314)
SITE_CONFIGURATION = LATEST_313


def copy_project(folder: Path) -> None:
	"""
	Copy the current code of the project into a folder, created when missing, keeping its environment and lock.

	Parameters
	----------
	folder
		The copy of the project.

	Raises
	------
	OSError
		When a file cannot be copied.
	"""
	folder.mkdir(parents=True, exist_ok=True)
	ignored_files = shutil.ignore_patterns(*IGNORED_COPY_FILES)

	for copied_folder in COPIED_FOLDERS:
		target_folder = folder / copied_folder
		shutil.rmtree(target_folder, ignore_errors=True)
		shutil.copytree(copied_folder, target_folder, ignore=ignored_files)

	for file_name in COPIED_FILES:
		shutil.copy2(file_name, folder / file_name)


def list_preparation_runs(configuration: Configuration) -> list[ToolRun]:
	"""
	Return the commands resolving the dependencies of a configuration again and installing them, as the CI does.

	Parameters
	----------
	configuration
		The configuration to prepare.

	Returns
	-------
	list[ToolRun]
		``uv lock --upgrade`` with the resolution of the configuration, then ``uv sync`` with its Python version.
	"""
	lock_name = CHECK_NAME.format(step="dependency resolution", configuration=configuration.name)
	lock_arguments = ["uv", "lock", "--resolution", configuration.resolution, "--upgrade", "--quiet"]
	sync_name = CHECK_NAME.format(step="installation", configuration=configuration.name)
	sync_arguments = ["uv", "sync", "--frozen", "--all-extras", "--python", configuration.python_version, "--quiet"]
	log_folder = configuration.folder / LOG_FOLDER_NAME
	preparation_runs = [
		ToolRun(lock_name, lock_arguments, configuration.folder, log_folder),
		ToolRun(sync_name, sync_arguments, configuration.folder, log_folder),
	]

	return preparation_runs


def list_check_runs(configuration: Configuration) -> list[ToolRun]:
	"""
	Return the commands of the CI steps that depend on the configuration.

	Parameters
	----------
	configuration
		The configuration to check.

	Returns
	-------
	list[ToolRun]
		Pyright, the tests with their coverage, the coverage threshold and the strict build of the docs.
	"""
	check_runs = list[ToolRun]()
	log_folder = configuration.folder / LOG_FOLDER_NAME

	for step, arguments in CHECK_STEPS:
		check_name = CHECK_NAME.format(step=step, configuration=configuration.name)
		check_run = ToolRun(check_name, [*UV_COMMAND, *arguments], configuration.folder, log_folder)
		check_runs.append(check_run)

	return check_runs


def check_configuration(configuration: Configuration, log_name: str) -> list[CheckResult]:
	"""
	Copy the project for a configuration, prepare its environment, then run its checks.

	Parameters
	----------
	configuration
		The configuration to check.
	log_name
		The name of the log file of this run of the checks, in the copy of the configuration.

	Returns
	-------
	list[CheckResult]
		One result per command, stopping after the first failing step of the copy or of the preparation.
	"""
	try:
		copy_project(configuration.folder)
	except OSError as error:
		copy_name = CHECK_NAME.format(step=COPY_STEP, configuration=configuration.name)
		copy_problem = COPY_PROBLEM.format(folder=configuration.folder, error=error)
		copy_result = CheckResult(copy_name, Severity.BLOCKING, [copy_problem])
		return [copy_result]

	results = list[CheckResult]()

	preparation_runs = list_preparation_runs(configuration)
	for preparation_run in preparation_runs:
		preparation_result = run_tool(preparation_run, log_name)
		results.append(preparation_result)
		if preparation_result.problems:
			return results

	check_runs = list_check_runs(configuration)
	check_results = [run_tool(check_run, log_name) for check_run in check_runs]
	results.extend(check_results)

	return results


def check_configurations(log_name: str) -> list[CheckResult]:
	"""
	Check every configuration at the same time, and return their results in the order of the configurations.

	Parameters
	----------
	log_name
		The name of the log file of this run of the checks, in the copy of each configuration.

	Returns
	-------
	list[CheckResult]
		The results of each configuration, one configuration after the other.
	"""
	configuration_count = len(CONFIGURATIONS)
	log_names = repeat(log_name)
	results = list[CheckResult]()

	with ThreadPoolExecutor(max_workers=configuration_count) as executor:
		configuration_results = executor.map(check_configuration, CONFIGURATIONS, log_names)
		for one_configuration_results in configuration_results:
			results.extend(one_configuration_results)

	return results
