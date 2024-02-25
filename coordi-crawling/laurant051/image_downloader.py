import csv, urllib.request, os, traceback
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


IMAGE_DIR = 'images'
URLS_CSV = 'urls.csv'
PRODUCT_CSV = 'products.csv'

up_label = ['jacket', 'cardigan', 'shirts', 'knit', 'blouson', 'coat', 'mtm', 'mustang', 'sleeves', 'padding', 'blazer', 'zip-up', 'jumper', 'kara', 'sleeveless', 'vest', 'hood', 'wind', 'jacekt', '%EC%85%94%EC%B8%A0', '%EB%A7%A8%ED%88%AC%EB%A7%A8', '%ED%8B%B0', '%ED%9B%84%EB%93%9C', 'ma']
down_label = ['pants', 'slacks', '%EC%8A%AC%EB%9E%99%EC%8A%A4', '%ED%8C%AC%EC%B8%A0', 'pans', 'jean']


options = webdriver.FirefoxOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
browser.set_page_load_timeout(5)
browser.set_script_timeout(5)

f = open(URLS_CSV, 'r')
urls_file = csv.reader(f)
f2 = open(PRODUCT_CSV, 'w', newline='')
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
for n, shopping_url in tqdm(data):
    
    classified = False
    
    for l in up_label:
        if l in shopping_url:
            position = 0
            classified = True
            break
    
    for l in down_label:
        if l in shopping_url:
            position = 1
            classified = True
            break
            
    if not classified:
        continue
    
    if try_get(browser, shopping_url, 10) == False:
        continue
    
    try:
        image_a = browser.find_elements(By.CLASS_NAME, 'group1')[0]
        img_url = image_a.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        product_file.writerow([index, position, img_url, shopping_url])
        
        image_path = os.path.join(IMAGE_DIR, f'{index}.jpg')
        urllib.request.urlretrieve(img_url, image_path)
        
        index += 1
        # print(image_path)
    except:
        print(f'index={index} error')
        traceback.print_exc()

f.close()
browser.close()
