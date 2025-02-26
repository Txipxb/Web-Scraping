from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

driver = webdriver.Chrome()
driver.get('https://www.jib.co.th/web/product/product_search/0?str_search=&cate_id[]=42')
time.sleep(5)

accept_cookie = driver.find_element(By.XPATH,'/html/body/div[1]/div/a[1]')
accept_cookie.click()

search = driver.find_element(By.XPATH,'//*[@id="productTitle"]')
search.send_keys('lga1200')
search.send_keys(Keys.ENTER)
time.sleep(5)

driver.execute_script("document.body.style.transform = 'scale(0.1)';")
driver.execute_script('document.body.style.transformOrigin = "0 0";')


from bs4 import BeautifulSoup

data = driver.page_source
soup = BeautifulSoup(data, 'html.parser')


records=[]
el=soup.select("#body > div > div > div.row > div > div.panel > div.panel-body.panel_body_detail > div")

for e in el:
    name = e.select_one("#body > div > div > div.row > div > div.panel > div.panel-body.panel_body_detail > div > div > div:nth-child(4) > div > a > div > div > div > div > span").text.strip()
    price = e.select_one("#body > div > div > div.row > div > div.panel > div.panel-body.panel_body_detail > div > div > div:nth-child(7) > div > div > div > div > div > div.col-md-6.col-sm-6.col-xs-6.pad-0.text-right > p").text.strip()
    records.append([name,price])
    print(records)

driver.quit()