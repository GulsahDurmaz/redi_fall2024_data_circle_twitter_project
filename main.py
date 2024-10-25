# main.py
from imports import *
from data_loader import load_data  # Ensure you're importing load_data
from data_cleaning import clean_data

@st.cache_data  # Streamlit caching
def load_and_clean_data():
    trump_df = load_data(r"csv/hashtag_donaldtrump.csv")
    biden_df = load_data(r"csv/hashtag_joebiden.csv")

    # Clean data
    trump_df = clean_data(trump_df)
    biden_df = clean_data(biden_df)

    return trump_df, biden_df  # Return both DataFrames