import glob
import os
import requests
import json
from json import JSONDecodeError


class RestCountries():

    def __init__(self):
        self.url = 'https://restcountries.eu/rest/v2'
        self.directory = 'currencies'
        self.prepare_currencies_directory()

    def request(self, method='GET'):
        response = requests.request(
            method,
            url=self.url,
        )
        try:
            content = json.loads(response.content.decode(errors='ignore'))
        except JSONDecodeError:
            content = response.content.decode(errors='ignore')

        return content

    def parse_countries(self):
        content = self.request()

        for country in content:
            self.parse_currencies(country['name'], country['currencies'])

    def parse_currencies(self, country_name: str, country_currencies: dict):
        for currency in country_currencies:
            if currency['code'] == None or currency['code'] == '(none)': #kilka walut nie miało przypisanego kodu waluty
                if not currency['name']: #gdy nie ma kodu ani nazwy to ignorujemy
                    continue
                currency['code'] = currency['name']

            self.add_country_to_currency(country_name,currency['code'])

    def add_country_to_currency(self, country_name: str, currency_code: str):
        with open(f'{self.directory}/{currency_code}.txt','a') as file:
            file.write(country_name+"\n")

    def prepare_currencies_directory(self):
        os.makedirs(self.directory, exist_ok=True) #tworzę katalog, jeśli nie istnieje
        files = glob.glob(f'{self.directory}/*.txt') #usuwam stare pliki
        for f in files:
            os.remove(f)

if __name__ == '__main__':
    RestCountries().parse_countries()

