import requests
import re

class ParseCBR:
    def __init__(self):
        self.req = requests.get('https://cbr.ru/currency_base/daily/')
        self.src = self.req.text
        
    def Currency(self, currency : str) -> float:
        '''
        Return 1 Currency to RUB
        '''
        cur_idx : int = self.src.find(f'<td>{currency}</td>')
        if cur_idx == -1:
            return None
        s_cur_val : str = re.search(r'\d\d,\d\d\d\d', self.src[cur_idx:])
        cur_val : float = float(s_cur_val.group().replace(',','.'))
        return cur_val

    def Units(self, letter_code : str) -> int:
        '''
        Return Units currency
        '''
        cur_idx : int = self.src.find(f'<td>{letter_code}</td>')
        if cur_idx == -1:
            return None
        s_units : str = re.search(r'\d+', self.src[cur_idx:])
        units_num : int = int(s_units.group())
        return units_num

    def ConvertToRUB(self, currency_num : float, letter_code : str) -> float:
        '''
        Convert currency number to RUB
        '''
        _cur_val : float = self.Currency(letter_code)
        _cur_units : int = self.Units(letter_code)
        return round((currency_num * _cur_val) / _cur_units, 2)
    
    def Refresh(self) -> int:
        '''
        Refresh CBR site
        returns 0 if changes were made
        returns -1 if there is no change
        ''' 
        req = requests.get('https://cbr.ru/currency_base/daily/')
        src = req.text
        if src == self.src:
            return -1
        else:
            self.src = src
            return 0
        
    def LastModified (self) -> str:
        '''
        Return date of last modified
        '''
        idx_modified_start = re.search('<meta name="zoom:last-modified" content="', self.src)
        idx_modified_start = idx_modified_start.end()
        idx_modified_end = re.search('\"', self.src[idx_modified_start:])
        idx_modified_end = idx_modified_start + idx_modified_end.end() - 1
        
        last_modified : str = self.src[idx_modified_start:idx_modified_end]

        return last_modified

if __name__ == '__main__':
    Parse = ParseCBR()
    print(Parse.LastModified())
    while True:
        letter_code : str = input()
        print(Parse.Currency(letter_code))
        print(Parse.Units(letter_code))
        cur_num : int = int(input())
        print(Parse.ConvertToRUB(cur_num, letter_code))
        print(f'refresh {Parse.Refresh()}')
    

