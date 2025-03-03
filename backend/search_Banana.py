from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_product(search_term):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.bnn.in.th/th/p/computer-hardware-diy?q=&ref=search-result')
    time.sleep(5)

    try:
        close_noti = driver.find_element(By.XPATH, '//*[@id="close-button-1573815308034"]/span')
        close_noti.click()
    except:
        pass

    try:
        accept_cookie = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/button[2]')
        accept_cookie.click()
    except:
        pass

    search = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/header[2]/div/div/section[1]/div/div/div/div[2]/div/input')
    search.send_keys(search_term)
    search.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.execute_script("document.body.style.transform = 'scale(0.1)';")
    driver.execute_script('document.body.style.transformOrigin = "0 0";')

    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')

    records = []
    elements = soup.select("#__layout > div > main > div > div.container > div > section.product-list-container > div.product-list > a")

    for e in elements:
        name_elem = e.select_one("div.product-item-details > div.product-name")
        price_elem = e.select_one("div.product-item-details > div.product-price")
        
        if name_elem and price_elem:
            name = name_elem.text.strip()
            price = price_elem.text.strip()
            records.append({'name': name, 'price': price})

    driver.quit()
    return records

@app.route('/search_Banana', methods=['GET'])
def search_route():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = search_product(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)