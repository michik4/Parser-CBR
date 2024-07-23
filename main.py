from CurrencyParse import ParseCBR

if __name__ == '__main__':
    Parse = ParseCBR()
    while(True):
        currency = input()
        num_cur = int(input())
        if currency == '0':
            break
        print(Parse.Currency(currency))
        print(Parse.Units(currency))
        print(Parse.ConvertToRUB(num_cur, currency), 'RUB')

