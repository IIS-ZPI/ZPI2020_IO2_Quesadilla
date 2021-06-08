from datetime import datetime
import sys
sys.path.insert(0, "./")
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate
from analysis.analysis import get_currency_statistical_measures, get_currencies_rates_distribution, get_session_changes_over_time

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

def t4_get_avg_currency_rate():
	res = get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-01', end_date='2020-01-03')

	#{"table":"A","currency":"dolar amerykański","code":"USD","rates":[{"no":"001/A/NBP/2020","effectiveDate":"2020-01-02","mid":3.8000}]}
	#{"table":"A","currency":"dolar amerykański","code":"USD","rates":[{"no":"002/A/NBP/2020","effectiveDate":"2020-01-03","mid":3.8213}]}

	assert res["table"] == "A"
	assert res["currency"] == "dolar amerykański"
	assert res["code"] == 'USD', "should be USD"
	assert res["rates"][0]["no"] == "001/A/NBP/2020"
	assert res["rates"][0]["effectiveDate"] == "2020-01-02"
	assert res["rates"][0]["mid"] == 3.8
	assert res["rates"][1]["no"] == "002/A/NBP/2020"
	assert res["rates"][1]["effectiveDate"] == "2020-01-03"
	assert res["rates"][1]["mid"] == 3.8213

def t5_get_avg_currency_rate():
	res = get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-04', end_date='2020-01-05')

	assert res == {}

def t1_get_currency_statistical_measures():
	res = get_currency_statistical_measures(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-01', end_date='2020-01-14')

	# print(res)

def t1_get_currencies_rates_distribution():
	pass

def test_everything():
	# t1_get_avg_currency_rate()
	# t2_get_avg_currency_rate()
	# t3_get_avg_currency_rate()
	# t4_get_avg_currency_rate()
	t5_get_avg_currency_rate()
	
	# t1_get_currency_statistical_measures()
	print("Everything passed")


test_everything()