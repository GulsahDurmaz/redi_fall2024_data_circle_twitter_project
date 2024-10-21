# percentage_calculating_state.py
from imports import *

def calculate_count_state(data1, data2, selected_state=None):
    # Filter by state if state is provided
    if selected_state:
        data1 = data1[data1['state'] == selected_state]
        data2 = data2[data2['state'] == selected_state]
    
    # Calculate the total percentage of tweets
    data1_count = data1.shape[0]
    data2_count = data2.shape[0]
    total_tweet_count = data1_count + data2_count

    return (data1_count, data2_count, total_tweet_count)

def calculate_percentage_state(data1, data2, selected_state=None):
    # Filter by state if state is provided
    if selected_state:
        data1 = data1[data1['state'] == selected_state]
        data2 = data2[data2['state'] == selected_state]
    
    # Calculate the total percentage of tweets
    data1_count = data1.shape[0]
    data2_count = data2.shape[0]
    total_tweet_count = data1_count + data2_count

    # Avoid division by zero
    if total_tweet_count == 0:
        return 0.0, 0.0  # Return 0 for both percentages if there are no tweets

    # Calculate percentages for Trump and Biden
    trump_percentage = (data1_count / total_tweet_count) * 100
    biden_percentage = (data2_count / total_tweet_count) * 100

    # Return both percentages
    return round(trump_percentage, 2), round(biden_percentage, 2)


def calculate_total_percentage_state(data1, data2, selected_state):
    total_tweet_usa = data1.shape[0] + data2.shape[0]
    # Filter the data by the selected state
    filtered_data1 = data1[data1['state'] == selected_state]
    filtered_data2 = data2[data2['state'] == selected_state]

    # Calculate the number of tweets for each candidate
    data1_count = filtered_data1.shape[0]
    data2_count = filtered_data2.shape[0]
    total_tweet_count = data1_count + data2_count

    # Avoid division by zero
    if total_tweet_count == 0:
        return 0  # Or return an appropriate error message
    
    total_percentage = (total_tweet_count / total_tweet_usa) * 100
    total_percentage = round(total_percentage, 1)

    return total_percentage