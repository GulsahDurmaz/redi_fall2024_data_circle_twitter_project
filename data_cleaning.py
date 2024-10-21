# data_cleaning.py
from imports import *

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
    'East Timor': 'TLS',
    'Unknown': 'Unknown'
}

# Function to get ISO Alpha-3 country code
def get_country_code(country_name):
    try:
        # Use pycountry to get the country object
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None  # If the country name is not found, return None

def clean_data(data):
    data = data.drop(columns= ['tweet_id', 'lat', 'long', 'continent'])
    # combine 'United States of America' & 'United States' and The Netherlands' & 'Netherlands' and None & 'Unknown'
    country_mapping = {
        'United States of America': 'United States',
        'The Netherlands': 'Netherlands',
        None: 'Unknown'
    }
    data['country'] = data['country'].replace(country_mapping)

    # Apply the function to the 'country' column to create a new 'country_code' column
    data['country_code'] = data['country'].apply(get_country_code)
    # Fill in the missing country codes
    data['country_code'] = data.apply(
        lambda row: missing_country_codes.get(row['country'], row['country_code']),
        axis=1
    )
    return data
