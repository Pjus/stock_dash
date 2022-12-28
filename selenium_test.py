from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import json
from pymongo import MongoClient

with open("SECRET.json", "r") as secret_json:
    sc_python = json.load(secret_json)

client = MongoClient(sc_python['MONGODB'], 27017)
db = client['stockDB']

calender_collection = db['calender']


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    url = "https://kr.tradingview.com/economic-calendar/"

    driver = webdriver.Chrome("~/Downloads/chromedriver.exe", options=options)
    driver.get(url)
    driver.implicitly_wait(3)

    items = driver.find_elements(by=By.CLASS_NAME, value='economicCalendarItem-Q1EBfqP8')
    driver.implicitly_wait(1)
    event_day = driver.find_elements(by=By.CLASS_NAME, value='innerWrapper-sM9C7FZj')
    driver.implicitly_wait(1)

    date = []
    data_dict = {}


    for day in event_day:
        data_dict[day.text] = {}
        date.append(day.text)
    
    day_start = -1
    defalut_time = 24

    for item_idx, item in enumerate(items):
        temp_dict = {}

        country = item.find_element(by=By.CLASS_NAME, value='country-Q1EBfqP8')
        inner_html = country.get_attribute("innerHTML")
        
        temp_dict['img_src'] = inner_html[inner_html.find("https"):inner_html.find("><")]
        temp_dict['country'] = re.compile('[가-힣]+').findall(inner_html)[0]
        all_data = item.text.split("\n")
       
        if ':' in all_data[0]:
            event_time = all_data[0]
            event_subject = all_data[1]

        else:
            if ':' in items[item_idx-1].text.split("\n")[0]:
                event_time = items[item_idx-1].text.split("\n")[0]
            else:
                event_time = items[item_idx-2].text.split("\n")[0]
            event_subject = all_data[0]

        if int(event_time.split(":")[0]) < defalut_time:
            day_start += 1
        defalut_time = int(event_time.split(":")[0])

        if "예측" in all_data:
            if all_data[-1] == '%':
                temp_dict['forecast'] = all_data[-5]
            else:
                temp_dict['forecast'] = all_data[-1]

        if "이전" in all_data:
            if all_data[-1] == '%':
                temp_dict['previous'] = all_data[-2]
            else:
                temp_dict['previous'] = all_data[-1]
                
        temp_dict['event_time'] = event_time
        temp_dict['event_subject'] = event_subject
        temp_dict['event_date'] = date[day_start]
        data_dict[date[day_start]][temp_dict['country']] = temp_dict
