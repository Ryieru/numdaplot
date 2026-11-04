"""
A drawn view of a Table or an Array.

.. versionadded:: 0.1.0
"""

from pathlib import Path

from matplotlib.figure import Figure

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.drawing.plot_drawing import build_figure
from numdaplot.plots.output.image_saving import choose_resolution, find_image_format, save_figure
from numdaplot.plots.output.plot_display import show_plot
from numdaplot.plots.style.image_options import ImageOptions
from numdaplot.plots.style.style import Style
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.files.file_paths import FilePath, require_free_path


class Plot:
	"""
	A drawn view of a Table or an Array, made by the ``plot_*`` functions such as ``plot_line``.

	A Plot is immutable: it keeps the values it was made from, so changing the data afterwards never changes it.
	It is only displayed by ``show``, never on its own in a notebook.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices})
	>>> chart = ndp.LineChart(x="day", y=["price"], marker=ndp.MarkerShape.CIRCLE)
	>>> style = ndp.Style(title="Price per day")
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	def __init__(self, layers: list[ChartLayer], style: Style) -> None:
		"""
		Keep the charts and the style of the Plot.

		The ``plot_*`` functions create Plots; this constructor is reserved to numdaplot.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layers
			The charts and their values, the first one giving the default labels. The Plot keeps its own copy
			of the list.
		style
			The look of the Plot.
		"""
		self._layers = list(layers)
		self._style = style

	def to_matplotlib(self) -> Figure:
		"""
		Return a new matplotlib figure of the Plot, to change it with matplotlib.

		Changing the figure never changes the Plot. The figure is not managed by ``matplotlib.pyplot``, so
		a notebook does not display it on its own.

		.. versionadded:: 0.1.0

		Returns
		-------
		matplotlib.figure.Figure
			The figure, drawn on a single matplotlib ``Axes``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
		>>> style = ndp.Style(title="Prices")
		>>> figure = ndp.plot_line(prices, ndp.LineChart(), style).to_matplotlib()
		>>> figure.axes[0].get_title()
		'Prices'
		>>> figure.axes[0].lines[0].get_ydata()
		array([12. , 15.5, 14. ])
		"""
		figure = build_figure(self._layers, self._style)

		return figure

	def save(self, path: FilePath, options: ImageOptions | None = None, on_conflict: Conflict = Conflict.ERROR) -> None:
		"""
		Save the Plot as an image, in the format named by the extension of the path.

		``.png`` gives an image made of pixels, ``.svg`` and ``.pdf`` images made of lines and texts that stay
		sharp at any zoom. The image has the size of the style, 640 by 480 pixels for a PNG image by default.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the image, ending with ``.png``, ``.svg`` or ``.pdf``.
		options
			The resolution of a PNG image, 100 dots per inch when omitted. SVG and PDF images take none.
		on_conflict
			``ERROR`` refuses to overwrite an existing file, ``REPLACE`` overwrites it.

		Raises
		------
		UnsupportedImageFormatError
			When the path does not end with ``.png``, ``.svg`` or ``.pdf``.
		RefusedSettingError
			When options are given for an SVG or PDF image.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "prices.svg"
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
		>>> plot = ndp.plot_line(prices, ndp.LineChart())
		>>> plot.save(path)
		>>> path.read_text().startswith("<?xml")
		True
		"""
		file_path = Path(path)
		image_format = find_image_format(file_path)
		resolution = choose_resolution(file_path, options)
		require_free_path(file_path, on_conflict)
		figure = build_figure(self._layers, self._style)
		save_figure(figure, file_path, image_format, resolution)

	def show(self) -> None:
		"""
		Show the Plot: as an image in a Jupyter notebook, in a matplotlib window anywhere else.

		In a script, the window stays open until it is closed. With a matplotlib backend that opens no window,
		such as the one of a server, matplotlib warns that the figure cannot be shown: save it instead.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
		>>> plot = ndp.plot_bar(prices, ndp.BarChart())
		>>> plot.show()
		"""
		show_plot(self._layers, self._style)
