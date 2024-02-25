import urllib.request
import csv, time, platform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

URL = 'https://dailyjou.com/product/list.html'
CATE_NO = [25, 26, 27, 28]
IMAGE_DIR = 'dailyjou'
CSV_FILE = 'urls.csv'

url_file = open(CSV_FILE, 'w', newline='')
url_csv = csv.writer(url_file)

options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

cnt = 0
for cate_no in CATE_NO:
    print(f'cate_no={cate_no}')
    for page in range(1, 10000):
        
        position = 1 if cate_no == 27 else 0
        
        browser.get(f'{URL}?cate_no={cate_no}&page={page}')

        imgs = browser.find_elements(By.CSS_SELECTOR, '.grid4 img')
        if len(imgs) == 0: break
        
        for img in imgs:
            if not 'PrdImage' in img.get_attribute('id'): continue
            shopping_url = img.find_element(By.XPATH, '..').get_attribute('href')
            url_csv.writerow([cnt, position, shopping_url])
            cnt += 1
        
        print(f'page={page}')


browser.close()
url_file.close()