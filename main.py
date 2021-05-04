import urllib.request, json


list_of_currency = []

#
# with urllib.request.urlopen("http://api.nbp.pl/api/exchangerates/tables/a/last/25/?format=json") as url:
#     data = json.loads(url.read().decode())
#     print("data")
#     print(data)
#     print(type(data))
#     print(data[0].keys())
#     print(type(data[0]['rates']))
#     print(data[0]['rates'][1]['mid'])
#
#




if __name__ == "__main__":
    print()
    print('\t\t\tWitamy w naszym systemie informatycznym!')
    print("system realizuje analize statystyczną i obliczenia na dazie danych pochodzących z platform API NBP\n")

    while True:
        user_input = int(input('''Proszę wybrać analizę statystyczną:
    1 - wyznaczenie ilości sesji wzrostowych / spadkowych / bez zmian (dla wybranej waluty)
    2 - miary statystyczne: miediana, dominanta, odchylenie standardowe i współczynnik zmienności (dla wybranej waluty)
    3 - rozkład zmian miesięcznych i kwartalnych w dowolnych wybranych parach walutowych
    4 - wyjść z systemu\n'''))

        if user_input == 1 or user_input == 2:
            user_time = 0
            while user_time < 1 or user_time > 6:
                user_time = int(input('''Proszę wybrać za jaki okres trzeba wyświetlić statystyki. Za okres:
        1) ostatniego 1 tygodnia
        2) 2 tygodni
        3) 1 miesiąca
        4) 1 kwartału
        5) pół roku
        6) 1 roku\n'''))
            user_currency = 'qwe'
            while user_currency not in list_of_currency:
                user_currency = input('''Proszę wybrać walute: \n''')

        elif user_input == 3:
            print('3')

        else:
            break



    print("wyłączenie systemu")