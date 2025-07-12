import pandas as pd
import os

HISTORY_FILE = 'zoro3sr-app/scrape_history.csv'

def save_scrape_history(df):
    """Appends a DataFrame to the history CSV file."""
    if os.path.exists(HISTORY_FILE):
        df.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(HISTORY_FILE, mode='w', header=True, index=False)

def load_scrape_history():
    """Loads the scrape history from the CSV file."""
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    else:
        return pd.DataFrame()
