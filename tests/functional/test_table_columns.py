"""
Functional tests of the column operations of a Table.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

import numdaplot as ndp

CITIES = ["Paris", "Lyon"]
PRICES = [10.0, 20.0]
ZIP_CODES = ["06000", "75001"]
EXPECTED_ZIP_NUMBERS = [6000, 75001]
WRONG_ZIP_CODES = ["06000", "Nice"]
EXPECTED_CONVERSION_MESSAGE = (
	"Cannot store the TEXT value 'Nice' of the column 'zip_code' as INT32 without losing information."
)
SALE_DAY = date(2026, 12, 31)
EXPECTED_SALE_DAY_TEXT = "31/12/2026 00:00:00"
THROUGH_DATETIME_HINT = "Convert the values to DATETIME first, then to TEXT"
TAX_RATE = 1.2
EXPECTED_TAXED_PRICES = [12.0, 24.0]
EXPECTED_ADDED_NAMES = ["city", "price", "zip_code", "taxed_price"]
EXPECTED_KEPT_NAMES = ["price", "city"]
EXPECTED_SWAPPED_NAMES = ["price", "city", "zip_code"]
EXPECTED_PRICE_TEXTS = ["10.0", "20.0"]
MISSPELLED_COLUMN = "prise"
PAID_FLAGS = [True, False, True]
EXPECTED_PAID_SHARE = 2 / 3
SEVERITY_CODES = [1, 0, 1]
EXPECTED_SEVERE_FLAGS = [True, False, True]
VISIT_COUNTS = [0, 3, 1]
EXPECTED_VISITED_FLAGS = [False, True, True]
EXPECTED_VISIT_MESSAGE = "Cannot store the INT64 value 3 of the column 'visits' as BOOL without losing information."
EXPECTED_BOOLEANS_MESSAGE = "The setting booleans does not apply to a conversion from TEXT to BOOL."


def build_shops() -> ndp.Table:
	"""
	Return a Table of two shops.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The shops.
	"""
	cities = ndp.Array.from_list(CITIES)
	prices = ndp.Array.from_list(PRICES)
	zip_codes = ndp.Array.from_list(ZIP_CODES)
	shops = ndp.Table.from_arrays({"city": cities, "price": prices, "zip_code": zip_codes})

	return shops


def test_columns_are_kept_in_the_order_of_the_choice() -> None:
	"""
	Check that KEEP orders the columns as listed.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	chosen_shops = shops.choose_columns(ndp.ColumnChoice(columns=["price", "city"]))

	assert chosen_shops.column_names == EXPECTED_KEPT_NAMES


def test_two_columns_swap_their_names_in_one_call() -> None:
	"""
	Check that city and price swap their names.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()
	swap = [ndp.NameChange(old_name="city", new_name="price"), ndp.NameChange(old_name="price", new_name="city")]

	renamed_shops = shops.rename(ndp.Renaming(changes=swap))

	assert renamed_shops.column_names == EXPECTED_SWAPPED_NAMES


def test_zip_codes_written_as_texts_become_numbers() -> None:
	"""
	Check that texts of numbers convert to INT32.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	converted_shops = shops.convert(ndp.TableConversion(column="zip_code", dtype=ndp.Type.INT32))

	zip_numbers = converted_shops.column("zip_code")
	zip_list = zip_numbers.to_list()
	assert zip_list == EXPECTED_ZIP_NUMBERS


def test_a_text_that_is_not_a_number_is_named_in_the_error() -> None:
	"""
	Check the message naming the first wrong text.

	.. versionadded:: 0.1.0
	"""
	cities = ndp.Array.from_list(CITIES)
	wrong_codes = ndp.Array.from_list(WRONG_ZIP_CODES)
	shops = ndp.Table.from_arrays({"city": cities, "zip_code": wrong_codes})

	with pytest.raises(ndp.ValueConversionError) as error_info:
		shops.convert(ndp.TableConversion(column="zip_code", dtype=ndp.Type.INT32))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_CONVERSION_MESSAGE


def test_numbers_become_texts() -> None:
	"""
	Check the texts of the prices.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	text_shops = shops.convert(ndp.TableConversion(column="price", dtype=ndp.Type.TEXT))

	price_texts = text_shops.column("price")
	text_list = price_texts.to_list()
	assert text_list == EXPECTED_PRICE_TEXTS


def test_a_column_computed_from_another_one_is_added_last() -> None:
	"""
	Check that taxed prices are computed with an Array and added as a new column.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()
	prices = shops.column("price")
	taxed_prices = prices * TAX_RATE

	taxed_shops = shops.add_column(ndp.NewColumn(name="taxed_price", values=taxed_prices))

	taxed_column = taxed_shops.column("taxed_price")
	taxed_list = taxed_column.to_list()
	assert taxed_shops.column_names == EXPECTED_ADDED_NAMES
	are_close = numpy.allclose(taxed_list, EXPECTED_TAXED_PRICES)
	assert are_close


def test_an_existing_column_is_replaced_only_when_asked() -> None:
	"""
	Check that an existing name raises DuplicateColumnError, and REPLACE keeps the column at its place.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()
	prices = shops.column("price")
	taxed_prices = prices * TAX_RATE

	with pytest.raises(ndp.DuplicateColumnError):
		shops.add_column(ndp.NewColumn(name="price", values=taxed_prices))

	replacing_column = ndp.NewColumn(name="price", values=taxed_prices, on_conflict=ndp.Conflict.REPLACE)
	replaced = shops.add_column(replacing_column)
	assert replaced.column_names == shops.column_names


def test_an_unknown_column_is_named_in_the_error() -> None:
	"""
	Check that a misspelled column raises ColumnNotFoundError with its name.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	with pytest.raises(ndp.ColumnNotFoundError) as error_info:
		shops.column(MISSPELLED_COLUMN)

	error = error_info.value
	assert error.column_name == MISSPELLED_COLUMN


def test_dates_written_with_a_time_format_point_to_a_conversion_through_datetimes() -> None:
	"""
	Check that the message about a time format on dates gives a path that works.

	.. versionadded:: 0.1.0
	"""
	days = ndp.Table.from_arrays({"day": ndp.Array.from_list([SALE_DAY])})
	day_and_time = ndp.DateFormat.DAY_MONTH_YEAR_TIME
	to_text = ndp.TableConversion(column="day", dtype=ndp.Type.TEXT, format=day_and_time)

	with pytest.raises(ndp.InvalidConversionError, match=THROUGH_DATETIME_HINT):
		days.convert(to_text)

	datetimes = days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATETIME))
	texts = datetimes.convert(to_text)
	text_list = texts.column("day").to_list()
	assert text_list == [EXPECTED_SALE_DAY_TEXT]


def test_booleans_become_numbers_for_a_share() -> None:
	"""
	Check that a BOOL column converted to FLOAT64 gives 1 and 0, so its mean is the share of True.

	.. versionadded:: 0.1.0
	"""
	paid = ndp.Array.from_list(PAID_FLAGS)
	sales = ndp.Table.from_arrays({"paid": paid})

	numbers = sales.convert(ndp.TableConversion(column="paid", dtype=ndp.Type.FLOAT64))

	paid_numbers = numbers.column("paid")
	paid_share_array = paid_numbers.compute(ndp.Mean())
	paid_share = paid_share_array.to_value()
	assert paid_share == EXPECTED_PAID_SHARE


def test_zeros_and_ones_become_booleans() -> None:
	"""
	Check that a column of 0 and 1 converts to BOOL without boolean rule.

	.. versionadded:: 0.1.0
	"""
	codes = ndp.Array.from_list(SEVERITY_CODES)
	accidents = ndp.Table.from_arrays({"severe": codes})

	flags = accidents.convert(ndp.TableConversion(column="severe", dtype=ndp.Type.BOOL))

	severe_flags = flags.column("severe")
	severe_values = severe_flags.to_list()
	assert severe_values == EXPECTED_SEVERE_FLAGS


def test_another_number_than_zero_or_one_is_named_in_the_error() -> None:
	"""
	Check the message naming the first number and the column when 0 and 1 are expected.

	.. versionadded:: 0.1.0
	"""
	counts = ndp.Array.from_list(VISIT_COUNTS)
	shops = ndp.Table.from_arrays({"visits": counts})

	with pytest.raises(ndp.ValueConversionError) as error_info:
		shops.convert(ndp.TableConversion(column="visits", dtype=ndp.Type.BOOL))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_VISIT_MESSAGE


def test_every_number_but_zero_is_true_with_its_rule() -> None:
	"""
	Check that NONZERO_TRUE reads 3 as True.

	.. versionadded:: 0.1.0
	"""
	counts = ndp.Array.from_list(VISIT_COUNTS)
	shops = ndp.Table.from_arrays({"visits": counts})
	conversion = ndp.TableConversion(column="visits", dtype=ndp.Type.BOOL, booleans=ndp.BooleanRule.NONZERO_TRUE)

	flags = shops.convert(conversion)

	visited_flags = flags.column("visits")
	visited_values = visited_flags.to_list()
	assert visited_values == EXPECTED_VISITED_FLAGS


def test_a_boolean_rule_on_texts_is_refused() -> None:
	"""
	Check that a boolean rule given to a conversion of texts to BOOL raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	answers = ndp.Array.from_list(["true", "false"])
	survey = ndp.Table.from_arrays({"answer": answers})
	conversion = ndp.TableConversion(column="answer", dtype=ndp.Type.BOOL, booleans=ndp.BooleanRule.NONZERO_TRUE)

	with pytest.raises(ndp.InvalidConversionError) as error_info:
		survey.convert(conversion)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_BOOLEANS_MESSAGE
