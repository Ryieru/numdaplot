"""Commands of the tools of the project, run in the project folder or in a copy of it, and their results."""

import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from check_report import BLOCKING_MARK, PASSED_MARK, CheckResult, Severity
from tool_logs import REPOSITORY_LOG_FOLDER, append_log, write_end, write_start

UV_COMMAND = ["uv", "run", "--frozen"]
CHECKED_FOLDERS = ["src", "tests", "tools"]
SHOWN_OUTPUT_LINES = 15
LOG_HINT = "full output: {log_path}"
DOCS_ENVIRONMENT = {"NO_MKDOCS_2_WARNING": "1"}
REMOVED_VARIABLES = ("VIRTUAL_ENV",)


@dataclass(frozen=True)
class ToolRun:
	"""
	A command of a tool, and where it runs.

	Parameters
	----------
	name
		The name shown in the report.
	command
		The whole command, such as ``["uv", "run", "--frozen", "pyright"]``.
	folder
		The folder the command runs in.
	log_folder
		The folder of the log file keeping its whole output.
	"""

	name: str
	command: list[str]
	folder: Path
	log_folder: Path


def build_environment() -> dict[str, str]:
	"""
	Return the environment of the tools: the current one, without another virtual environment, for the docs.

	Returns
	-------
	dict[str, str]
		The variables given to each command.
	"""
	environment = dict(os.environ)

	for variable in REMOVED_VARIABLES:
		environment.pop(variable, None)

	environment.update(DOCS_ENVIRONMENT)

	return environment


def run_tool(tool_run: ToolRun, log_name: str) -> CheckResult:
	"""
	Run a command of a tool, print when it starts and ends, keep its output in a log, and return its result.

	Parameters
	----------
	tool_run
		The command, its folder and its log folder.
	log_name
		The name of the log file of this run of the checks.

	Returns
	-------
	CheckResult
		A blocking result, with the last lines of the output and the path of the log as problems when the command fails.
	"""
	write_start(tool_run.name)
	start_seconds = time.monotonic()
	environment = build_environment()
	completed = subprocess.run(
		tool_run.command, cwd=tool_run.folder, env=environment, capture_output=True, text=True, check=False
	)
	end_seconds = time.monotonic()
	output = completed.stdout + completed.stderr
	log_path = tool_run.log_folder / log_name
	append_log(log_path, tool_run.name, tool_run.command, output)

	problems = list[str]()
	mark = PASSED_MARK
	if completed.returncode != 0:
		stripped_output = output.strip()
		output_lines = stripped_output.splitlines()
		problems = output_lines[-SHOWN_OUTPUT_LINES:]
		log_hint = LOG_HINT.format(log_path=log_path)
		problems.append(log_hint)
		mark = BLOCKING_MARK

	duration_seconds = end_seconds - start_seconds
	write_end(tool_run.name, mark, duration_seconds)
	result = CheckResult(tool_run.name, Severity.BLOCKING, problems)

	return result


def list_fast_tool_runs(scope_files: list[Path]) -> list[ToolRun]:
	"""
	Return the commands of the fast checks: ruff on the changed files, pyright on the project.

	Parameters
	----------
	scope_files
		The changed Python files.

	Returns
	-------
	list[ToolRun]
		The ruff commands when files changed, then pyright.
	"""
	here = Path.cwd()
	file_names = [str(path) for path in scope_files]
	tool_runs = list[ToolRun]()
	if file_names:
		lint_command = [*UV_COMMAND, "ruff", "check", *file_names]
		format_command = [*UV_COMMAND, "ruff", "format", "--check", *file_names]
		tool_runs.append(ToolRun("ruff lint", lint_command, here, REPOSITORY_LOG_FOLDER))
		tool_runs.append(ToolRun("ruff format", format_command, here, REPOSITORY_LOG_FOLDER))

	tool_runs.append(ToolRun("pyright", [*UV_COMMAND, "pyright"], here, REPOSITORY_LOG_FOLDER))

	return tool_runs


def list_full_tool_runs() -> list[ToolRun]:
	"""
	Return the commands of the full checks that do not depend on the Python version, before a push.

	Returns
	-------
	list[ToolRun]
		Ruff on every file. The other tools run in each configuration of ``configurations``.
	"""
	here = Path.cwd()
	lint_command = [*UV_COMMAND, "ruff", "check", "."]
	format_command = [*UV_COMMAND, "ruff", "format", "--check", *CHECKED_FOLDERS]
	tool_runs = [
		ToolRun("ruff lint", lint_command, here, REPOSITORY_LOG_FOLDER),
		ToolRun("ruff format", format_command, here, REPOSITORY_LOG_FOLDER),
	]

	return tool_runs
