from datetime import datetime, timedelta
from enum import Enum, EnumMeta
from typing import Dict
import requests
from custom_errors import Response404Error


class ContainsEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class CurrencyCode(Enum, metaclass=ContainsEnum):
    """
    Represents NBP currencies according to https://www.nbp.pl/kursy/kursya.html
    """
    THAILAND_BAT = 'THB'
    AMERICAN_DOLLAR = 'USD'
    AUSTRALIAN_DOLLAR = 'AUD'
    HONG_KONG_DOLLAR = 'HKD'
    CANADIAN_DOLLAR = 'CAD'
    NEW_ZEALANDER_DOLLAR = 'NZD'
    SINGAPOREAN_DOLLAR = 'SGD'
    EURO = 'EUR'
    FORINT = 'HUF'
    SWISS_FRANK = 'CHF'
    STERLING = 'GBP'
    HRYVNIA = 'UAH'
    YEN = 'JPY'
    CZECH_KORUNA = 'CZK'
    DANISH_KRONE = 'DKK'
    ICELANDIC_KRONA = 'ISK'
    NORWEGIAN_CROWN = 'NOK'
    SWEDISH_KRONA = 'SEK'
    CROATIAN_KUNA = 'HRK'
    ROMANIAN_LEU = 'RON'
    LEV = 'BGN'
    TURKISH_LIRA = 'TRY'
    ISRAELI_NEW_SHEKEL = 'ILS'
    CHILEAN_PESO = 'CLP'
    PHILIPPINE_PESO = 'PHP'
    MEXICAN_PESO = 'MXN'
    RAND = 'ZAR'
    REAL = 'BRL'
    RINGGIT = 'MYR'
    RUSSIAN_RUBEL = 'RUB'
    INDONESIAN_RUPIAH = 'IDR'
    INDIAN_RUPIAH = 'INR'
    SOUTH_KOREAN_WON = 'KRW'
    YUAN_RENMINBI = 'CNY'
    SDR = 'XDR'


class TableType(Enum):
    """
    Represents NBP tables according to https://www.nbp.pl/home.aspx?f=/kursy/instrukcja_pobierania_kursow_walut.html
    """
    AVERAGE_EXCHANGE_RATE = 'a'
    AVERAGE_UNTRADABLE_RATE = 'b'
    BID_ASK_RATE = 'c'


class TimeRange(Enum, metaclass=ContainsEnum):
    """
    Represents days to subtract from today (end_date) to get start_date
    Used for extracting NBP currencies' records
    """
    LAST_WEEK = 7
    LAST_TWO_WEEKS = 14
    LAST_MONTH = 30
    LAST_QUARTER = 90
    LAST_HALF_OF_YEAR = 182
    LAST_YEAR = 365
    LAST_LEAP_YEAR = 366


def get_avg_currency_rate(currency_code: CurrencyCode, time_range: TimeRange, **kwargs) -> Dict:
    """
    This function request NBP API for a average exchange rate of given :param time_range

    :param currency_code: one of available currency codes. Available in CurrencyCode class.
    :param time_range: available time ranges for request. Available in TimeRange class.
    :return: return json response as python dictionary

    Optional keyword arguments:
    :param table_type: average exchange rate (Table A) as default
    Only for testing purposes:
    :param start_date: date in format '%YYYY-%mm-%dd' to specify first day of interest
    :param end_date: date in format '%YYYY-%mm-%dd' to specify last day of interest
    """

    format_arg = '?format=json'
    table_type = kwargs.get('table_type') or TableType.AVERAGE_EXCHANGE_RATE
    base_url = 'http://api.nbp.pl/api/exchangerates/rates'

    date_format = '%Y-%m-%d'
    end_date = kwargs.get('end_date') or datetime.today().strftime(date_format)
    start_date = kwargs.get('start_date') or (datetime.today() - timedelta(days=time_range.value)).strftime(date_format)

    url = f'{base_url}/{table_type.value}/{currency_code.value}/{start_date}/{end_date}{format_arg}'

    return_value = requests.get(url).json()

    if return_value == null:
        raise Response404Error

    return return_value


if __name__ == '__main__':
    print('Examples of requests')
    print("---Currencies' values of last week", '-' * 47)
    for cc in CurrencyCode:
        print(get_avg_currency_rate(cc, TimeRange.LAST_WEEK))
    print('---Euro values of different time ranges', '-' * 47)
    for tr in TimeRange:
        print(f'TimeRange {tr}')
        print(get_avg_currency_rate(CurrencyCode.AMERICAN_DOLLAR, tr))

    print('Testing only')
    print(get_avg_currency_rate(CurrencyCode.EURO, None, start_date='2020-01-01', end_date='2020-01-31'))
    print(get_avg_currency_rate(CurrencyCode.AUSTRALIAN_DOLLAR, None, start_date='2020-01-01', end_date='2020-12-31'))
