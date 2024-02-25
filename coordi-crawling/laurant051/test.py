from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://laurant051.com/product/unisex-glossy-leather-padding-blouson2color/3449/category/24/display/1/'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Remote('http://localhost:4444', options=options)

browser.get(url)

group1 = browser.find_elements(By.CLASS_NAME, 'group1')

print(group1)

for el in group1:
    print(el.tag_name)


browser.close()
