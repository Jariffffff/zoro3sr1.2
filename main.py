import streamlit as st
import pandas as pd
import os
from scraper import scrape_all, analyze_and_compare

st.set_page_config(layout="wide", page_title="Zoro3sr Product Scraper", page_icon="🛒")

st.title("🛒 Zoro3sr Multi-Source Product Scraper & Analyzer")
st.markdown("---")

# --- Main Layout with Columns ---
col1, col2 = st.columns(2)

with col1:
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
            except Exception as e:
                st.error(f"❌ Error: {e}")

with col2:
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
