import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from nltk.tokenize import sent_tokenize

# Configure the Streamlit page
st.set_page_config(page_title="2020 US Presidental Election Dashboard", 
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

    
# Load the dataframes
@st.cache_data
def load_data(file):
    data = pd.read_csv(file, encoding='utf8', lineterminator='\n')
    
    # Converting date values (data type: object) to datetime format
    data['created_at'] = pd.to_datetime(data['created_at'])
    
    return data

trump_df = load_data(r"/Users/gulsah/Desktop/REDI/redi_fall2024_data_circle_twitter_project/csv/hashtag_donaldtrump.csv")
biden_df = load_data(r"/Users/gulsah/Desktop/REDI/redi_fall2024_data_circle_twitter_project/csv/hashtag_joebiden.csv")

# drop non necesssary columns
trump_df = trump_df.drop(columns= ['tweet_id', 'lat', 'long', 'continent'])
biden_df = biden_df.drop(columns= ['tweet_id', 'lat', 'long', 'continent'])

# combine 'United States of America' and 'United States'
country_mapping = {
    'United States of America': 'USA',
    'United States': 'USA'
}
trump_df['country'] = trump_df['country'].replace(country_mapping)
biden_df['country'] = biden_df['country'].replace(country_mapping)

# combine 'The Netherlands', 'Netherlands'

country_mapping2 = {
    'The Netherlands': 'Netherlands',
}
trump_df['country'] = trump_df['country'].replace(country_mapping2)
biden_df['country'] = biden_df['country'].replace(country_mapping2)

# Count the number of tweets for each candidate (Global)
trump_tweet_count = trump_df.shape[0]
biden_tweet_count = biden_df.shape[0]
total_tweet_count = trump_tweet_count + biden_tweet_count

# Percentage of Total Tweets (Global)
trump_tweet_percentage = (trump_tweet_count / total_tweet_count) * 100
biden_tweet_percentage = (biden_tweet_count / total_tweet_count) * 100

# Create a new DataFrame with only USA data
usa_trump_df = trump_df[trump_df['country'] == 'USA']
usa_biden_df = biden_df[biden_df['country'] == 'USA']

# Count the number of tweets for each candidate (USA)
usa_trump_tweet_count = usa_trump_df.shape[0]
usa_biden_tweet_count = usa_biden_df.shape[0]
usa_total_tweet_count = usa_trump_tweet_count + usa_biden_tweet_count

# Percentage of Total Tweets (USA)
usa_trump_tweet_percentage = (usa_trump_tweet_count / usa_total_tweet_count) * 100
usa_biden_tweet_percentage = (usa_biden_tweet_count / usa_total_tweet_count) * 100

# Sidebar menu
option = st.sidebar.selectbox("Select a feature", ["Homepage", "Exploratory Data Analysis", "Content & Data", "Key Word in Context"])

if option == "Homepage":
    # Informative Markdown Sections (Preserved Exactly)
    st.markdown("# US Election 2020 Tweets Analysis")

    # Context
    st.markdown("""
    The 2020 United States presidential election was held on **November 3, 2020**. The major candidates were incumbent 
    Republican President Donald Trump and Democratic former Vice President Joe Biden. In the months leading up to the 
    election, social media played a significant role in shaping public opinion, with platforms like Twitter serving as a 
    key battleground for discussions, endorsements, and criticism.
    """)

    # Why Twitter?
    st.markdown("## Why Twitter?")
    st.markdown("""
    Social media platforms like Facebook and Twitter have transformed how we interact and share news. As of June 2019, Twitter had over 348M users posting 500M tweets daily, enabling users to influence trends and shape news coverage.

    Twitter has become increasingly important in electoral campaigning, with politicians and parties actively using the platform. This rise in political activity on Twitter has attracted researchers' interest, making election prediction based on Twitter data a popular field. Researchers now analyze citizen sentiment to estimate candidate performance in elections ([Garcia et al., 2019](https://dl.acm.org/doi/pdf/10.1145/3339909)).
    """)

elif option == "Exploratory Data Analysis":
    # Set the page title
    st.title("2020 US Presidental Election")

    # Streamlit radio button to select between 'Global' and 'USA'
    #view = st.radio("Select View", ["Global", "USA"])
    view = st.select_slider('Select View', options=['Global.1', 'USA.1'])

    # Filter data based on the selected view
    if view == "USA.1":  # USA View
        trump_tweet_percentage = usa_trump_tweet_percentage
        biden_tweet_percentage = usa_biden_tweet_percentage
        trump_tweet_count = usa_trump_tweet_count
        biden_tweet_count = usa_biden_tweet_count
        total_tweets = usa_total_tweet_count
    else:  # Global View
        trump_tweet_percentage = trump_tweet_percentage
        biden_tweet_percentage = biden_tweet_percentage
        trump_tweet_count = trump_tweet_count
        biden_tweet_count = biden_tweet_count
        total_tweets = total_tweet_count

    # Prepare data for the bar chart
    popularity_data_percentage = pd.DataFrame({
        'Candidates': ['Donald Trump', 'Joe Biden'],
        'Tweet Percentage': [trump_tweet_percentage, biden_tweet_percentage]
    })

    # Plot the bar chart
    fig1 = px.bar(popularity_data_percentage, 
                x='Candidates', 
                y='Tweet Percentage', 
                title=f"Twitter Popularity % - Trump vs Biden ({view})",
                labels={'Tweet Percentage': 'Tweet %', 'Candidates': 'Candidates'},
                color='Candidates',
                color_discrete_map={'Donald Trump': 'red', 'Joe Biden': 'blue'})

    fig1.update_layout(title_x=0.25)
    # Display the chart in Streamlit
    st.plotly_chart(fig1)

    # Additional Conclusion Section
    # Dynamically update the conclusion based on the selected view
    conclusion = f"""
        <div style='text-align: justify;'>
            This bar chart reveals important insights into the relative popularity of Donald Trump and
            Joe Biden on Twitter during the 2020 U.S. presidential election. A total of {total_tweets} tweets 
            were recorded, with {trump_tweet_count} tweets using the Trump hashtag and {biden_tweet_count} 
            tweets associated with the Biden hashtag. These figures indicate the level of public interest and the extent
            of discussions surrounding each candidate's campaign in the **{view}** dataset.
        </div>
    """

    # Display the conclusion
    st.markdown(conclusion, unsafe_allow_html=True)

    # Streamlit select slider to select between 'Global' and 'USA'
    view2 = st.select_slider('Select View', options=['Global.2', 'USA.2'])

    # Filter data based on the selected view
    if view2 == "USA.2":  # USA View
        t_tweets_per_day = usa_trump_df.groupby(trump_df['created_at'].dt.date).size()
        b_tweets_per_day = usa_biden_df.groupby(biden_df['created_at'].dt.date).size()
    else:  # Global View
        t_tweets_per_day = trump_df.groupby(trump_df['created_at'].dt.date).size()
        b_tweets_per_day = biden_df.groupby(biden_df['created_at'].dt.date).size()

    # Plotting
    plt.figure(figsize=(14, 7), facecolor='black')
    plt.plot(t_tweets_per_day.index, t_tweets_per_day.values, label='Trump', color='red', linewidth=2)
    plt.plot(b_tweets_per_day.index, b_tweets_per_day.values, label='Biden', color='blue', linewidth=2)
    plt.xlabel('Date', color='white', fontsize=14)
    plt.ylabel('Tweet Counts', color='white', fontsize=14)
    plt.title(f'Daily Tweet Counts About - Trump vs. Biden ({view2})', color='white', fontsize=16, fontweight='bold')
    plt.legend(facecolor='white', fontsize=10)
    plt.xticks(rotation=90, color='white', fontsize=10)
    plt.yticks(color='white', fontsize=10)
    plt.gca().set_xticks(t_tweets_per_day.index)
    plt.gca().set_xticklabels(t_tweets_per_day.index, rotation=90)
    plt.grid(color='grey', linestyle='--', linewidth=0.5)

    # Display the plot in Streamlit
    st.pyplot(plt, transparent=True)

    # Additional Conclusion Section
    st.markdown("""
        <p style='text-align: justify;'>
            The spikes in tweet activity on <strong>October 23</strong>, <strong>November 4</strong>, and <strong>November 7</strong>, 2020, reflect pivotal
            moments in the 2020 U.S. presidential election. The October 23 spike corresponded to the final
            debate between Donald Trump and Joe Biden, which significantly engaged voters on social media.
            The peak on November 4 occurred the day after the election as results began to unfold, prompting
            widespread discussion. Finally, the surge on November 7 followed the announcement of Joe Biden's
            victory, highlighting the mass mobilization of public sentiment on Twitter.
        </p>
    """, unsafe_allow_html=True)

    # Adding space between the paragraph and the chart
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Streamlit select slider to select between 'Global' and 'USA'
    view3 = st.select_slider('Select View', options=['Global.3', 'USA.3'])

    # Filter data based on the selected view
    if view3 == "USA.3":  # USA View
        trump_df['tweet_hour'] = usa_trump_df['created_at'].dt.hour
        biden_df['tweet_hour'] = usa_biden_df['created_at'].dt.hour
    else:  # Global View
        trump_df['tweet_hour'] = trump_df['created_at'].dt.hour
        biden_df['tweet_hour'] = biden_df['created_at'].dt.hour

   # Create a new figure for Streamlit
    fig2, ax = plt.subplots(figsize=(12, 6), facecolor='black')  # Set the background to black

    # Plotting histograms for Trump and Biden
    sns.histplot(trump_df['tweet_hour'], bins=24, kde=False, color='red', label='Trump', alpha=0.8, ax=ax)
    sns.histplot(biden_df['tweet_hour'], bins=24, kde=False, color='blue', label='Biden', alpha=0.7, ax=ax)

    # Set titles and labels with specified font sizes
    ax.set_title(f'Distribution of Tweets by Hour - Trump vs Biden ({view3})', color='white', fontsize=16, fontweight='bold')
    ax.set_xlabel('Hour of Day (0-23)', color='white', fontsize=14)
    ax.set_ylabel('Tweet Count', color='white', fontsize=14)
    ax.set_xticks(range(0, 24))  # Show all hours on the x-axis
    ax.legend(facecolor='white', fontsize=10)  # Show the legend to distinguish Trump and Biden
    ax.grid(color='grey', linestyle='--', linewidth=0.5)  # Add gridlines

    # Change tick values to white
    ax.tick_params(axis='x', colors='white')  # X-axis ticks
    ax.tick_params(axis='y', colors='white')  # Y-axis ticks

    # Display the plot in Streamlit
    st.pyplot(fig2, transparent=True)


elif option == "Content & Data":
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