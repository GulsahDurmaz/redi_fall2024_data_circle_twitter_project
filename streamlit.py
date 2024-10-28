import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pycountry
import streamlit as st

from data_loader import *

# Configure the Streamlit page
st.set_page_config(page_title="2020 US Presidential Election Dashboard",
                #    layout='wide',
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

def main():
    st.title("My Streamlit App")
    st.write("Hello, world!")

if __name__ == "__main__":
    main()

biden_df = load_data(r"csv/joebiden.csv")

st.dataframe(biden_df.head(3))