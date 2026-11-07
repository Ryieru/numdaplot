"""
Chart drawing each row as a point.

.. versionadded:: 0.1.0
"""

import math
from dataclasses import dataclass

from numdaplot.errors.conflicting_settings_error import ConflictingSettingsError
from numdaplot.errors.invalid_opacity_error import InvalidOpacityError
from numdaplot.errors.invalid_point_size_error import InvalidPointSizeError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.color_scale import ColorScale
from numdaplot.plots.charts.marker_shape import MarkerShape
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_optional_column_name

CHART_NAME = "ScatterChart"
COLOR_SETTING = "color"
COLOR_BY_SETTING = "color_by"
NO_MARKER_NAME = "MarkerShape.NONE"
POINT_SIZE_SETTING = "point_size"
SIZE_BY_SETTING = "size_by"
SCALE_WITHOUT_COLOR_BY = "scale without color_by"


@dataclass(frozen=True)
class ScatterChart(Chart):
	"""
	Chart drawing each row as a point, used by ``Plot.scatter``.

	A row with a missing value in one of the columns used is not drawn. In a dense cloud, a low ``opacity`` shows where
	the points gather, and a small ``point_size`` separates them. The last group drawn stays on top of the others.

	.. versionadded:: 0.1.0

	Parameters
	----------
	x
		For a Table, the column of the horizontal positions: numbers, dates, datetimes, times of day, texts or
		booleans, the row numbers when omitted. An Array takes none, its rows being numbered. Times of day are placed
		on an axis of one day labeled ``HH:MM``.
	y
		For a Table, the column of the vertical positions, holding numbers. A Table needs it. An Array takes none: when
		omitted, each of its columns is a series of points.
	color
		The color of every point, the first color of the default cycle when omitted. With an Array of
		several columns, the series take the colors of the default cycle and ``color`` is refused.
	color_by
		For a Table, the column coloring each point: numbers give a color scale shown next to the axes, texts, booleans
		and times of day give one color per value, named in the legend, times being written ``HH:MM``. Every point
		takes the same color when omitted.
	size_by
		For a Table, the column of numbers sizing each point, from the smallest to the largest value. Every point has
		the same size when omitted.
	marker
		The shape of the points, ``MarkerShape.CIRCLE`` by default.
	opacity
		How opaque the points are, above 0 and up to 1, ``1.0`` by default. The legend and the color scale stay opaque.
	point_size
		The diameter of every point, in typographic points, 6 when omitted.
	scale
		The colors of a ``color_by`` column of numbers, ``ColorScale.VIRIDIS`` when omitted. It needs such a column.
		``BLUES``, ``REDS``, ``GREENS`` and ``GRAYS`` skip their lightest colors, so that every point stays visible.
		``RED_BLUE`` keeps white for 0, so the points close to 0 stay pale.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``x``, ``y``, ``color_by`` or ``size_by`` is an empty text.
	ConflictingSettingsError
		When ``color`` and ``color_by`` are both given, or ``point_size`` and ``size_by``.
	RefusedSettingError
		When ``marker`` is ``MarkerShape.NONE``, which would draw nothing, or ``scale`` is given without ``color_by``.
	InvalidOpacityError
		When ``opacity`` is 0 or lower, greater than 1, or not a number.
	InvalidPointSizeError
		When ``point_size`` is 0 or lower, infinite, or not a number.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0, 52.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0, 190.0])
	>>> cities = ndp.Array.from_list(["Paris", "Paris", "Lyon", "Lyon", "Pau"])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices, "city": cities})
	>>> chart = ndp.ScatterChart(x="surface", y="price", color_by="city", size_by="surface")
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""

	x: str | None = None
	y: str | None = None
	color: Color | CustomColor | None = None
	color_by: str | None = None
	size_by: str | None = None
	marker: MarkerShape = MarkerShape.CIRCLE
	opacity: float = 1.0
	point_size: float | None = None
	scale: ColorScale | None = None

	def __post_init__(self) -> None:
		"""
		Check that the color and the size settings exclude each other, and that the points can be drawn.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``x``, ``y``, ``color_by`` or ``size_by`` is an empty text.
		ConflictingSettingsError
			When ``color`` and ``color_by`` are both given, or ``point_size`` and ``size_by``.
		RefusedSettingError
			When ``marker`` is ``MarkerShape.NONE``, or ``scale`` is given without ``color_by``.
		InvalidOpacityError
			When ``opacity`` is 0 or lower, greater than 1, or not a number.
		InvalidPointSizeError
			When ``point_size`` is 0 or lower, infinite, or not a number.
		"""
		require_field_types(self)

		require_optional_column_name(self.x)
		require_optional_column_name(self.y)
		require_optional_column_name(self.color_by)
		require_optional_column_name(self.size_by)

		has_both_colors = self.color is not None and self.color_by is not None
		if has_both_colors:
			raise ConflictingSettingsError(COLOR_SETTING, COLOR_BY_SETTING)

		if self.marker == MarkerShape.NONE:
			raise RefusedSettingError(NO_MARKER_NAME, CHART_NAME)

		has_scale_alone = self.scale is not None and self.color_by is None
		if has_scale_alone:
			raise RefusedSettingError(SCALE_WITHOUT_COLOR_BY, CHART_NAME)

		has_both_sizes = self.point_size is not None and self.size_by is not None
		if has_both_sizes:
			raise ConflictingSettingsError(POINT_SIZE_SETTING, SIZE_BY_SETTING)

		is_drawable_opacity = 0 < self.opacity <= 1
		if not is_drawable_opacity:
			raise InvalidOpacityError(self.opacity)

		if self.point_size is not None:
			is_drawable_size = 0 < self.point_size < math.inf
			if not is_drawable_size:
				raise InvalidPointSizeError(self.point_size)
