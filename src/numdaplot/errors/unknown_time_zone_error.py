"""
Error raised when a time zone name is not a known IANA name.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNKNOWN_TIME_ZONE_MESSAGE = "Unknown time zone {name!r}, expected an IANA name such as 'Europe/Paris' or 'UTC'."


class UnknownTimeZoneError(NumdaplotError):
	"""
	Raised when a time zone name is not a known IANA name, such as ``"Paris"`` or ``"+01:00"``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The rejected name.

	Attributes
	----------
	name
		The rejected name.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.TimeZone("Paris")
	... except ndp.UnknownTimeZoneError as error:
	... 	print(error)
	Unknown time zone 'Paris', expected an IANA name such as 'Europe/Paris' or 'UTC'.
	"""

	def __init__(self, name: str) -> None:
		"""
		Build the error message from the rejected name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		name
			The rejected name.
		"""
		message = UNKNOWN_TIME_ZONE_MESSAGE.format(name=name)
		super().__init__(message)
		self.name = name
