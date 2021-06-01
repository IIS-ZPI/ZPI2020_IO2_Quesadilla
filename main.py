from enum import IntEnum, auto

from url_builder.url_builder import CurrencyCode, TimeRange
from analysis.analysis import get_session_changes_over_time, get_currency_statistical_measures, \
    get_currencies_rates_distribution


class Action(IntEnum):
    GROWTH_LOSS_CHANGES = auto()
    STATISTIC_MEASURES = auto()
    CURRENCY_DISTRIBUTION_RATE = auto()
    EXIT = auto()
    INCORRECT = auto()


def get_functionality_from_user() -> Action:
    try:
        action = Action(int(input("""\nProszę wybrać analizę statystyczną:
    1 - wyznaczenie ilości sesji wzrostowych / spadkowych / bez zmian (dla wybranej waluty)
    2 - miary statystyczne: miediana, dominanta, odchylenie standardowe i współczynnik zmienności (dla wybranej waluty)
    3 - rozkład zmian miesięcznych i kwartalnych w dowolnych wybranych parach walutowych
    4 - wyjdź z systemu\n> """)))
    except ValueError:
        action = Action.INCORRECT
    return action


def get_period_of_time_from_user(**kwargs) -> TimeRange:
    lookup_times = kwargs.get('time_range') or {1: TimeRange.LAST_WEEK, 2: TimeRange.LAST_TWO_WEEKS,
                                                3: TimeRange.LAST_MONTH,
                                                4: TimeRange.LAST_QUARTER, 5: TimeRange.LAST_HALF_OF_YEAR,
                                                6: TimeRange.LAST_YEAR}
    prompt = kwargs.get('prompt') or """Proszę wybrać za jaki okres trzeba wyświetlić statystyki. Za okres:
    1) ostatniego 1 tygodnia
    2) 2 tygodni
    3) 1 miesiąca
    4) 1 kwartału
    5) pół roku
    6) 1 roku\n> """

    time_range = None
    while time_range not in lookup_times.keys():
        try:
            time_range = int(input(prompt))
        except ValueError:
            print('Niepoprawny przedział czasu!')
            time_range = None
    return lookup_times.get(time_range)


def get_currency_from_user(prompt='Proszę wybrać kod waluty. (By wyświelić dostępne waluty wpisz "/h")\n> ') -> CurrencyCode:
    chosen_code = 'NONE'
    while chosen_code.upper() not in CurrencyCode:
        chosen_code = input(prompt)
        if '/h' == chosen_code:
            for cc in CurrencyCode:
                print(f'{str(cc)[len("CurrencyCode."):]}, code: {cc.value}')
        if chosen_code.upper() not in CurrencyCode:
            print('Niepoprawny kod waluty')
    return CurrencyCode(chosen_code.upper())


if __name__ == "__main__":
    print('Witamy w naszym systemie informatycznym!')
    print("System realizuje analizę statystyczną i obliczenia na bazie danych pochodzących z platform API NBP\n")

    while True:
        user_input = get_functionality_from_user()
        if Action.EXIT == user_input:
            break

        elif Action.GROWTH_LOSS_CHANGES == user_input:
            curr_code = get_currency_from_user()
            time = get_period_of_time_from_user()
            growth, loss, no_change = get_session_changes_over_time(curr_code, time)
            print('-' * 50,
                  f'\n{str(curr_code)[len("CurrencyCode."):]}:\nilości sesji wzrostowych:  {growth},\nilości sesji spadkowych: {loss},\nilości sesji bez zmian:  {no_change}'
                  f'\nprzez ostatnie {time.value} dni\n',
                  '-' * 50)

        elif Action.STATISTIC_MEASURES == user_input:
            curr_code = get_currency_from_user()
            time = get_period_of_time_from_user()
            measurements = get_currency_statistical_measures(curr_code, time)
            print('-' * 50, f'\n{str(curr_code)[len("CurrencyCode."):]}:')
            print("miediana: " + str(measurements['median']))
            print("dominanta: " + str(measurements['mode'][0][0]))
            print("odchylenie standardowe: " + str(measurements['std']))
            print("współczynnik zmienności: " + str(measurements['cv']))
            print(f'przez ostatnie {time.value} dni')
            print('-' * 50)

        elif Action.CURRENCY_DISTRIBUTION_RATE == user_input:
            distribution = None
            time = None
            while True:
                try:
                    curr_code_1 = get_currency_from_user('Podaj kod pierwszej waluty. (By wyświelić dostępne waluty '
                                                         'wpisz "/h")\n> ')
                    curr_code_2 = get_currency_from_user('Podaj kod drugiej waluty. (By wyświelić dostępne waluty '
                                                         'wpisz "/h")\n> ')

                    new_prompt = "Proszę wybrać za jaki okres trzeba wyświetlić statystyki. Za okres:\n1) 1 " \
                                 "miesiąca\n2) 1 kwartału\n> "
                    time = get_period_of_time_from_user(time_range={1: TimeRange.LAST_MONTH, 2: TimeRange.LAST_QUARTER},
                                                        prompt=new_prompt)

                    distribution = get_currencies_rates_distribution(curr_code_1, curr_code_2, time)
                except ValueError:
                    print('Waluty nie mogą być takie same!')
                    continue
                break

            for currency_name, currency_values in distribution.items():
                print(f'Różnice kursowe {currency_name} przez ostatnie {time.value} dni')
                for date, value in currency_values.items():
                    print(f"{date} zmiana {'w górę' if value > 0. else 'w dół'} o {value:.2}%")

        else:
            print('Niepoprawna opcja! Proszę wybrać ponownie.')
    print("Wyłączenie systemu")
