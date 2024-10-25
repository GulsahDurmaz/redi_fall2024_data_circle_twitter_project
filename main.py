# main.py
from imports import *

trump_df = load_data(r"csv/hashtag_donaldtrump.csv")
biden_df = load_data(r"csv/hashtag_joebiden.csv")

# Clean data
trump_df = clean_data(trump_df)
biden_df = clean_data(biden_df)

# Create cleaned
trump_df.to_csv("csv/donaldtrump.csv", index=False)
biden_df.to_csv("csv/joebiden.csv", index=False)