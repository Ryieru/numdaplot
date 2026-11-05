"""
Width and height of a Plot in inches, as matplotlib counts sizes.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.style.size import Size
from numdaplot.plots.style.size_unit import SizeUnit

UNITS_PER_INCH = {
	SizeUnit.INCH: 1.0,
	SizeUnit.CENTIMETER: 2.54,
	SizeUnit.PIXEL: 100.0,
}


def convert_size_to_inches(size: Size) -> tuple[float, float]:
	"""
	Return the width and the height of a size in inches, as matplotlib counts sizes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	size
		The size, in any ``SizeUnit``.

	Returns
	-------
	tuple[float, float]
		The width and the height, a pixel counting for a hundredth of an inch.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.size_inches import convert_size_to_inches
	>>> convert_size_to_inches(ndp.Size(width=600, height=300, unit=ndp.SizeUnit.PIXEL))
	(6.0, 3.0)
	"""
	units_per_inch = UNITS_PER_INCH[size.unit]
	width_inches = size.width / units_per_inch
	height_inches = size.height / units_per_inch
	inches = (width_inches, height_inches)

	return inches
