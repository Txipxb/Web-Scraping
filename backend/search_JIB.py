from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

def search_product(search_term):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.jib.co.th/web/product/product_search/0?str_search=&cate_id[]=42')
    time.sleep(5)

    try:
        accept_cookie = driver.find_element(By.XPATH, '/html/body/div[1]/div/a[1]')
        accept_cookie.click()
        time.sleep(2)
    except:
        pass  

    search = driver.find_element(By.XPATH, '//*[@id="productTitle"]')
    search.send_keys(search_term)
    search.send_keys(Keys.ENTER)
    time.sleep(5)

    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')

    records = []
    elements = soup.select("#body > div > div > div.row > div > div.panel > div.panel-body.panel_body_detail > div")

    for e in elements:
        name_elem = e.select_one("div > div > div:nth-child(4) > div > a > div > div > div > div > span")
        price_elem = e.select_one("div > div > div:nth-child(7) > div > div > div > div > div > div.col-md-6.col-sm-6.col-xs-6.pad-0.text-right > p")
        img_elem = e.select_one("div > div > div.row > div > div.panel > div.panel-body.panel_body_detail > div > div > div > div > a > img")
        link_elem = e.select_one("div > div > div:nth-child(4) > div > a")
        

        if name_elem and price_elem and img_elem and link_elem:
            name = name_elem.text.strip()
            price = price_elem.text.strip()
            img_url = img_elem.get('src', '').strip()
            product_url = link_elem.get('href', '').strip()
            
            if img_url.startswith("/"):
                img_url = "https://www.jib.co.th" + img_url

            if img_url and product_url:
                records.append({
                    'name': name,
                    'price': price,
                    'image_url': img_url,
                    'product_url': product_url
                })
    
    driver.quit()
    return records

@app.route('/search_JIB', methods=['GET'])
def search_route():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = search_product(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)