import streamlit as st
import pandas as pd
import os
from scraper.base import scrape_all
from scraper import analyze_and_compare
from auth import check_credentials
from history import save_scrape_history, load_scrape_history

st.set_page_config(layout="wide", page_title="Zoro3sr Product Scraper", page_icon="🛒")

def login_screen():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state['logged_in'] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def main_app():
    st.title("🛒 Zoro3sr Multi-Source Product Scraper & Analyzer")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Scraper", "Analyzer", "History"])

    with tab1:
        st.header("1. Scrape by Keyword")
        query = st.text_input("Enter search query", value="laptop")
        # Add new source to the list
        source = st.selectbox("Select source", options=["daraz", "pickaboo", "rokomari", "startech"])
        pages = st.number_input("Pages to scrape", min_value=1, max_value=5, value=1)

        if st.button("Scrape Products"):
            with st.spinner(f"Scraping {pages} page(s) from {source}..."):
                try:
                    df = scrape_all(query, source, pages)
                    if df.empty:
                        st.warning("No results found.")
                    else:
                        st.success(f"✅ Found {len(df)} results from {source.title()}.")
                        st.dataframe(df)
                        save_scrape_history(df)
                        
                        # --- CSV Download Button ---
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download results as CSV",
                            data=csv,
                            file_name=f'{source}_{query}_scrape_results.csv',
                            mime='text/csv',
                        )
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab2:
        st.header("2. Analyze from Product Link")
        product_url = st.text_input("Enter a product URL to compare")

        if st.button("Analyze and Save"):
            if not product_url:
                st.warning("Please enter a product URL.")
            else:
                with st.spinner("Analyzing link and comparing across other sites..."):
                    try:
                        # This function needs to be added to scraper.py
                        comparison_df = analyze_and_compare(product_url)
                        if comparison_df.empty:
                            st.warning("Could not find the product or any comparisons.")
                        else:
                            st.success("✅ Analysis complete! Found the following results:")
                            st.dataframe(comparison_df)

                            # Save to CSV
                            csv_path = "analysis_history.csv"
                            if os.path.exists(csv_path):
                                comparison_df.to_csv(csv_path, mode='a', header=False, index=False)
                            else:
                                comparison_df.to_csv(csv_path, mode='w', header=True, index=False)
                            
                            st.success(f"Results appended to `{csv_path}`")

                    except Exception as e:
                        st.error(f"❌ An error occurred during analysis: {e}")
    
    with tab3:
        st.header("Scrape History")
        history_df = load_scrape_history()
        if not history_df.empty:
            st.dataframe(history_df)
        else:
            st.info("No scrape history found.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
