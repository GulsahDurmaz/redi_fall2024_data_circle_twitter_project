import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go  # Use graph_objs for custom traces
import pycountry
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
    'United States of America': 'United States',
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
usa_trump_df = trump_df[trump_df['country'] == 'United States']
usa_biden_df = biden_df[biden_df['country'] == 'United States']

# Count the number of tweets for each candidate (USA)
usa_trump_tweet_count = usa_trump_df.shape[0]
usa_biden_tweet_count = usa_biden_df.shape[0]
usa_total_tweet_count = usa_trump_tweet_count + usa_biden_tweet_count

# Percentage of Total Tweets (USA)
usa_trump_tweet_percentage = (usa_trump_tweet_count / usa_total_tweet_count) * 100
usa_biden_tweet_percentage = (usa_biden_tweet_count / usa_total_tweet_count) * 100

# Group by country and count tweets
trump_grouped = trump_df.groupby('country')['tweet'].count().reset_index(name='trump_grouped')
biden_grouped = biden_df.groupby('country')['tweet'].count().reset_index(name='biden_grouped')

# Merge the grouped DataFrames on 'country'
combined_df = pd.merge(trump_grouped, biden_grouped, on='country', how='outer')

# Fill NaN values with 0
combined_df.fillna(0, inplace=True)

# Convert tweet counts to integers
combined_df['trump_grouped'] = combined_df['trump_grouped'].astype(int)
combined_df['biden_grouped'] = combined_df['biden_grouped'].astype(int)

# Total counts
combined_df['total_tweet_count'] = combined_df['trump_grouped'] + combined_df['biden_grouped']

combined_df['trump_percentage'] = (combined_df['trump_grouped'] / combined_df['total_tweet_count'] * 100).round(2)
combined_df['biden_percentage'] = (combined_df['biden_grouped'] / combined_df['total_tweet_count'] * 100).round(2)

# Sort top 10 countries
combined_df = combined_df.sort_values(by='total_tweet_count', ascending=False)

# Function to get ISO Alpha-3 country code
def get_country_code(country_name):
    try:
        # Use pycountry to get the country object
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None  # If the country name is not found, return None

# Apply the function to the 'country' column to create a new 'country_code' column
combined_df['country_code'] = combined_df['country'].apply(get_country_code)

# Define a mapping for the missing country codes
missing_country_codes = {
    'Turkey': 'TUR',
    'Russia': 'RUS',
    'Jamaika': 'JAM',
    'Palestinian Territory': 'PSE',
    'Kosovo': 'XKX',  # Kosovo is often represented with 'XKX'
    'The Bahamas': 'BHS',
    'The Gambia': 'GMB',
    'Congo-Brazzaville': 'COG',
    'Vatican City': 'VAT',
    'Falkland Islands': 'FLK',
    'Democratic Republic of the Congo': 'COD',
    'Cape Verde': 'CPV',
    'East Timor': 'TLS'
}

# Fill in the missing country codes
combined_df['country_code'] = combined_df.apply(
    lambda row: missing_country_codes.get(row['country'], row['country_code']),
    axis=1
)

# USA  top 10 state analysis
usa_trump_grouped = usa_trump_df.groupby('state_code')['tweet'].count()
usa_biden_grouped = usa_biden_df.groupby('state_code')['tweet'].count()

usa_combined_df = pd.merge(usa_trump_grouped, usa_biden_grouped, on='state_code', how='outer')
usa_combined_df = usa_combined_df.rename(columns={'tweet_x': 'trump_tweets', 'tweet_y': 'biden_tweets'})
usa_combined_df = usa_combined_df.reset_index()
usa_combined_df = pd.merge(usa_combined_df, usa_biden_grouped, on='state_code', how='outer')

# NaN fill with  0
usa_combined_df['trump_tweets'].fillna(0, inplace=True)

usa_combined_df['trump_tweets'] = usa_combined_df['trump_tweets'].astype(int)

usa_combined_df['total_tweets'] = usa_combined_df['trump_tweets'] + usa_combined_df['biden_tweets']
usa_combined_df['total_tweets_overall'] = usa_combined_df['trump_tweets'].sum() + usa_combined_df['biden_tweets'].sum()

usa_combined_df['trump_percentage'] = (usa_combined_df['trump_tweets'] / usa_combined_df['total_tweets'] * 100).round(2)
usa_combined_df['biden_percentage'] = (usa_combined_df['biden_tweets'] / usa_combined_df['total_tweets'] * 100).round(2)

usa_combined_df['usa_percentage_total'] = (usa_combined_df['total_tweets'] / usa_combined_df['total_tweets_overall'] * 100).round(2)

usa_combined_df = usa_combined_df.sort_values(by='total_tweets', ascending=False)
usa_combined_df.head(10)

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
        conclusion = f"""
            <div style='text-align: justify;'>
                In the USA dataset, tweet activity peaks between 01:00-02:00 AM, which could be related to
                post-event discussions, late-night media coverage, or breaking news updates. These hours often
                see active conversations around political events such as debate reactions or campaign
                announcements, especially when critical moments occur late in the evening.  
            </div>
        """
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

    # Additional Conclusion Section
    conclusion = f"""
        <div style='text-align: justify;'>
            In the global dataset, tweet activity shows a significant spike between 16:00-17:00, marking the
            first time that Joe Biden's tweet volume surpasses Donald Trump's. This time window likely
            corresponds to moments when people worldwide are active on social media, particularly in the late
            afternoon or after work hours. 
        </div>
    """

    # Display the conclusion
    st.markdown(conclusion, unsafe_allow_html=True)

    # Adding space between the paragraph and the chart
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Streamlit select slider to select between 'Global' and 'USA'
    view4 = st.select_slider('Select View', options=['Global.map', 'USA.map'])

    # Filter data based on the selected view
    if view4 == "USA.map": 
            # Calculate the color mapping based on the percentage difference
        usa_combined_df['color'] = usa_combined_df['trump_percentage'] - usa_combined_df['biden_percentage']

        # Create a choropleth map
        fig = px.choropleth(
            usa_combined_df,
            locationmode='USA-states',
            locations='state_code',
            color='color',
            color_continuous_scale=[(1, 'red'), (0, 'blue')],
            range_color=[-100, 100],  # Adjust this range based on your data
            scope="usa",
            title='Biden vs Trump Tweet Percentages by State',
            hover_name='state_code',  # Show the state code on hover
            hover_data={
                'trump_percentage': True,  # Display Trump percentage
                'biden_percentage': True,   # Display Biden percentage
                'color': False              # Do not display the difference
            }
        )
        # Update layout for better visualization with a transparent background
        fig.update_layout(
            title_font=dict(size=16, color='white'),
            paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to transparent
            geo=dict(bgcolor='rgba(255, 255, 255, 0)'),  # Set geo background color to transparent
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else: 
        # Calculate color mapping based on percentage difference
        combined_df['color'] = combined_df['trump_percentage'] - combined_df['biden_percentage']

        # Create a choropleth map
        fig = px.choropleth(
            combined_df,
            locations='country_code',  # Column with country ISO Alpha-3 codes
            color='color',  # Column for the color scale
            color_continuous_scale=[(1, 'red'), (0, 'blue')],
            range_color=[-100, 100],  # Adjust based on your data
            scope="world",  # Display the entire world
            title='Biden vs Trump Tweet Percentages by Country',
            hover_name='country_code',  # Show the country code on hover
            hover_data={
                'trump_percentage': True,  # Display Trump percentage
                'biden_percentage': True,  # Display Biden percentage
                'color': False  # Do not display the difference
            }
        )

        # Update layout for better visualization
        fig.update_geos(showcoastlines=True, coastlinecolor="Gray", showland=True, landcolor="white")

        # Update layout for better visualization with a transparent background
        fig.update_layout(
            title_font=dict(size=16, color='white'),
            paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to transparent
            geo=dict(bgcolor='rgba(255, 255, 255, 0)'),  # Set geo background color to transparent
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    # Adding space between the paragraph and the chart
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Streamlit select slider to select between 'Global' and 'USA'
    view5 = st.select_slider('Select View', options=['Global.chart', 'USA.chart'])

    # Filter data based on the selected view
    if view5 == "USA.chart":
        # Get the top 10 states based on total tweet counts
        top_states = usa_combined_df.head(10)

        # Set the position of bars on the x-axis
        bar_width = 0.25
        x = range(len(top_states))

        # Create a figure for the bar chart
        plt.figure(figsize=(12, 6))

        # Plot Trump tweets
        plt.bar(x, top_states['trump_tweets'], width=bar_width, label='Trump Tweets', color='red', align='center')

        # Plot Biden tweets
        plt.bar([p + bar_width for p in x], top_states['biden_tweets'], width=bar_width, label='Biden Tweets', color='blue', align='center')

        # Plot Total tweets
        plt.bar([p + bar_width*2 for p in x], top_states['total_tweets'], width=bar_width, label='Total Tweets', color='gray', align='center')

        # Adding labels and title
        plt.xlabel('State', fontsize=14, color='white')
        plt.ylabel('Tweet Count', fontsize=14, color='white')
        plt.title('Top 10 States Tweet Counts: Trump vs Biden vs Total', fontsize=16, color='white', weight='bold')
        plt.xticks([p + bar_width for p in x], top_states['state_code'], rotation=45, color='white')
        plt.legend(facecolor='white', fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)  # Add gridlines

        # Change tick values to white
        plt.tick_params(axis='x', colors='white')  # X-axis ticks
        plt.tick_params(axis='y', colors='white')  # Y-axis ticks

        # Streamlit display
        st.pyplot(plt, transparent=True)

        # Clear the figure after displaying
        plt.clf()

    else:
        # The top 10 countries based on total tweet counts
        top_countries = combined_df.head(10)

        # Set the position of bars on the x-axis
        bar_width = 0.25
        x = range(len(top_countries))

        # Create a figure for the bar chart
        plt.figure(figsize=(12, 6))

        # Plot Trump tweets
        plt.bar(x, top_countries['trump_grouped'], width=bar_width, label='Trump Tweets', color='red', align='center')

        # Plot Biden tweets
        plt.bar([p + bar_width for p in x], top_countries['biden_grouped'], width=bar_width, label='Biden Tweets', color='blue', align='center')

        # Plot Total tweets
        plt.bar([p + bar_width*2 for p in x], top_countries['total_tweet_count'], width=bar_width, label='Total Tweets', color='gray', align='center')

        # Adding labels and title
        plt.xlabel('Country', fontsize=14, color='white')
        plt.ylabel('Tweet Count', fontsize=14, color='white')
        plt.title('Top 10 Countries Tweet Counts: Trump vs Biden vs Total', fontsize=16, color='white', weight='bold')
        plt.xticks([p + bar_width for p in x], top_countries['country'], rotation=45, color='white')
        plt.legend(facecolor='white', fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)  # Add gridlines

        # Change tick values to white
        plt.tick_params(axis='x', colors='white')  # X-axis ticks
        plt.tick_params(axis='y', colors='white')  # Y-axis ticks

        # Streamlit display
        st.pyplot(plt, transparent=True)

        # Clear the figure after displaying
        plt.clf()

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