import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_daraz(query="headphones", pages=1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://www.daraz.com.bd/catalog/?q={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()  # Raise an exception for bad status codes
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
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping Daraz page {page}: {e}")
            continue # Continue to the next page
    return pd.DataFrame(results)

def scrape_pickaboo(query="headphones", pages=1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://www.pickaboo.com/search?q={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
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
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping Pickaboo page {page}: {e}")
            continue
    return pd.DataFrame(results)

def scrape_rokomari(query="book", pages=1):
    results = []
    for page in range(1, pages + 1):
        url = f"https://www.rokomari.com/book/search?term={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
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
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping Rokomari page {page}: {e}")
            continue
    return pd.DataFrame(results)

def scrape_startech(query="laptop", pages=1):
    results = []
    # Star Tech uses a POST request for search, which is more complex.
    # For simplicity, we will use their URL-based search.
    for page in range(1, pages + 1):
        url = f"https://www.startech.com.bd/product/search?search={query}&page={page}"
        try:
            res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all("div", class_="p-item")
            for item in items:
                title = item.find("h4", class_="p-item-name")
                price = item.find("div", class_="p-item-price")
                if title and price:
                    results.append({
                        "title": title.get_text(strip=True),
                        "price": int(price.get_text(strip=True).replace("৳", "").replace(",", "")),
                        "category": query.title(),
                        "source": "Star Tech"
                    })
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping Star Tech page {page}: {e}")
            continue
    return pd.DataFrame(results)

def scrape_all(query: str, source: str = "daraz", pages: int = 1):
    if source == "daraz":
        return scrape_daraz(query, pages)
    elif source == "pickaboo":
        return scrape_pickaboo(query, pages)
    elif source == "rokomari":
        return scrape_rokomari(query, pages)
    elif source == "startech":
        return scrape_startech(query, pages)
    else:
        raise ValueError(f"Unsupported source: {source}")
