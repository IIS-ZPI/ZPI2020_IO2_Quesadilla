import numpy as np
from scipy import stats
from typing import Dict, Tuple
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate
from custom_errors import Response404Error

def get_currency_statistical_measures(currency_code: CurrencyCode, time_range: TimeRange, **kwargs) -> Dict:
    """
    This function is used to get median, mode, standard deviation and coefficient of variation of currency
    from NBP data.
    :param currency_code: one of the currency included in CurrencyCode
    :param time_range: one of the time interval included in TimeRange
    :return: dictionary with result :)

    Optional keyword arguments only for testing purposes:
    :param start_date: date in format '%YYYY-%mm-%dd' to specify first day of interest
    :param end_date: date in format '%YYYY-%mm-%dd' to specify last day of interest
    """
    currency_data = get_avg_currency_rate(currency_code, time_range, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))
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
        handler[session_row.get('effectiveDate')] = ((session_row.get('mid') / previous_session_row.get(
            'mid')) - 1) * 100
    return handler


def get_currencies_rates_distribution(first_currency: CurrencyCode, second_currency: CurrencyCode,
                                      time_range: TimeRange, **kwargs) -> Dict:
    """
    This function calculates difference (in percentage %) from one session to another session for chosen currencies and
     :param first_currency: Code of the very first currency
     :param second_currency: Code of second currency (must vary from the first one)
     :param time_range: Time between month and quarter
     :return: dictionary of currencies with sessions' dates and difference values

    Optional keyword arguments only for testing purposes:
    :param start_date: date in format '%YYYY-%mm-%dd' to specify first day of interest
    :param end_date: date in format '%YYYY-%mm-%dd' to specify last day of interest
    """
    if first_currency.value == second_currency.value:
        raise ValueError("Currencies' codes should not be equal")
    if kwargs.get('start_date') is None or kwargs.get('end_date') is None:
        if not (TimeRange.LAST_MONTH.value <= time_range.value <= TimeRange.LAST_QUARTER.value):
            raise ValueError(
                f"Incorrect time range. Available range: <{TimeRange.LAST_MONTH}, {TimeRange.LAST_QUARTER}>")

    currency_data_1 = get_avg_currency_rate(first_currency, time_range, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))
    currency_data_2 = get_avg_currency_rate(second_currency, time_range, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date'))
    currencies_distribution = dict()

    for currency_data in (currency_data_1, currency_data_2):
        currencies_distribution[currency_data.get('code')] = _calc_sessions_differences(currency_data)
    return currencies_distribution


def get_session_changes_over_time(currency_code: CurrencyCode, time_range: TimeRange, bias=10 ** (-5), **kwargs) -> Tuple[int, int, int]:
    """
    This function returns upward, downward and unchanged sessions counters
    :param currency_code: Code of currency to check
    :param time_range: Time of interest
    :param bias: values between <-bias, bias> are treated as there's no change
    :return: growth, loss and no change counter

    Optional keyword arguments only for testing purposes:
    :param start_date: date in format '%YYYY-%mm-%dd' to specify first day of interest
    :param end_date: date in format '%YYYY-%mm-%dd' to specify last day of interest
    """
    currency_distribution = _calc_sessions_differences(get_avg_currency_rate(currency_code, time_range, start_date=kwargs.get('start_date'), end_date=kwargs.get('end_date')))
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
    distribution = get_currencies_rates_distribution(CurrencyCode.AMERICAN_DOLLAR, CurrencyCode.AUSTRALIAN_DOLLAR,
                                                     TimeRange.LAST_QUARTER)
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

    print('\n\nTesting example', '-' * 50)
    start_date = '2020-01-01'
    end_date = '2020-01-10'
    distribution = get_currencies_rates_distribution(CurrencyCode.YEN, CurrencyCode.EURO,
                                                     None, start_date=start_date, end_date=end_date)

    yen = distribution.get(CurrencyCode.YEN.value)
    euro = distribution.get(CurrencyCode.EURO.value)

    print(f'{CurrencyCode.YEN.value} currency rate differences from {start_date} to {end_date}')
    for date, value in yen.items():
        print(f'At day {date} currency changed come to {value:.2} %')

    print(f'{CurrencyCode.EURO.value} currency rate differences from {start_date} to {end_date}')
    for date, value in euro.items():
        print(f'At day {date} currency changed come to {value:.2} %')

    print(f"Yen currency's upward, downward and unchanged session from {start_date} to {end_date}")
    growth, loss, no_change = get_session_changes_over_time(CurrencyCode.YEN, None, start_date=start_date, end_date=end_date)
    print(f'Growth: {growth}, loss: {loss}, no change: {no_change}')

    print(f'Statistics from {start_date} to {end_date} of YEN')
    for math_operation_name, value in get_currency_statistical_measures(CurrencyCode.YEN, None, start_date=start_date, end_date=end_date).items():
        print(f'{math_operation_name} = {value}')
