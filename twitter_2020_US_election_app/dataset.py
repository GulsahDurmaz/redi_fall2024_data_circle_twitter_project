# dataset.py
from imports import *

def run_dataset():
    # Content
    st.markdown("## Content")
    st.markdown("""
    Tweets were collected using the Twitter API `statuses_lookup` and `snsscrape` for specific keywords. The original goal was to update the dataset daily to cover the period from **October 15 to November 4, 2020**.

    - **Added on November 6, 2020**: As the election events continue, I decided to keep updating the dataset until at least the end of November 6.
    - **Added on November 8, 2020**: One final version will include tweets up until the end of November 8.
    """)

    # Data Source and Acknowledgement
    st.markdown("## Data Source and Acknowledgement")
    st.markdown("""
    The data and content described here are originally from **MANCH HUI**'s Kaggle profile. This information was adapted from their dataset, and can be found at their [Kaggle profile](https://www.kaggle.com/manchunhui). All credit for the dataset collection and updates goes to them.



    You can download the dataset from [this](https://www.kaggle.com/datasets/manchunhui/us-election-2020-tweets/data) link.

    The dataset contains 21 features :

    | No  | Column Name          | Description                                              |
    |-----|----------------------|----------------------------------------------------------|
    | 1   | created_at           | Date and time of tweet creation                          |
    | 2   | tweet_id             | Unique ID of the tweet                                   |
    | 3   | tweet                | Full tweet text                                          |
    | 4   | likes                | Number of likes                                          |
    | 5   | retweet_count        | Number of retweets                                       |
    | 6   | source               | Utility used to post the tweet                           |
    | 7   | user_id              | User ID of tweet creator                                 |
    | 8   | user_name            | Username of tweet creator                                |
    | 9   | user_screen_name     | Screen name of tweet creator                             |
    | 10  | user_description     | Description of self by tweet creator                     |
    | 11  | user_join_date       | Join date of tweet creator                               |
    | 12  | user_followers_count | Followers count of tweet creator                         |
    | 13  | user_location        | Location given on tweet creator's profile                |
    | 14  | lat                  | Latitude parsed from user_location                       |
    | 15  | long                 | Longitude parsed from user_location                      |
    | 16  | city                 | City parsed from user_location                           |
    | 17  | country              | Country parsed from user_location                        |
    | 18  | state                | State parsed from user_location                          |
    | 19  | state_code           | State code parsed from user_location                     |
    | 20  | collected_at         | Date and time tweet data was mined from Twitter          |

    """)

    # Importing Libraries
    st.markdown("""
    # Importing Libraries

    Here we are using the following libraries:

    - **Pandas**: To load and manipulate the dataset efficiently as a DataFrame.
    - **NumPy**: For numerical operations and handling arrays.
    - **Matplotlib**: To create static, animated, and interactive visualizations, such as bar plots.
    - **Seaborn**: To create more sophisticated and aesthetically pleasing visualizations, such as correlation heatmaps, and to visualize relationships between features.
    - **Streamlit**: For building interactive web applications to showcase data analysis and visualizations.
    - **Plotly Express**: To create interactive visualizations like scatter plots and bar charts.
    - **NLTK (Natural Language Toolkit)**: Specifically, the `sent_tokenize` function is used to tokenize sentences, splitting the text into individual sentences.

    """)