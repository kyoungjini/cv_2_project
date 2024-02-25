from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

browser.get('https://dailyjou.com/product/%EB%AF%B8%EB%9D%BC%EB%B2%A8-%EC%85%94%EC%B8%A0-%EB%A0%88%EC%9D%B4%EC%96%B4%EB%93%9C-%EA%B0%80%EB%94%94%EA%B1%B4%EB%8B%88%ED%8A%B8-4-color/17142/category/25/display/1/')

url = browser.find_elements(By.CLASS_NAME, 'ThumbImage')[0].get_attribute('src')
print(url)


browser.close()