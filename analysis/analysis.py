import numpy as np
from scipy import stats
from typing import Dict, Tuple
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


def _calc_sessions_differences(currency_data: Dict) -> Dict:
    handler = dict()
    for previous_session_row, session_row in zip(currency_data.get('rates'), currency_data.get('rates')[1:]):
        handler[session_row.get('effectiveDate')] = ((session_row.get('mid') / previous_session_row.get('mid')) - 1) * 100
    return handler


def get_currencies_rates_distribution(first_currency: CurrencyCode, second_currency: CurrencyCode, time_range: TimeRange) -> Dict:
    """
    This function calculates difference (in percentage %) from one session to another session for chosen currencies and
     :param first_currency: Code of the very first currency
     :param second_currency: Code of second currency (must vary from the first one)
     :param time_range: Time between month and quarter
     :return: dictionary of currencies with sessions' dates and difference values
    """
    if first_currency.value == second_currency.value:
        raise ValueError("Currencies' codes should not be equal")
    if not (TimeRange.LAST_MONTH.value <= time_range.value <= TimeRange.LAST_QUARTER.value):
        raise ValueError(f"Incorrect time range. Available range: <{TimeRange.LAST_MONTH}, {TimeRange.LAST_QUARTER}>")

    currency_data_1 = get_avg_currency_rate(first_currency, time_range)
    currency_data_2 = get_avg_currency_rate(second_currency, time_range)
    currencies_distribution = dict()

    for currency_data in (currency_data_1, currency_data_2):
        currencies_distribution[currency_data.get('code')] = _calc_sessions_differences(currency_data)
    return currencies_distribution


def get_session_changes_over_time(currency_code: CurrencyCode, time_range: TimeRange, bias=10**(-5)) -> Tuple[int, int, int]:
    """
    This function returns upward, downward and unchanged sessions counters
    :param currency_code: Code of currency to check
    :param time_range: Time of interest
    :param bias: values between <-bias, bias> are treated as there's no change
    :return: growth, loss and no change counter
    """
    currency_distribution = _calc_sessions_differences(get_avg_currency_rate(currency_code, time_range))
    growth_counter = loss_counter = no_change_counter = 0

    for record in currency_distribution.values():
        if -bias < record < bias:
            no_change_counter += 1
        elif record < 0:
            loss_counter += 1
        else:
            growth_counter += 1
    return growth_counter, loss_counter, no_change_counter


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

    print(f"American currency's upward, downward and unchanged session over {TimeRange.LAST_WEEK.value} days")
    growth, loss, no_change = get_session_changes_over_time(CurrencyCode.AMERICAN_DOLLAR, TimeRange.LAST_WEEK)
    print(f'Growth: {growth}, loss: {loss}, no change: {no_change}')
