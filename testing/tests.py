import unittest
from datetime import datetime
from custom_errors import Response404Error
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate
from analysis.analysis import get_currency_statistical_measures, get_currencies_rates_distribution, get_session_changes_over_time


class AvgCurrencyRateTest(unittest.TestCase):

	def test_get_avg_currency_rate(self):
		res = get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, TimeRange.LAST_WEEK)
		self.assertEqual(res["code"], 'USD')
		dt2 = datetime.strptime(res["rates"][0]["effectiveDate"], "%Y-%m-%d")
		dt1 = datetime.strptime(res["rates"][-1]["effectiveDate"], "%Y-%m-%d")
		self.assertTrue((dt1 - dt2).days <= 7)

	def test_get_avg_currency_rate_2(self):
		res = get_avg_currency_rate(CurrencyCode.CANADIAN_DOLLAR, TimeRange.LAST_TWO_WEEKS)
		self.assertEqual(res["code"], 'CAD')
		dt2 = datetime.strptime(res["rates"][0]["effectiveDate"], "%Y-%m-%d")
		dt1 = datetime.strptime(res["rates"][-1]["effectiveDate"], "%Y-%m-%d")
		self.assertTrue((dt1 - dt2).days <= 14)

	def test_get_avg_currency_rate_3(self):
		res = get_avg_currency_rate(CurrencyCode.YEN, TimeRange.LAST_YEAR)
		self.assertEqual(res["code"], 'JPY')
		dt2 = datetime.strptime(res["rates"][0]["effectiveDate"], "%Y-%m-%d")
		dt1 = datetime.strptime(res["rates"][-1]["effectiveDate"], "%Y-%m-%d")
		self.assertTrue((dt1 - dt2).days <= 365)

	def test_get_avg_currency_rate_4(self):
		res = get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-01', end_date='2020-01-03')
		self.assertEqual(res["table"], "A")
		self.assertEqual(res["currency"], "dolar amerykański")
		self.assertEqual(res["code"], 'USD')
		self.assertEqual(res["rates"][0]["no"], "001/A/NBP/2020")
		self.assertEqual(res["rates"][0]["effectiveDate"], "2020-01-02")
		self.assertEqual(res["rates"][0]["mid"], 3.8)
		self.assertEqual(res["rates"][1]["no"], "002/A/NBP/2020")
		self.assertEqual(res["rates"][1]["effectiveDate"], "2020-01-03")
		self.assertEqual(res["rates"][1]["mid"], 3.8213)

	def test_get_avg_currency_rate_5(self):
		with self.assertRaises(Response404Error):
			get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-04', end_date='2020-01-05')


class StatisticalMeasuresTest(unittest.TestCase):
	def test_if_empty(self):
		with self.assertRaises(Response404Error):
			get_currency_statistical_measures(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-04', end_date='2020-01-05')

	def test_usd_in_two_weeks(self):
		res = get_currency_statistical_measures(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2021-05-25', end_date='2021-06-08')
		self.assertEqual(res.get('median'), 3.66905)
		self.assertEqual(res.get('mode')[0], 3.6549)
		self.assertEqual(res.get('std'), 0.012083480458874382)
		self.assertEqual(res.get('cv'), 0.3290842615813386)

	def test_yen_in_year(self):
		res = get_currency_statistical_measures(CurrencyCode.YEN, None, start_date='2020-06-08', end_date='2021-06-08')
		self.assertEqual(res.get('median'), 0.035598500000000005)
		self.assertEqual(res.get('mode')[0], 0.035991)
		self.assertEqual(res.get('std'), 0.000900877294990445)
		self.assertEqual(res.get('cv'), 2.5255031372776733)


class SessionOverTimeTest(unittest.TestCase):
	def test_if_empty(self):
		with self.assertRaises(Response404Error):
			get_session_changes_over_time(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-04', end_date='2020-01-05')

	def test_aud_in_week(self):
		res = get_session_changes_over_time(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2021-06-01', end_date='2021-06-08')
		up_down_none = (3, 1, 0)
		self.assertEqual(res, up_down_none)

	def test_euro_in_two_weeks(self):
		res = get_session_changes_over_time(CurrencyCode.EURO, None, start_date='2021-05-25', end_date='2021-06-08')
		up_down_none = (4, 5, 0)
		self.assertEqual(res, up_down_none)

	def test_chilean_peso_in_last_year(self):
		res = get_session_changes_over_time(CurrencyCode.CHILEAN_PESO, None, start_date='2020-06-08', end_date='2021-06-08')
		print(res)
		up_down_none = (124, 127, 2)
		self.assertEqual(res, up_down_none)


if __name__ == '__main__':
	unittest.main()
