import csv, urllib.request, os, traceback
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

URLS_CSV = 'slowand.csv'
PRODUCT_CSV = 'slowand_with_title.csv'

options = webdriver.FirefoxOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
browser.set_page_load_timeout(5)
browser.set_script_timeout(5)

f = open(URLS_CSV, 'r')
urls_file = csv.reader(f)
f2 = open(PRODUCT_CSV, 'w', newline='', encoding='utf-8')
product_file = csv.writer(f2)


def try_get(browser: WebDriver, url: str, n: int) -> bool:
    cnt = 0
    for i in range(n):
        try:
            browser.get(url)
            break
        except:
            cnt += 1
            print(f'\nretry: {cnt}')
            if cnt >= n:
                return False
    return True


index = 0
data = list(urls_file)
for index, position, img_url, shopping_url in tqdm(data):

    if try_get(browser, shopping_url, 10) == False:
        continue

    try:
        title_text = browser.title.replace(" - 슬로우앤드", "")
        #print(title_text)
        product_file.writerow([index, position, img_url, shopping_url, title_text])
    except:
        print(f'index={index} error')
        traceback.print_exc()

f.close()
browser.close()
print("Complete")
