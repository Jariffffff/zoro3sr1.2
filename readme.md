# Zoro3sr Multi-Source Product Scraper

🛒 Scrape and analyze products from Daraz, Pickaboo, Rokomari, and Star Tech using a Streamlit UI.

## Features
- **Keyword Search**: Scrape products by keyword from four different e-commerce sites.
- **URL Analyzer**: Paste a product link to find its title and then search for it on all other sites for price comparison.
- **Save Results**: The results of every URL analysis are automatically saved to `analysis_history.csv`.

## Supported Sources
- Daraz
- Pickaboo
- Rokomari
- Star Tech

## Usage
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the app:**
    ```bash
    streamlit run main.py
    ```

## Deployment
This app can be easily deployed to [Streamlit Cloud](https://streamlit.io/cloud).
