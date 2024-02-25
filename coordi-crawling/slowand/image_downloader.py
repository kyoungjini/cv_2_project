import csv, urllib.request, os, traceback
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image

IMAGE_DIR = './images'
URLS_CSV = './urls.csv'
PRODUCT_CSV = './products.csv'

options = webdriver.FirefoxOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
browser.set_page_load_timeout(10)
browser.set_script_timeout(10)

urls_file = csv.reader(open(URLS_CSV, 'r'))
product_file = csv.writer(open(PRODUCT_CSV, 'w', newline=''))

def try_get(browser: WebDriver, url: str, n: int) -> bool:
    cnt = 0
    for _ in range(n):
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

for n, position, shopping_url in tqdm(data):
    if try_get(browser, shopping_url, 10) == False:
        continue
    
    try:
        img_url = browser.find_element(By.CSS_SELECTOR, '.detailArea .thumbnail img').get_attribute('src')
        product_file.writerow([index, position, img_url, shopping_url])
        
        image_path = os.path.join(IMAGE_DIR, f'{index}.jpg')
        urllib.request.urlretrieve(img_url, 'tmp.webp')
        im = Image.open('tmp.webp').convert('RGB')
        im.save(image_path, 'jpeg')
        
        index += 1
    except:
        print(f'index={index} error')
        traceback.print_exc()

browser.close()
