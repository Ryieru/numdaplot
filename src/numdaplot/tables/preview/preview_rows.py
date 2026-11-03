"""
Rows of a Table shown by a preview.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.side import Side


def choose_preview_rows(frame: pandas.DataFrame, preview: Preview) -> pandas.DataFrame:
	"""
	Return the rows of a Table that a preview shows, with their row numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	preview
		How many rows, and which ones.

	Returns
	-------
	pandas.DataFrame
		The chosen rows, in the order of the Table, keeping their numbers in the Table.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.preview.preview_rows import choose_preview_rows
	>>> frame = pandas.DataFrame({"price": [1.0, 2.0, 3.0]})
	>>> choose_preview_rows(frame, ndp.Preview(count=2, side=ndp.Side.END))
	price
	1    2.0
	2    3.0
	"""
	match preview.side:
		case Side.START:
			chosen_rows = frame.head(preview.count)
		case Side.END:
			chosen_rows = frame.tail(preview.count)
		case Side.RANDOM:
			row_count = len(frame)
			drawn_count = min(preview.count, row_count)
			generator = numpy.random.default_rng(preview.seed)
			drawn_rows = frame.sample(n=drawn_count, random_state=generator)
			chosen_rows = drawn_rows.sort_index()

	return chosen_rows
