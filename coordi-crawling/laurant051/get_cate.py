import urllib.request
import csv, time, platform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

URL = 'https://laurant051.com/product/list.html'
# CATE_NO = map(str, range(80, 200))
CATE_NO = map(str, range(0, 200))
IMAGE_DIR = 'images'
CSV_FILE = 'urls.csv'

options = webdriver.FirefoxOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

available_cate = []

cnt = 0
for cate_no in CATE_NO:
    page = 1
    browser.get(f'{URL}?cate_no={cate_no}&page={page}')
    img_elements = browser.find_elements(By.CSS_SELECTOR, 'img')

    page_exists = False
    for img in img_elements:
        # print(img.get_property('class'))
        if img.get_attribute('class') == 'thumber_1':
            page_exists = True

    if not page_exists:
        print(f'cate_no={cate_no}, page={page} does not exist')
    else:
        print(f'cate_no={cate_no}, page={page}')
        available_cate.append(cate_no)

print(available_cate)
print(len(available_cate))
browser.close()