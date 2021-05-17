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


if __name__ == '__main__':
    ms = get_currency_statistical_measures(CurrencyCode.AMERICAN_DOLLAR, TimeRange.LAST_WEEK)
    print(ms)
