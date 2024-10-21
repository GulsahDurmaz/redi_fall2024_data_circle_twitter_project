# app.py
from imports import *
import eda  # Import the Exploratory Data Analysis module
import world_popularity_analysis  # Import the World Popularity Analysis module
import us_popularity_analysis  # Import the US Popularity Analysis module
import dataset # Import the Dataset module


# Configure the Streamlit page
st.set_page_config(page_title="2020 US Presidential Election Dashboard",
                #    layout='wide',
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Apply custom styles
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('US Presidential Election Dashboard `2020`')

### Load the dataframes
@st.cache_data
def load_data(file):
    data = pd.read_csv(file, encoding='utf8', lineterminator='\n')
    
    # Converting date values (data type: object) to datetime format
    data['created_at'] = pd.to_datetime(data['created_at'])
    return data

trump_df = load_data(r"/Users/gulsah/Desktop/REDI/redi_fall2024_data_circle_twitter_project/csv/hashtag_donaldtrump.csv")
biden_df = load_data(r"/Users/gulsah/Desktop/REDI/redi_fall2024_data_circle_twitter_project/csv/hashtag_joebiden.csv")

# Clean data
trump_df = clean_data(trump_df)
biden_df = clean_data(biden_df)

# Initialize page state
if 'page' not in st.session_state:
    st.session_state.page = 'Exploratory Data Analysis'  # Default page

# Sidebar buttons for page navigation
if st.sidebar.button("Exploratory Data Analysis"):
    st.session_state.page = 'Exploratory Data Analysis'

if st.sidebar.button("World Popularity Analysis"):
    st.session_state.page = 'World Popularity Analysis'

if st.sidebar.button("US Popularity Analysis"):
    st.session_state.page = 'US Popularity Analysis'

if st.sidebar.button("Dataset"):
    st.session_state.page = 'Dataset'

# Display content based on the active page
if st.session_state.page == 'Exploratory Data Analysis':
    eda.run_exploratory_data_analysis(trump_df, biden_df)  # Call the function from eda.py

elif st.session_state.page == 'World Popularity Analysis':
    world_popularity_analysis.run_world_popularity_analysis(trump_df, biden_df)  # Call the function from world_popularity_analysis.py

elif st.session_state.page == 'US Popularity Analysis':
    us_popularity_analysis.run_us_popularity_analysis(trump_df, biden_df)  # Call the function from us_popularity_analysis.py

elif st.session_state.page == 'Dataset':
    dataset.run_dataset()

# Sidebar footer
st.sidebar.markdown('''
---
Created with ❤️ by [Gulsah Durmaz](https://github.com/GulsahDurmaz).
''')
