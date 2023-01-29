# Download driver from https://chromedriver.chromium.org/
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

#keeps browser open
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


#chose chromedriver directory and web page url
s = Service('C:/Users/Димитрий/Desktop/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)
# driver.get('https://yandex.ru/maps/org/mkafe/230094363823/reviews/?ll=39.863270%2C47.300535&z=15')
driver.get('https://yandex.ru/maps/org/mkafe/197803051070/reviews/?ll=35.065454%2C57.172989')
sleep(3)

WebDriverWait(driver, 150)
review_block = driver.find_element(By.CSS_SELECTOR, ".business-reviews-card-view__reviews-container")
WebDriverWait(driver, 150)

while True:
    review_list = review_block.find_elements(By.CSS_SELECTOR, ".business-review-view__body-text")
    sleep(7)
    n = 0
    for i in review_list:
        # print("__________")
        n+=1
        driver.execute_script("arguments[0].scrollIntoView();", review_list[n-1])
        print(n)
    if n == 600:
        break

sleep(2)
source_data = driver.page_source
soup = BeautifulSoup(source_data, 'html.parser')
data = []
reviews_selector = soup.find_all('div', class_='business-review-view__info')
# print(reviews_selector)

for i in reviews_selector:
    date = i.find('span', class_='business-review-view__date').text
    name = i.find('div', class_='business-review-view__author').find('span').text
    txt = i.find('span', class_='business-review-view__body-text').text
    try:
        rating = i.find('div', class_='business-review-view__rating').find('meta', itemprop="ratingValue").attrs
    except AttributeError:
        continue

    data.append([date.strip(), name.strip(), rating.get('content'), txt.strip()])

print(data)


#put data to CSV
header = ['date', 'name', 'rating', 'txt']
df = pd.DataFrame(data, columns=header)
df.to_csv('D:\MyPython\PinterestScraper\Yandex_Reviews_Parser.csv', sep=';', encoding='cp1251', errors="ignore")