# us_popularity_analysis.py
from imports import *

def run_us_popularity_analysis(trump_df, biden_df):

    usa_trump_df = trump_df[trump_df['country'] == 'United States']
    usa_biden_df = biden_df[biden_df['country'] == 'United States']

    st.subheader("US Popularity Analysis")

    ### Row A
    # Group by 'state_code' and 'state' for both Trump and Biden DataFrames
    usa_trump_grouped = usa_trump_df.groupby(['state_code', 'state'])['tweet'].count().reset_index()
    usa_biden_grouped = usa_biden_df.groupby(['state_code', 'state'])['tweet'].count().reset_index()

    # Merge grouped DataFrames on 'state_code' (keeping the state information)
    usa_combined_df = pd.merge(usa_trump_grouped, usa_biden_grouped, on='state_code', how='outer')

    # Combine 'state_x' and 'state_y' into a new column 'state'
    usa_combined_df['state'] = usa_combined_df['state_x'].combine_first(usa_combined_df['state_y'])

    # Drop the old columns if they are no longer needed
    usa_combined_df = usa_combined_df.drop(columns=['state_x', 'state_y'])

    # Rename the columns to make them clear
    usa_combined_df = usa_combined_df.rename(columns={'tweet_x': 'trump_tweets', 'tweet_y': 'biden_tweets'})

    # Reset the index for a clean DataFrame
    usa_combined_df = usa_combined_df.reset_index(drop=True)

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
    # plt.title('Top 10 States Tweet Counts: Trump vs Biden vs Total', fontsize=16, color='white', weight='bold')
    plt.xticks([p + bar_width for p in x], top_states['state'], rotation=90, color='white')
    plt.legend(facecolor='white', fontsize=10)
    plt.grid(color='grey', linestyle='--', linewidth=0.5)  # Add gridlines

    # Change tick values to white
    plt.tick_params(axis='x', colors='white')  # X-axis ticks
    plt.tick_params(axis='y', colors='white')  # Y-axis ticks

    # Streamlit display
    st.pyplot(plt, transparent=True)

    # Clear the figure after displaying
    plt.clf()
   
    ### Row B
    usa_trump_df['state'] = usa_trump_df['state'].astype(str)
    usa_biden_df['state'] = usa_biden_df['state'].astype(str)

    unique_states = sorted(list(set(usa_trump_df['state'].unique()) | set(usa_biden_df['state'].unique())))
    selected_state = st.selectbox('Select state', unique_states)

    # Calculate percentage for selected state
    trump_percentage, biden_percentage = calculate_percentage_state(usa_trump_df, usa_biden_df, selected_state)

    # Calculate us percentage
    us_trump_percentage, us_biden_percentage = calculate_percentage(trump_df, biden_df)

    # Calculate state_tweet_count / us_tweet_count
    us_percentage = calculate_total_percentage_state(usa_trump_df, usa_biden_df, selected_state)

    st.markdown(f'### {selected_state}')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Trump", f'{trump_percentage}%')

    with col2:
        st.metric("Biden", f'{biden_percentage}%')

    with col3:
        st.metric("State/US", f'{us_percentage}%')


    ### Row C
    st.markdown('### Map')

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
        # title='Biden vs Trump Tweet Percentages by State',
        hover_name='state',  # Show the state code on hover
        hover_data={
            'trump_percentage': True,  # Display Trump percentage
            'biden_percentage': True,   # Display Biden percentage
            'color': False              # Do not display the difference
        }
    )
    # Update layout for better visualization with a transparent background
    fig.update_layout(
        # title_font=dict(size=16, color='white'),
        paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to transparent
        geo=dict(bgcolor='rgba(255, 255, 255, 0)'),  # Set geo background color to transparent
        coloraxis_showscale=False,  # Hide the color scale (legend)
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    ### Row D

    # Add a selectbox for selecting either "Trump" or "Biden"
    selected_candidate = st.selectbox('Select Candidate', ['Trump', 'Biden'])

    # Dynamically filter the DataFrame based on the selected candidate
    if selected_candidate == 'Trump':
        filtered_df = usa_trump_df[usa_trump_df['state'] == selected_state]
    else:
        filtered_df = usa_biden_df[usa_biden_df['state'] == selected_state]

    # Display the Top 5 Most Liked Tweets
    st.markdown('### Top 5 Most Liked Tweets')
    # Top 10 most liked tweets for the selected state
    top_liked_tweets = filtered_df[filtered_df['state'] == selected_state].nlargest(5, 'likes')
    # Display the dataframe without index and extend it to fill the page
    st.dataframe(
        top_liked_tweets[['tweet', 'likes']],  # Display only the 'tweet' and 'likes' columns
        hide_index=True,  # Hide the index numbers
        use_container_width=True  # Extend the table to fill the page width
    )

    # Display the Top 5 Most Retweeted Tweets
    st.markdown('### Top 5 Most Retweeted Tweets')
    # Select top 5 most retweeted tweets for the selected state
    top_retweeted_tweets = filtered_df[filtered_df['state'] == selected_state].nlargest(5, 'retweet_count')

    # Display the dataframe
    st.dataframe(
        top_retweeted_tweets[['tweet', 'retweet_count']],  # Display 'tweet' and 'retweet_count' columns
        hide_index=True,  # Hide index numbers
        use_container_width=True  # Extend the table to fill the page width
    )