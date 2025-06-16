from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from prettytable import PrettyTable
from selenium import webdriver
from datetime import datetime
import pyspark
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import itertools
# url = "https://www.wunderground.com/history/monthly/vn/ho-chi-minh/date/2023-5"
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get(url)

def scrape_weather_data(url):
    
    time.sleep(10)
    table = driver.find_element(
        By.CSS_SELECTOR, "#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > lib-city-history-observation > div > div.observation-table.ng-star-inserted")
    
    print(table.text)
    return table.text


# Thực hiện cào dữ liệu cho thành phố Hanoi
# For tentp in list:
# 	For year in range(2021, 2024):
# 		For month in range(1, 13):
# 			/* truy cập vào url * /
# 			url = “https: // www.wunderground.com/history/monthly/vn /”+tentp +”/date /”+year +”-“+”month”
# /*** crawl dữ liệu***/
# If(year == 2023 and month == 6):
# 	break
list_tinh1 = ['hoa-binh','son-la','dien-bien','lai-chau','lao-cai','yen-bai','thanh-hoa','nghe-an','ha-tinh','quang-binh','quang-tri','thua-thien-hue','ho-chi-minh','vung-tau','binh-duong','binh-phuoc','dong-nai','tay-ninh','phu-tho','ha-giang','tuyen-quang','cao-bang','bac-kan','thai-nguyen','lang-son','bac-giang','quang-ninh','da-nang','quang-nam','quang-ngai','binh-dinh','phu-yen','khanh-hoa','ninh-thuan','binh-thuan','ha-noi','bac-ninh','ha-nam','hai-duong','hai-phong','hung-yen','nam-dinh','thai-binh','vinh-phuc','ninh-binh','kon-tum','dak-lak','dak-nong','lam-dong','an-giang','bac-lieu','ben-tre','ca-mau','can-tho','dong-thap','hau-giang','kien-giang','long-an','soc-trang','tien-giang','tra-vinh','vinh-long']
list_tinh = ['ho-chi-minh']
l=[]
for ten_tinh in list_tinh:
    for year in range(2021, 2024):
        for month in range(1,13):
            date = str(year)+"-"+str(month)
            #truy cập vào trang web
            url = "https://www.wunderground.com/history/monthly/vn/"+ten_tinh+"/date/"+str(year)+"-"+str(month)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)
            try:
                # chờ load
                time.sleep(5)
                # crawl bảng tháng
                text = scrape_weather_data(url)
                # viết vào line tiếp theo của file text data
                print(text)
                f = open("demofile2.txt", "a")
                f.write('\n' + ten_tinh + '-' + str(year) + '\n' + text)
                f.close()
            except:
                text = ''
                f = open("demofile2.txt", "a")
                f.write('\n' + ten_tinh + '-' + str(year) + '\n' + text)
                f.close()
            # #check điều kiện
            if year == 2023 and month == 5:
                break
data = open("demofile2.txt").read()
lines_of_data = data.splitlines()
filter_list = []

for line in lines_of_data:
    if "2021" in line:
      filter_list.append("2021")
    if "2022" in line:
      filter_list.append("2022")
    if "2023" in line:
      filter_list.append("2023")
    if len(line.split(' ')) == 3:
      filter_list.append(line)
print(filter_list[0])
spl = [list(y) for x, y in itertools.groupby(
    filter_list, lambda z: z == "2023" or z == "2022" or z == "2021") if not x]

spl2 = []

for s in spl:
  spl2.append([list(y) for x, y in itertools.groupby(
      s, lambda z: z == "Max Avg Min") if not x])

spl2[0][4][30]  # [bảng][cột][dòng] -> [month-1][value][day-1]
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["STT", "Province", "Date", "Max Temp", "Avg Temp", "Min Temp", "Max Dew Point", "Avg Dew Point", "Min Dew Point", "Max Humidity",
                    "Avg Humidity", "Min Humidity", "Max Wind Speed", "Avg Wind Speed", "Min Wind Speed", "Max Pressure", "Avg Pressure", "Min Pressure"])
    count = 0
    for tinh in list_tinh:
        for year in range(2021, 2024):
            for month in range(1, 13):
                if month == 6 and year == 2023:
                    break
                day_count = 30
                if month == 2:
                    day_count = 28
                if str(month) in ['1', '3', '5', '7', '8', '10', '12']:
                    day_count = 31
                for i in range(1, day_count+1):
                    count += 1
                    writer.writerow([count, tinh, str(year)+"/"+str(month)+"/"+str(i), spl2[month-1][0][i-1].split(" ")[0], spl2[month-1][0][i-1].split(" ")[1], spl2[month-1][0][i-1].split(" ")[2], spl2[month-1][1][i-1].split(" ")[0], spl2[month-1][1][i-1].split(" ")[1], spl2[month-1][1][i-1].split(" ")[2], spl2[month-1][2][i-1].split(" ")[0], spl2[month-1][2][i-1].split(" ")[1], spl2[month-1][2][i-1].split(" ")[2], spl2[month-1][3][i-1].split(" ")[0], spl2[month-1][3][i-1].split(" ")[1], spl2[month-1][3][i-1].split(" ")[2], spl2[month-1][4][i-1].split(" ")[0], spl2[month-1][4][i-1].split(" ")[1], spl2[month-1][4][i-1].split(" ")[2]])
