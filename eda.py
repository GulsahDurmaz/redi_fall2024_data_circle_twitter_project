# eda.py
from imports import *

def run_exploratory_data_analysis(trump_df, biden_df):
    st.markdown("## Exploratory Data Analysis")
    st.markdown("""
    The 2020 United States presidential election was held on **November 3, 2020**. The major candidates were incumbent 
    Republican President Donald Trump and Democratic former Vice President Joe Biden. In the months leading up to the 
    election, social media played a significant role in shaping public opinion, with platforms like Twitter serving as a 
    key battleground for discussions, endorsements, and criticism.
    """)

    st.markdown("**Why Twitter?**")
    st.markdown("""
    Social media platforms like Facebook and Twitter have transformed how we interact and share news. As of June 2019, Twitter had over 348M users posting 500M tweets daily, enabling users to influence trends and shape news coverage.

    Twitter has become increasingly important in electoral campaigning, with politicians and parties actively using the platform. This rise in political activity on Twitter has attracted researchers' interest, making election prediction based on Twitter data a popular field. Researchers now analyze citizen sentiment to estimate candidate performance in elections ([Garcia et al., 2019](https://dl.acm.org/doi/pdf/10.1145/3339909)).
    """)
    
    selected_country = 'United States'
    # Calculate percentage for selected country
    trump_percentage, biden_percentage = calculate_percentage(trump_df, biden_df, selected_country)
    
    # Calculate global percentage
    trump_percentage_global, biden_percentage_global = calculate_percentage(trump_df, biden_df)
    
    # Streamlit radio button to select between 'Global' and 'USA'
    view = st.radio("Select View", ['Global_popularity', 'USA_popularity'])
    # Filter data based on the selected view
    if view == "USA_popularity":  # USA View
        trump_tweet_percentage = trump_percentage
        biden_tweet_percentage = biden_percentage
        trump_tweet_count, biden_tweet_count, total_tweet_count = calculate_count(trump_df, biden_df, selected_country)
    else:  # Global View
        trump_tweet_percentage = trump_percentage_global
        biden_tweet_percentage = biden_percentage_global
        trump_tweet_count, biden_tweet_count, total_tweet_count = calculate_count(trump_df, biden_df)
    # Prepare data for the bar chart
    popularity_data_percentage = pd.DataFrame({
        'Candidates': ['Donald Trump', 'Joe Biden'],
        'Tweet Percentage': [trump_tweet_percentage, biden_tweet_percentage]
    })
    # Plot the bar chart
    fig1 = px.bar(popularity_data_percentage, 
                x='Candidates', 
                y='Tweet Percentage', 
                # title=f"Twitter Popularity % - Trump vs Biden ({view})",
                labels={'Tweet Percentage': 'Tweet %', 'Candidates': 'Candidates'},
                color='Candidates',
                color_discrete_map={'Donald Trump': 'red', 'Joe Biden': 'blue'})
    st.markdown("**Twitter Popularity % - Trump vs Biden**")
    # Display the chart in Streamlit
    st.plotly_chart(fig1)
    # Additional Conclusion Section
    # Dynamically update the conclusion based on the selected view
    conclusion = f"""
        <div style='text-align: justify;'>
            This bar chart reveals important insights into the relative popularity of Donald Trump and
            Joe Biden on Twitter during the 2020 U.S. presidential election. A total of <strong>{total_tweet_count}</strong> tweets 
            were recorded, with <strong>{trump_tweet_count}</strong> tweets using the Trump hashtag and <strong>{biden_tweet_count}</strong> 
            tweets associated with the Biden hashtag. These figures indicate the level of public interest and the extent
            of discussions surrounding each candidate's campaign in the <strong>{view}</strong> dataset.
        </div>
    """# Display the conclusion
    st.markdown(conclusion, unsafe_allow_html=True)

    # Adding space between the paragraph and the chart
    st.markdown("<br><br>", unsafe_allow_html=True)

    view2 = st.radio("Select View", ['Global_daily', 'USA_daily'])
    # Filter data based on the selected view
    usa_trump_df = trump_df[trump_df['country'] == 'United States']
    usa_biden_df = biden_df[biden_df['country'] == 'United States']
    if view2 == "USA_daily":  # USA View
        t_tweets_per_day = usa_trump_df.groupby(trump_df['created_at'].dt.date).size()
        b_tweets_per_day = usa_biden_df.groupby(biden_df['created_at'].dt.date).size()
    else:  # Global View
        t_tweets_per_day = trump_df.groupby(trump_df['created_at'].dt.date).size()
        b_tweets_per_day = biden_df.groupby(biden_df['created_at'].dt.date).size()
    # Plotting
    plt.figure(figsize=(10, 5), facecolor='black')
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
    view3 = st.radio('Select View', options=['Global_hourly', 'USA_hourly'])
    # Filter data based on the selected view
    if view3 == "USA_hourly":  # USA View
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
