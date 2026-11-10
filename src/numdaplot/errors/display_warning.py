"""
Warning emitted when a Plot or a Figure cannot be shown in a window.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_warning import NumdaplotWarning


class DisplayWarning(NumdaplotWarning):
	"""
	Emitted when ``show`` cannot open a window, because matplotlib has no graphical backend.

	This happens outside a Jupyter notebook when Python has no ``tkinter``, or on a server or in a container without
	a screen. Nothing is shown. The warning points at the line calling ``show`` in the calling code, and suggests
	installing ``tkinter`` or saving the image with ``save``: ``No window can be opened, matplotlib has no graphical
	backend here. Install tkinter (python3-tk on Debian and Ubuntu) to see the plot, or save it with Plot.save.``

	Silence it with the standard ``warnings`` module, for one block of code or for a whole script, alone or with every
	``NumdaplotWarning``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import warnings
	>>> plot = ndp.Plot.bar(ndp.Array.from_list([12.0, 15.5]))
	>>> with warnings.catch_warnings():
	... 	warnings.simplefilter("ignore", ndp.DisplayWarning)
	... 	plot.show()
	"""
