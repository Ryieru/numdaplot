"""
Error raised when a time zone change has a zone it does not use, or misses the zone it needs.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

MISSING_ZONE_MESSAGE = "TimeZoneMode.{mode_name} needs a zone."
EXTRA_ZONE_MESSAGE = "TimeZoneMode.{mode_name} takes no zone."


class InvalidTimeZoneChangeError(NumdaplotError):
	"""
	Raised when ``TimeZoneMode.ATTRIBUTE`` or ``SHIFT`` has no zone, or ``TimeZoneMode.REMOVE`` has one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mode_name
		Name of the ``TimeZoneMode`` member of the change.
	needs_zone
		True when the mode needs a zone that is missing, False when it has a zone it does not use.

	Attributes
	----------
	mode_name
		Name of the ``TimeZoneMode`` member of the change.
	needs_zone
		True when the mode needs a zone that is missing, False when it has a zone it does not use.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.TimeZoneChange(mode=ndp.TimeZoneMode.SHIFT)
	... except ndp.InvalidTimeZoneChangeError as error:
	... 	print(error)
	TimeZoneMode.SHIFT needs a zone.
	"""

	def __init__(self, mode_name: str, needs_zone: bool) -> None:
		"""
		Build the error message from the mode and whether its zone is missing or extra.

		.. versionadded:: 0.1.0

		Parameters
		----------
		mode_name
			Name of the ``TimeZoneMode`` member of the change.
		needs_zone
			True when the mode needs a zone that is missing, False when it has a zone it does not use.
		"""
		message_template = EXTRA_ZONE_MESSAGE
		if needs_zone:
			message_template = MISSING_ZONE_MESSAGE

		message = message_template.format(mode_name=mode_name)
		super().__init__(message)
		self.mode_name = mode_name
		self.needs_zone = needs_zone
