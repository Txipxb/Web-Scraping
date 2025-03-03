from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


app = Flask(__name__)

def scrape_product(keyword: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    url = f"https://www.itcity.in.th/product-category/%E0%B8%AD%E0%B8%B8%E0%B8%9B%E0%B8%81%E0%B8%A3%E0%B8%93%E0%B9%8C%E0%B8%84%E0%B8%AD%E0%B8%A1%E0%B8%9E%E0%B8%B4%E0%B8%A7%E0%B9%80%E0%B8%95%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%AD%E0%B8%9A-(DIY)?search={keyword}"
    driver.get(url)
    

    driver.execute_script("document.body.style.transform = 'scale(0.1)';")
    driver.execute_script('document.body.style.transformOrigin = "0 0";')

    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')

    records = []
    elements = soup.select("#grid-content > div")

    for e in elements:
        name_elem = e.select_one("#grid-content > div > a > div > div > div.product-content.flex.flex-col.flex-1.px-\[9px\].pb-\[9px\].lg\:px-\[11px\].lg\:pb-\[11px\].px-\[9px\].pb-\[9px\].lg\:px-\[11px\].lg\:pb-\[11px\] > div.min-h-\[43px\]")
        price_elem = e.select_one("div.product-content > p.price")
        
        if name_elem and price_elem:
            records.append({
            'name': name_elem.text.strip(),
            'price': price_elem.text.strip()
        })
    
    driver.quit()
    return records

@app.route("/search_ITcity", methods=["GET"])
def search():
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    results = scrape_product(keyword)
    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
