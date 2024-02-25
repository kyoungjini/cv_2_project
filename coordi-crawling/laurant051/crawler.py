import urllib.request
import csv, time, platform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

URL = 'https://laurant051.com/product/list.html'
# CATE_NO = map(str, range(80, 200))
CATE_NO = [61] # All
IMAGE_DIR = 'images'
CSV_FILE = 'urls.csv'

url_file = open(CSV_FILE, 'w', newline='')
url_csv = csv.writer(url_file)

options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

cnt = 0
for cate_no in CATE_NO:
    for page in range(1, 200):
        browser.get(f'{URL}?cate_no={cate_no}&page={page}')
        img_elements = browser.find_elements(By.CSS_SELECTOR, 'img')

        page_exists = False
        for img in img_elements:
            # print(img.get_property('class'))
            if img.get_attribute('class') == 'thumber_1':
                page_exists = True
                img_url = img.get_attribute('src')
                a = img.find_element(By.XPATH, '..')
                url_csv.writerow([cnt, a.get_attribute('href')])
                print(f'{cnt}.jpg')
                cnt = cnt + 1 

        if not page_exists:
            print(f'cate_no={cate_no}, page={page} does not exist')
            break
        
        print(f'cate_no={cate_no}, page={page}')


browser.close()
url_file.close()