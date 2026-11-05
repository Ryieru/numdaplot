"""
Settings of the SAS data files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.tables.files.encoding import Encoding


@dataclass(frozen=True)
class SasOptions:
	"""
	Settings of a SAS data file (``.sas7bdat``), used by ``Table.from_sas``.

	These files are read only.

	The example reads
	[airline.sas7bdat](https://github.com/Ryieru/Numdaplot/blob/main/tests/data/airline.sas7bdat),
	a SAS data file of 32 rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	encoding
		The text encoding of the texts stored in the file, UTF-8 by default.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> latin_1 = ndp.SasOptions(encoding=ndp.Encoding.LATIN_1)
	>>> airline = ndp.Table.from_sas("airline.sas7bdat", latin_1)
	>>> airline.preview(ndp.Preview(count=3))
	     YEAR       Y       W       R       L       K
	  FLOAT64 FLOAT64 FLOAT64 FLOAT64 FLOAT64 FLOAT64
	0  1948.0   1.214   0.243  0.1454   1.415   0.612
	1  1949.0   1.354   0.260  0.2181   1.384   0.559
	2  1950.0   1.569   0.278  0.3157   1.388   0.573
	"""

	encoding: Encoding = Encoding.UTF_8
