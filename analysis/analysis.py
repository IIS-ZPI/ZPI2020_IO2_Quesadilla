import numpy as np
from scipy import stats
from typing import Dict
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate


def get_currency_statistical_measures(currency_code: CurrencyCode, time_range: TimeRange) -> Dict:
    """
    This function is used to get median, mode, standard deviation and coefficient of variation of currency
    from NBP data.
    :param currency_code: one of the currency included in CurrencyCode
    :param time_range: one of the time interval included in TimeRange
    :return: dictionary with result :)
    """
    currency_data = get_avg_currency_rate(currency_code, time_range)
    currency_rates = [rate_info.get('mid') for rate_info in currency_data.get('rates')]

    measures = dict()
    measures['median'] = np.median(currency_rates)
    measures['mode'] = stats.mode(currency_rates)
    measures['std'] = np.std(currency_rates)
    measures['cv'] = np.std(currency_rates) / np.mean(currency_rates) * 100
    return measures


def get_currencies_rates_distribution(first_currency: CurrencyCode, second_currency: CurrencyCode, time_range: TimeRange) -> Dict:
    """
    This function is used to get median, mode, standard deviation and coefficient of variation of currency
    from NBP data.
    :param currency_code: one of the currency included in CurrencyCode
    :param time_range: one of the time interval included in TimeRange
    :return: dictionary with result :)
    """
    if first_currency.value == second_currency.value:
        raise ValueError("Currencies' codes should not be equal")
    if not (TimeRange.LAST_MONTH.value <= time_range.value <= TimeRange.LAST_QUARTER.value):
        raise ValueError(f"Incorrect time range. Available range: <{TimeRange.LAST_MONTH}, {TimeRange.LAST_QUARTER}>")

    currency_data_1 = get_avg_currency_rate(first_currency, time_range)
    currency_data_2 = get_avg_currency_rate(second_currency, time_range)
    currencies_distribution = dict()

    for currency_data in (currency_data_1, currency_data_2):
        handler = dict()
        for previous_session_row, session_row in zip(currency_data.get('rates'), currency_data.get('rates')[1:]):
            handler[session_row.get('effectiveDate')] = 100 - (session_row.get('mid') * 100 / previous_session_row.get('mid'))
        currencies_distribution[currency_data.get('code')] = handler

    return currencies_distribution


if __name__ == '__main__':
    distribution = get_currencies_rates_distribution(CurrencyCode.AMERICAN_DOLLAR, CurrencyCode.AUSTRALIAN_DOLLAR, TimeRange.LAST_QUARTER)
    american_values = distribution.get(CurrencyCode.AMERICAN_DOLLAR.value)
    australian_code = distribution.get(CurrencyCode.AUSTRALIAN_DOLLAR.value)

    print(f'American currency rate differences over {TimeRange.LAST_QUARTER.value} days')
    for date, value in american_values.items():
        print(f'At day {date} currency changed come to {value:.2} %')

    print(f'Australian currency rate differences over {TimeRange.LAST_QUARTER.value} days')
    for date, value in australian_code.items():
        print(f'At day {date} currency changed come to {value:.2} %')
