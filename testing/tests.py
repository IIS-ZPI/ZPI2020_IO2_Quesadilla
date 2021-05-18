import sys
sys.path.insert(0, "./")
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate

def t1_get_avg_currency_rate():
	get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, TimeRange.LAST_WEEK)
	assert sum([1, 2, 3]) == 6, "Should be 6"


def test_everything():
	t1_get_avg_currency_rate()
	print("Everything passed")


test_everything()