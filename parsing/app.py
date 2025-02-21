import requests
from bs4 import BeautifulSoup
import json
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def scrape_product_data(url, product_id):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            category_tag = soup.find("span", class_=lambda x: x and x.startswith("ProductLink_"))
            category = category_tag["data-category"].split("|")[0] if category_tag and "data-category" in category_tag.attrs else "N/A"
            name = category_tag["data-name"] if category_tag and "data-name" in category_tag.attrs else "N/A"
            price_tag = soup.find("span", id="pricing")
            price = price_tag["content"] if price_tag and "content" in price_tag.attrs else "N/A"
            return {
                "id": product_id,
                "category": category,
                "name": name,
                "price": f"${price}" if price != "N/A" else "N/A",
                "url": url
            }
        else:
            print(f"Failed to fetch the page: {url} (Status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return None

if __name__ == "__main__":
    input_file = "generated_urls.json"
    output_file = "product_data.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        urls = data.get("urls", [])

    product_data = []
    product_id = 1

    for url in urls:
        product = scrape_product_data(url, product_id)
        if product:
            product_data.append(product)
            product_id += 1
        delay = random.uniform(2, 5)
        print(f"Waiting {delay:.2f} seconds before next request...")
        time.sleep(delay)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)

    print(f"Scraping completed. {len(product_data)} valid products saved to {output_file}.")
