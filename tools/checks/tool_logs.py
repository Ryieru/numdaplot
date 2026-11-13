"""Progress lines printed while the tool commands run, and the full output of each command kept in a log file."""

import sys
import threading
from datetime import datetime
from pathlib import Path

LOG_FOLDER_NAME = "logs"
REPOSITORY_LOG_FOLDER = Path("/tmp/numdaplot-repository", LOG_FOLDER_NAME)
LOG_FILE_NAME = "{action}-{moment}.log"
MOMENT_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_PATTERN = "/tmp/numdaplot-*/" + LOG_FOLDER_NAME + "/{log_name}"
LOG_HEADER = "Full output of each command in " + LOG_PATTERN
START_LINE = "  > {name}: started\n"
END_LINE = "  > {name}: {mark} ({seconds:.0f} s)\n"
LOG_SECTION = "===== {name}\n$ {command}\n{output}\n"
COMMAND_SEPARATOR = " "
PROGRESS_LOCK = threading.Lock()


def build_log_name(action_name: str) -> str:
	"""
	Return the name of the log files of one run of the checks, from the git action and the current moment.

	Parameters
	----------
	action_name
		The git action, ``commit`` or ``push``.

	Returns
	-------
	str
		A name such as ``push-2026-11-13_15-42-10.log``, the same in every log folder of the run.
	"""
	moment = datetime.now()
	moment_text = moment.strftime(MOMENT_FORMAT)
	log_name = LOG_FILE_NAME.format(action=action_name, moment=moment_text)

	return log_name


def write_progress(line: str) -> None:
	"""
	Print a progress line at once, so that the lines of commands running at the same time never mix.

	Parameters
	----------
	line
		The whole line, ending with a line break.
	"""
	with PROGRESS_LOCK:
		sys.stdout.write(line)
		sys.stdout.flush()


def write_start(name: str) -> None:
	"""
	Print that a command starts.

	Parameters
	----------
	name
		The name of the command in the report.
	"""
	start_line = START_LINE.format(name=name)
	write_progress(start_line)


def write_end(name: str, mark: str, seconds: float) -> None:
	"""
	Print that a command ended, with its result and its duration.

	Parameters
	----------
	name
		The name of the command in the report.
	mark
		The mark of the result, as in the report.
	seconds
		The duration of the command.
	"""
	end_line = END_LINE.format(name=name, mark=mark, seconds=seconds)
	write_progress(end_line)


def append_log(log_path: Path, name: str, command: list[str], output: str) -> None:
	"""
	Add the whole output of a command at the end of a log file, created with its folder when missing.

	Parameters
	----------
	log_path
		The log file.
	name
		The name of the command in the report.
	command
		The command that ran.
	output
		Its standard output followed by its error output.
	"""
	log_path.parent.mkdir(parents=True, exist_ok=True)
	command_text = COMMAND_SEPARATOR.join(command)
	section = LOG_SECTION.format(name=name, command=command_text, output=output)

	with log_path.open("a") as log_file:
		log_file.write(section)
