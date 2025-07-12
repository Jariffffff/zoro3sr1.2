import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
from .scraper.base import scrape_all

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_source_from_url(url: str):
    """Identifies the e-commerce source from a product URL."""
    if "daraz.com.bd" in url:
        return "daraz"
    elif "pickaboo.com" in url:
        return "pickaboo"
    elif "rokomari.com" in url:
        return "rokomari"
    else:
        return None

def scrape_product_page(url: str):
    """Scrapes the title and price from a single product page URL."""
    source = get_source_from_url(url)
    if not source:
        raise ValueError("Unsupported URL. Please use a valid Daraz, Pickaboo, or Rokomari URL.")

    try:
        res = requests.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title = None
        price = None

        if source == "daraz":
            # NOTE: These selectors are for product pages and may need adjustment.
            title_element = soup.find("span", class_="pdp-mod-product-badge-title")
            price_element = soup.find("span", class_="pdp-price")
            if title_element:
                title = title_element.get_text(strip=True)
            if price_element:
                price_text = price_element.get_text(strip=True).replace("৳", "").replace(",", "")
                if price_text.isdigit():
                    price = int(price_text)

        elif source == "pickaboo":
            # NOTE: These selectors are for product pages and may need adjustment.
            title_element = soup.find("h1", class_="product-title")
            price_element = soup.find("span", class_="price")
            if title_element:
                title = title_element.get_text(strip=True)
            if price_element:
                price_text = price_element.get_text(strip=True).replace("৳", "").replace(",", "")
                if price_text.isdigit():
                    price = int(price_text)

        elif source == "rokomari":
            # NOTE: These selectors are for product pages and may need adjustment.
            title_element = soup.find("h1", class_="details-book-main-title")
            price_element = soup.find("span", class_="details-book-info-price__value")
            if title_element:
                title = title_element.get_text(strip=True)
            if price_element:
                price_text = price_element.get_text(strip=True).replace("৳", "").replace(",", "")
                if price_text.isdigit():
                    price = int(price_text)
        
        if title:
            return {"title": title, "price": price, "source": source.title()}
        else:
            logging.warning(f"Could not find title for URL: {url}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping product page {url}: {e}")
        return None


def analyze_and_compare(url: str):
    """
    Analyzes a product from a URL and compares its price across all sources.
    """
    logging.info(f"Analyzing URL: {url}")
    original_product = scrape_product_page(url)

    if not original_product or not original_product.get("title"):
        logging.warning("Could not extract product title from the URL.")
        return pd.DataFrame()

    product_title = original_product["title"]
    logging.info(f"Extracted product title: {product_title}")

    # Now search for this title on all platforms
    daraz_results = scrape_all(query=product_title, pages=1, source='daraz')
    pickaboo_results = scrape_all(query=product_title, pages=1, source='pickaboo')
    rokomari_results = scrape_all(query=product_title, pages=1, source='rokomari')

    # Combine all results
    all_results = pd.concat([daraz_results, pickaboo_results, rokomari_results], ignore_index=True)
    
    return all_results
