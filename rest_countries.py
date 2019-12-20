"""
This file contains class to integration with external api https://restcountries.eu/rest/v2
Using this api, creates text files  with the same name as the three-letter currency name.
Each file contains a list of countries using this currency
"""
import glob
import os
import requests
import json
from json import JSONDecodeError


class RestCountries():

    def __init__(self):
        """
        Class implements integration with external api https://restcountries.eu/rest/v2
        to download list of countries and theirs currencies
        """
        self.url = 'https://restcountries.eu/rest/v2'
        self.directory_to_write = 'currencies'
        self.prepare_currencies_directory()

    def request(self):
        """
        Method sends simple GET request to api, and returns content from its response
        :return: response content as  json
        """
        response = requests.request("GET", url=self.url)
        try:
            content = json.loads(response.content.decode(errors='ignore'))
        except JSONDecodeError:
            content = response.content.decode(errors='ignore')

        return content

    def parse_countries(self):
        """
        The method retrieves a list of countries from api in json format and parses it to group them by currency
        creates currency directory with txt files (every currency in one file)
        :return: None
        """
        content = self.request()

        for country in content:
            self.parse_currencies(country['name'], country['currencies'])

    def parse_currencies(self, country_name: str, country_currencies):
        """
        The method parses a list of country_currencies , for each one  creates text file named {currency_name}.txt (if doesn't exist) .
        Then appends {country_name} to this file
        :param country_name: str , name of country
        :param country_currencies: json object of currencies list
        :return: None
        """
        for currency in country_currencies:
            # some currencies hasn't  currency code assigned, I get a currency name
            if currency['code'] == None or currency['code'] == '(none)':
                #some currencies hasn't currency name assigned, I ignore them
                if not currency['name']:
                    continue
                currency['code'] = currency['name']

            self.add_country_to_currency(country_name,currency['code'])

    def add_country_to_currency(self, country_name: str, currency_code: str):
        """
        The method appends {country_name} to file {currency_code}.txt (if doesnt exists, creates it)
        in directory {self.directory_to_write}
        :param country_name: str
        :param currency_code: tree-letter currency code
        :return: None
        """
        with open(f'{self.directory_to_write}/{currency_code}.txt','a') as file:
            file.write(country_name+"\n")

    def prepare_currencies_directory(self):
        """
        The method prepares directory {self.directory_to_write}
        :return: None
        """
        os.makedirs(self.directory_to_write, exist_ok=True)

        files = glob.glob(f'{self.directory_to_write}/*.txt')
        for f in files:
            os.remove(f)

if __name__ == '__main__':
    RestCountries().parse_countries()

