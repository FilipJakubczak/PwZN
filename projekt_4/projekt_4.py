import re
import argparse
import datetime
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager



parser = argparse.ArgumentParser()
parser.add_argument('-out', help="Out filename.")
args = parser.parse_args()

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://www.worldometers.info/coronavirus/")
link = driver.find_element_by_link_text("Poland")
ActionChains(driver).move_to_element(link).perform()
driver.execute_script("arguments[0].click();", link)

date = driver.find_element_by_class_name("news_date").text.replace(' (GMT)', '')
dt = datetime.datetime.strptime(re.sub(r"\b([0123]?[0-9])(st|th|nd|rd)\b",r"\1", date) + " " + str(datetime.datetime.now().year), "%B %d %Y")
date = str(datetime.date(dt.year, dt.month, dt.day))

cases = int(driver.find_elements_by_class_name("maincounter-number")[0].text.replace(',', ''))
deaths = int(driver.find_elements_by_class_name("maincounter-number")[1].text.replace(',', ''))
recovered = int(driver.find_elements_by_class_name("maincounter-number")[2].text.replace(',', ''))

data = {
    "date": date,
    "cases": cases,
    "deaths": deaths,
    "recovered": recovered
}

with open('{}.json'.format(args.out), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)