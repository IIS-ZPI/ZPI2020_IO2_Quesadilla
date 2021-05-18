from datetime import datetime
import sys
sys.path.insert(0, "./")
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate

def t1_get_avg_currency_rate():
	res = get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, TimeRange.LAST_WEEK)

	assert res["code"] == 'USD', "should be USD"

	dt2 = datetime.strptime(res["rates"][0]["effectiveDate"], "%Y-%m-%d")
	dt1 = datetime.strptime(res["rates"][-1]["effectiveDate"], "%Y-%m-%d")
	assert (dt1 - dt2).days <= 7, "should be max 7 days"


def t2_get_avg_currency_rate():
	res = get_avg_currency_rate(CurrencyCode.CANADIAN_DOLLAR, TimeRange.LAST_TWO_WEEKS)

	assert res["code"] == 'CAD', "should be CAD"

	dt2 = datetime.strptime(res["rates"][0]["effectiveDate"], "%Y-%m-%d")
	dt1 = datetime.strptime(res["rates"][-1]["effectiveDate"], "%Y-%m-%d")
	assert (dt1 - dt2).days <= 14, "should be max 14 days"

def t3_get_avg_currency_rate():
	res = get_avg_currency_rate(CurrencyCode.YEN, TimeRange.LAST_YEAR)

	assert res["code"] == 'JPY', "should be JPY"

	dt2 = datetime.strptime(res["rates"][0]["effectiveDate"], "%Y-%m-%d")
	dt1 = datetime.strptime(res["rates"][-1]["effectiveDate"], "%Y-%m-%d")
	assert (dt1 - dt2).days <= 365, "should be max 365 days"

def test_everything():
	t1_get_avg_currency_rate()
	t2_get_avg_currency_rate()
	t3_get_avg_currency_rate()
	print("Everything passed")


test_everything()