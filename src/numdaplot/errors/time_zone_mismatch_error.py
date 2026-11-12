"""
Error raised when datetimes with a time zone meet datetimes without one, or of another time zone.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

TIME_ZONE_MISMATCH_MESSAGE = "{operation} needs datetimes {state} a time zone."
TIME_ZONE_PAIR_MESSAGE = "{operation} needs datetimes in one time zone, got {zone_names}."
ZONE_NAME_SEPARATOR = " and "
WITH_TIME_ZONE = "with"
WITHOUT_TIME_ZONE = "without"


class TimeZoneMismatchError(NumdaplotError):
	"""
	Raised when datetimes with a time zone meet datetimes without one, or datetimes of another time zone.

	For example, a rule compares a datetime column with a time zone to a datetime without one,
	or ``TimeZoneMode.SHIFT`` is asked for datetimes that have no time zone.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		What was attempted, such as ``"Shifting to another time zone"``.
	expects_time_zone
		True when the operation needs datetimes with a time zone, False when it needs datetimes without one.
	zone_names
		The two time zones met, such as ``["Europe/Paris", "UTC"]``. When omitted, one side has no time zone.

	Attributes
	----------
	operation
		What was attempted.
	expects_time_zone
		True when the operation needs datetimes with a time zone, False when it needs datetimes without one.
	zone_names
		The two time zones met, or None.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 1, 2, 10, 30)])})
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.SHIFT, zone=ndp.TimeZone("Europe/Paris"))
	>>> try:
	... 	times.convert(ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=paris))
	... except ndp.TimeZoneMismatchError as error:
	... 	print(error)
	Shifting to another time zone needs datetimes with a time zone.
	"""

	def __init__(self, operation: str, expects_time_zone: bool, zone_names: list[str] | None = None) -> None:
		"""
		Build the error message from the operation and the time zone state it needs, or the two zones met.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			What was attempted.
		expects_time_zone
			True when the operation needs datetimes with a time zone, False when it needs datetimes without one.
		zone_names
			The two time zones met. When omitted, one side has no time zone.
		"""
		state = WITHOUT_TIME_ZONE
		if expects_time_zone:
			state = WITH_TIME_ZONE

		message = TIME_ZONE_MISMATCH_MESSAGE.format(operation=operation, state=state)
		if zone_names is not None:
			joined_names = ZONE_NAME_SEPARATOR.join(zone_names)
			message = TIME_ZONE_PAIR_MESSAGE.format(operation=operation, zone_names=joined_names)

		super().__init__(message)
		self.operation = operation
		self.expects_time_zone = expects_time_zone
		self.zone_names = zone_names
