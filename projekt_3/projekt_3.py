import requests
import re
import argparse
import datetime
import json
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()
parser.add_argument('-out', help="Out filename.")
args = parser.parse_args()


page_url = 'https://www.worldometers.info/coronavirus/country/poland/'
page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')
 

date = soup.find_all("div", {"class": "news_date"})[0].get_text().replace(' (GMT)', '')
dt = datetime.datetime.strptime(re.sub(r"\b([0123]?[0-9])(st|th|nd|rd)\b",r"\1", date) + " " + str(datetime.datetime.now().year), "%B %d %Y")
date = str(datetime.date(dt.year, dt.month, dt.day))

cases = int(soup.find_all("div", {"class": "maincounter-number"})[0].get_text().replace(',', ''))
deaths = int(soup.find_all("div", {"class": "maincounter-number"})[1].get_text().replace(',', ''))
recovered = int(soup.find_all("div", {"class": "maincounter-number"})[2].get_text().replace(',', ''))
print(date, cases, deaths, recovered)

data = {
    "date": date,
    "cases": cases,
    "deaths": deaths,
    "recovered": recovered
}

with open('{}.json'.format(args.out), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)