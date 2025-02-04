from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    driver = webdriver.Chrome()
    driver.get('https://www.jib.co.th/web/product/product_search/0?str_search=&cate_id[]=42')
    time.sleep(5)
    
    try:
        accept_cookie = driver.find_element(By.XPATH, '/html/body/div[1]/div/a[1]')
        accept_cookie.click()
        time.sleep(2)
    except:
        pass  # ถ้าไม่มีปุ่ม cookie ก็ข้ามไป
    
    search = driver.find_element(By.XPATH, '//*[@id="productTitle"]')
    search.send_keys(query)
    search.send_keys(Keys.ENTER)
    time.sleep(2)
    
    driver.execute_script("document.body.style.transform = 'scale(0.1)';")
    driver.execute_script('document.body.style.transformOrigin = "0 0";')
    
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    records = []
    elements = soup.select("#body > div > div > div.row > div > div.panel > div.panel-body.panel_body_detail > div")
    
    for e in elements:
        name_elem = e.select_one("div > div > div:nth-child(4) > div > a > div > div > div > div > span")
        price_elem = e.select_one("div > div > div:nth-child(7) > div > div > div > div > div > div.col-md-6.col-sm-6.col-xs-6.pad-0.text-right > p")
        
        if name_elem and price_elem:
            name = name_elem.text.strip()
            price = price_elem.text.strip()
            records.append({'name': name, 'price': price})
    
    driver.quit()
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)

