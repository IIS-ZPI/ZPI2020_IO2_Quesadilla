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
		self.assertRaises(
			Response404Error,
			get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, None, start_date='2020-01-04', end_date='2020-01-05')
		)

	def test_get_currencies_rates_distribution_1(self):
			pass


if __name__ == '__main__':
	unittest.main()
