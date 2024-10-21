# world_popularity_analysis.py
from imports import *

def run_world_popularity_analysis(trump_df, biden_df):

    st.subheader("World Popularity Analysis")
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
    # Sort top 10 countries
    combined_df = combined_df.sort_values(by='total_tweet_count', ascending=False)
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
    # plt.title('Top 10 Countries Tweet Counts: Trump vs Biden vs Total', fontsize=16, color='white', weight='bold')
    plt.xticks([p + bar_width for p in x], top_countries['country'], rotation=90, color='white')
    plt.legend(facecolor='white', fontsize=10)
    plt.grid(color='grey', linestyle='--', linewidth=0.5)  # Add gridlines
    # Change tick values to white
    plt.tick_params(axis='x', colors='white')  # X-axis ticks
    plt.tick_params(axis='y', colors='white')  # Y-axis ticks
    # Streamlit display
    st.pyplot(plt, transparent=True)
    # Clear the figure after displaying
    plt.clf()

    unique_countries = sorted(list(set(trump_df['country'].unique()) | set(biden_df['country'].unique())))
    selected_country = st.selectbox('Select country', unique_countries)

    # Calculate percentage for selected country
    trump_percentage, biden_percentage = calculate_percentage(trump_df, biden_df, selected_country)

    # Calculate global percentage
    trump_percentage_global, biden_percentage_global = calculate_percentage(trump_df, biden_df)

    # Calculate country_tweet_count / global_tweet_count
    country_global_percentage = calculate_total_percentage(trump_df, biden_df, selected_country)

    ### Row A
    st.markdown(f'### {selected_country}')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Trump", f'{trump_percentage}%')

    with col2:
        st.metric("Biden", f'{biden_percentage}%')

    with col3:
        st.metric("Country/World", f'{country_global_percentage}%')


    ### Row B
    st.markdown('### Map')
    draw_choropleth(trump_df, biden_df)

    ### Row C
    # Create a filtered DataFrame for the selected country
    # filtered_trump_df = trump_df[trump_df['country'] == selected_country]
    # filtered_biden_df = biden_df[biden_df['country'] == selected_country]

    # Add a selectbox for selecting either "Trump" or "Biden"
    selected_candidate = st.selectbox('Select Candidate', ['Trump', 'Biden'])

    # Dynamically filter the DataFrame based on the selected candidate
    if selected_candidate == 'Trump':
        filtered_df = trump_df[trump_df['country'] == selected_country]
    else:
        filtered_df = biden_df[biden_df['country'] == selected_country]

    # Display the Top 5 Most Liked Tweets
    st.markdown('### Top 5 Most Liked Tweets')
    # Top 10 most liked tweets for the selected country
    top_liked_tweets = filtered_df[filtered_df['country'] == selected_country].nlargest(5, 'likes')
    # Display the dataframe without index and extend it to fill the page
    st.dataframe(
        top_liked_tweets[['tweet', 'likes']],  # Display only the 'tweet' and 'likes' columns
        hide_index=True,  # Hide the index numbers
        use_container_width=True  # Extend the table to fill the page width
    )

    # Display the Top 5 Most Retweeted Tweets
    st.markdown('### Top 5 Most Retweeted Tweets')
    # Select top 5 most retweeted tweets for the selected country
    top_retweeted_tweets = filtered_df[filtered_df['country'] == selected_country].nlargest(5, 'retweet_count')

    # Display the dataframe
    st.dataframe(
        top_retweeted_tweets[['tweet', 'retweet_count']],  # Display 'tweet' and 'retweet_count' columns
        hide_index=True,  # Hide index numbers
        use_container_width=True  # Extend the table to fill the page width
    )
