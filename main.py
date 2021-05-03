import urllib.request, json



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

        if user_input == 4:
            break



    print("wyłączenie systemu")