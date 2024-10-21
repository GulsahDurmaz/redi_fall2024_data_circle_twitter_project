from imports import *

def draw_choropleth(trump_df, biden_df):
    # Create a DataFrame to store the country-wise percentage values
    country_list = sorted(list(set(trump_df['country'].unique()) | set(biden_df['country'].unique())))
    percentage_list = []

    # Iterate over each country and calculate the Trump/Biden percentages
    for country in country_list:
        trump_percentage, biden_percentage = calculate_percentage(trump_df, biden_df, country)
        # Calculate a color value based on the difference between Trump and Biden
        difference = trump_percentage - biden_percentage
        percentage_list.append({
            'country': country,
            'trump_percentage': trump_percentage,
            'biden_percentage': biden_percentage,
            'difference': difference  # Positive for Trump, Negative for Biden
        })

    # Create a DataFrame from the percentage_list
    map_data = pd.DataFrame(percentage_list)

    # Normalize the difference for color mapping (-100 for Biden, +100 for Trump)
    map_data['color'] = map_data['difference'].apply(lambda x: max(min(x, 100), -100))  # Cap between -100 and 100

    # Plot the choropleth using Plotly
    fig = px.choropleth(
        map_data,
        locations='country',  # Column containing country names
        locationmode='country names',  # Map locations by country name
        color='color',  # Use the normalized difference to determine the color
        color_continuous_scale=['blue', 'white', 'red'],  # Blue for Biden, Red for Trump, White for balance
        range_color=(-100, 100),  # Range from -100 (Biden) to +100 (Trump)
        # height=400,  # Adjust height as needed
        hover_data={
            'trump_percentage': True,  # Display Trump percentage
            'biden_percentage': True,  # Display Biden percentage
            'color': False  # Do not display the color (difference)
        }
    )

    # Update geos and layout
    fig.update_geos(
        showcoastlines=True, 
        coastlinecolor="Gray", 
        showland=True, 
        landcolor="white",
        showframe=False,
        projection_type="natural earth"  # Specify the type of map projection
    )
    
    # Set layout to remove margins and hide the legend
    fig.update_layout(
        autosize=True,
        margin=dict(l=5, r=5, t=5, b=5),  # Remove margins
        paper_bgcolor='rgba(255, 255, 255, 0)',  # Set paper background color to transparent
        geo=dict(bgcolor='rgba(255, 255, 255, 0)'),
        coloraxis_showscale=False,  # Hide the color scale (legend)
    )

    # Display the figure using Streamlit
    st.plotly_chart(fig, use_container_width=True)  # Use container width for responsiveness