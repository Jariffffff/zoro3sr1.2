import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_daraz(query="headphones", pages=1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://www.daraz.com.bd/catalog/?q={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all("div", class_="gridItem--Yd0sa")
            for item in items:
                title = item.find("div", class_="title--wFj93")
                price = item.find("span", class_="price--NVB62")
                if title and price:
                    results.append({
                        "title": title.get_text(strip=True),
                        "price": int(price.get_text(strip=True).replace("৳", "").replace(",", "")),
                        "category": query.title(),
                        "source": "Daraz"
                    })
        except Exception as e:
            logging.error(f"Daraz error: {e}")
            continue
    return pd.DataFrame(results)

def scrape_pickaboo(query="headphones", pages=1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://www.pickaboo.com/search?q={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all("div", class_="product-details")
            for item in items:
                title = item.find("a", class_="product-title")
                price = item.find("span", class_="price")
                if title and price:
                    results.append({
                        "title": title.get_text(strip=True),
                        "price": int(price.get_text(strip=True).replace("৳", "").replace(",", "")),
                        "category": query.title(),
                        "source": "Pickaboo"
                    })
        except Exception as e:
            logging.error(f"Pickaboo error: {e}")
            continue
    return pd.DataFrame(results)

def scrape_rokomari(query="book", pages=1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://www.rokomari.com/book/search?term={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all("div", class_="book-list-wrapper")
            for item in items:
                title = item.find("p", class_="book-title")
                price = item.find("p", class_="book-price")
                if title and price:
                    results.append({
                        "title": title.get_text(strip=True),
                        "price": int(price.get_text(strip=True).replace("৳", "").replace(",", "")),
                        "category": query.title(),
                        "source": "Rokomari"
                    })
        except Exception as e:
            logging.error(f"Rokomari error: {e}")
            continue
    return pd.DataFrame(results)

def scrape_all(query: str, source: str = "daraz", pages: int = 1):
    if source == "daraz":
        return scrape_daraz(query, pages)
    elif source == "pickaboo":
        return scrape_pickaboo(query, pages)
    elif source == "rokomari":
        return scrape_rokomari(query, pages)
    else:
        raise ValueError(f"Unsupported source: {source}")
