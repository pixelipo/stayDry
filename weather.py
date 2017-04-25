import requests
from bs4 import BeautifulSoup


class WeatherModel:

    def __init__(self, args):
        self.searchTerm = args.pop(0)

        if args:
            # this is hours-5 we are mapping
            self.hours = list(map(lambda x: int(x) - 5, args))
        else:
            # default, equivalent of 7-9AM and 3-5PM
            self.hours = [2, 3, 10, 11]

    def findCity(self):
        # TODO: use json instead of crawler
        # import json
        # json_data = open("file root")
        # data = json.load(json_data)

        url = "https://www.yr.no/soek/soek.aspx"
        params = {'spr': 'eng', 'sted': self.searchTerm}

        data = requests.get(url, params=params)
        data_parsed = BeautifulSoup(data.text, "lxml")

        table = data_parsed.find('table', {'class': 'yr-table-search-results'})
        if table is None:

            return None
        else:
            location = table.find('a')
            self.city = (location['title'], location['href'])

            return(self.city)

    def fetchWeather(self):
        url_prefix = "https://www.yr.no"
        url_suffix = "hour_by_hour.html"
        self.city = self.findCity()
        if self.city is None:

            return("Location not found!")

        data = requests.get(url_prefix + self.city[1] + url_suffix)
        data_parsed = BeautifulSoup(data.text, "lxml")

        tables = data_parsed.find_all('table', {'class': 'yr-table-hourly'})
        rows = tables[1].find_all('tr')
        rain = 0

        for hour in self.hours:
            mm = rows[hour].find('td', {'class': 'precipitation'}).string
            rain += float(mm[0].replace(",", "."))

        return rain
