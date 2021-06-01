import urllib.request, json
from url_builder.url_builder import CurrencyCode, TimeRange, get_avg_currency_rate
from analysis.analysis import *

list_of_currency = ['THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP', 'UAH', 'JPY', 'CZK',
                    'DKK', 'ISK', 'NOK', 'SEK', 'HRK', 'RON', 'BGN', 'TRY', 'ILS', 'CLP', 'PHP', 'MXN', 'ZAR', 'BRL',
                    'MYR', 'RUB', 'IDR', 'INR', 'KRW', 'CNY', 'XDR']


def get_functionality_from_user():
    user_input = int(input('''\nProszę wybrać analizę statystyczną:
        1 - wyznaczenie ilości sesji wzrostowych / spadkowych / bez zmian (dla wybranej waluty)
        2 - miary statystyczne: miediana, dominanta, odchylenie standardowe i współczynnik zmienności (dla wybranej waluty)
        3 - rozkład zmian miesięcznych i kwartalnych w dowolnych wybranych parach walutowych
        4 - wyjść z systemu\n'''))

    return user_input


def get_period_of_time_from_user():
    user_time = 0
    while user_time < 1 or user_time > 6:
        user_time = int(input('''Proszę wybrać za jaki okres trzeba wyświetlić statystyki. Za okres:
            1) ostatniego 1 tygodnia
            2) 2 tygodni
            3) 1 miesiąca
            4) 1 kwartału
            5) pół roku
            6) 1 roku\n'''))

    return_time = TimeRange.LAST_WEEK
    for time in (TimeRange):
        return_time = time
        user_time = user_time - 1
        if user_time < 1:
            break

    return return_time


def get_currency_from_user():
    while True:
        user_currency = (input('Proszę wybrać walute: ' + str(list_of_currency) + '\n')).upper()
        if user_currency in list_of_currency:
            break

    user_currency = CurrencyCode(user_currency)
    return user_currency


if __name__ == "__main__":
    print()
    print('\t\t\tWitamy w naszym systemie informatycznym!')
    print("system realizuje analize statystyczną i obliczenia na dazie danych pochodzących z platform API NBP\n")

    while True:
        user_input = get_functionality_from_user()

        if user_input == 1 or user_input == 2:

            user_time = get_period_of_time_from_user()
            user_currency = get_currency_from_user()

            if user_input == 1:
                output_tuple = get_session_changes_over_time(user_currency, user_time)
                print('\ndla ' + user_currency.value + ' (' + user_currency.name + ') waluty:')
                print("ilości sesji wzrostowych: " + str(output_tuple[0]))
                print("ilości sesji spadkowych: " + str(output_tuple[1]))
                print("ilości sesji bez zmian: " + str(output_tuple[2]))

            elif user_input == 2:
                output_dict = get_currency_statistical_measures(user_currency, user_time)
                print('\ndla ' + user_currency.value + ' (' + user_currency.name + ') waluty:')
                print("miediana: " + str(output_dict['median']))
                print("dominanta: " + str(output_dict['mode']))
                print("odchylenie standardowe: " + str(output_dict['std']))
                print("współczynnik zmienności: " + str(output_dict['cv']))

        elif user_input == 3:

            user_currency_1 = get_currency_from_user()
            while True:
                user_currency_2 = get_currency_from_user()
                if user_currency_2 != user_currency_1:
                    break

            output_dict = get_currencies_rates_distribution(user_currency_1, user_currency_2, TimeRange.LAST_MONTH)
            print(output_dict)

        else:
            break

    print("wyłączenie systemu")
