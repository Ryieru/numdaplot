"""
Output of a Plot: display, image files and matplotlib figures.

.. versionadded:: 0.1.0
"""

from matplotlib.figure import Figure

from numdaplot.plots.drawing.plot_drawing import build_figure
from numdaplot.plots.output.image_saving import write_image
from numdaplot.plots.output.plot_display import show_drawing
from numdaplot.plots.plot_data import PlotData
from numdaplot.plots.style.image_options import ImageOptions
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.files.file_paths import FilePath


class PlotOutput(PlotData):
	"""
	Output of a Plot: display, image files and matplotlib figures.

	Use ``ndp.Plot``; this group only adds the output methods.

	.. versionadded:: 0.1.0
	"""

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
		>>> style = ndp.PlotStyle(title="Prices")
		>>> figure = ndp.Plot.line(prices, style=style).to_matplotlib()
		>>> figure.axes[0].get_title()
		'Prices'
		>>> figure.axes[0].lines[0].get_ydata()
		array([12. , 15.5, 14. ])
		"""
		drawing = self._describe_drawing()
		figure = build_figure(drawing)

		return figure

	@checked_arguments
	def save(self, path: FilePath, options: ImageOptions | None = None, on_conflict: Conflict = Conflict.ERROR) -> None:
		"""
		Save the Plot as an image, in the format named by the extension of the path.

		``.png`` gives an image made of pixels, ``.svg`` and ``.pdf`` images made of lines and texts that stay
		sharp at any zoom. The image has the size of the style, 640 by 480 pixels for a PNG image by default.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the image, a ``FilePath`` such as ``"chart.png"`` or ``Path("images/chart.svg")``, ending with
			``.png``, ``.svg`` or ``.pdf``.
		options
			The resolution of a PNG image, 100 dots per inch when omitted. SVG and PDF images take none.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		UnsupportedImageFormatError
			When the path does not end with ``.png``, ``.svg`` or ``.pdf``.
		RefusedSettingError
			When options are given for an SVG or PDF image.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.
		FileAccessError
			When the file system refuses the file: missing folder, missing permission and so on.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "prices.svg"
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
		>>> plot = ndp.Plot.line(prices)
		>>> plot.save(path)
		>>> path.read_text().startswith("<?xml")
		True
		"""
		drawing = self._describe_drawing()
		write_image(drawing, path, options, on_conflict)

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
		>>> plot = ndp.Plot.bar(prices)
		>>> plot.show()
		"""
		drawing = self._describe_drawing()
		show_drawing(drawing)
