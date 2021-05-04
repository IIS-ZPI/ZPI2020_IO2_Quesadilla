import urllib.request, json

list_of_currency = ['THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP', 'UAH', 'JPY', 'CZK',
                    'DKK', 'ISK', 'NOK', 'SEK', 'HRK', 'RON', 'BGN', 'TRY', 'ILS', 'CLP', 'PHP', 'MXN', 'ZAR', 'BRL',
                    'MYR', 'RUB', 'IDR', 'INR', 'KRW', 'CNY', 'XDR']


def get_functionality_from_user():
    user_input = int(input('''Proszę wybrać analizę statystyczną:
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

    return user_time


def get_currency_from_user(number = 0, cur1 = 'www'):
    user_currency = 'qwe'
    if number == 0:
        while user_currency not in list_of_currency:
            user_currency = (input('''Proszę wybrać walute: \n''')).upper()
    elif number == 1:
        while user_currency not in list_of_currency:
            user_currency = (input('''Proszę wybrać walute 1: \n''')).upper()
    elif number == 2:
        while (user_currency not in list_of_currency) or (user_currency == cur1):
            user_currency = (input('''Proszę wybrać walute 2: \n''')).upper()

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

        elif user_input == 3:
            user_currency_1 = get_currency_from_user(1)
            user_currency_2 = get_currency_from_user(2, user_currency_1)
        else:
            break

    print("wyłączenie systemu")

    # with urllib.request.urlopen("http://api.nbp.pl/api/exchangerates/tables/a/last/25/?format=json") as url:
    #     data = json.loads(url.read().decode())
    #     print("data")
    #     print(data)
    #     print(type(data))
    #     print(data[0].keys())
    #     print(type(data[0]['rates']))
    #     print(data[0]['rates'][1]['mid'])
    #     for i in data[0]['rates']:
    #         list_of_currency.append(i['code'])
    #
    #     print(list_of_currency)
    #
    #     list_of_currency1 = []
    #
    #     for i in data[2]['rates']:
    #         list_of_currency1.append(i['code'])
    #
    #     print(list_of_currency1)
