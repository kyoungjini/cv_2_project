import urllib.request
import csv, time, platform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

URL = 'https://www.slowand.com'
IMAGE_DIR = './images'
CSV_FILE = './urls.csv'

url_file = open(CSV_FILE, 'w', newline='')
url_csv = csv.writer(url_file)

options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

browser.get(URL)
menus = browser.find_element(By.ID, 'category').find_elements(By.CSS_SELECTOR, 'a')

category = []
for menu in menus:
    if menu.text in ['TOP', 'SHIRT', 'KNIT', 'OUTER']:
        category.append((0, menu.get_attribute('href')))
    elif menu.text in ['BOTTOM']:
        category.append((1, menu.get_attribute('href')))
    
cnt = 0
for position, cate_url in category:
    print(cate_url)
    for page in range(1, 10000):
        browser.get(f'{cate_url}?page={page}')
        
        img_divs = browser.find_element(By.CSS_SELECTOR, 'main').find_elements(By.CLASS_NAME, 'prdImg')
        if len(img_divs) == 0: break
        for div in img_divs:
            a = div.find_element(By.CSS_SELECTOR, 'a')
            url_csv.writerow([cnt, position, a.get_attribute('href')])
            cnt += 1
        
        print(page)

browser.close()
url_file.close()