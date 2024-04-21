import requests
import json
import pandas as pd
import numpy as np
from geojson import Point, Feature, FeatureCollection

base_url = "https://naptan.api.dft.gov.uk"
endpoint = "/v1/access-nodes"
param = {
    "dataFormat": 'csv'
    }
x= base_url + endpoint
print(x)

response = requests.get(x,params=param)
response.raise_for_status()  # raises exception when not a 2xx response
if response.status_code != 204:
  with open("naptan_scrapped.csv", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            file.flush()

a  = pd.read_csv('naptan_scrapped.csv')

# null_values = a['Latitude'].isnull().sum()
# # Check for missing values (non-null values) in a specific column
# missing_values = a['Latitude'].notna().sum()
# # Get descriptive statistics for a numerical column (e.g., 'Latitude')
# latitude_stats = a['Latitude'].describe()
# print("Null values in 'Latitude' column:", null_values)
# print("Missing values (non-null) in 'Latitude' column:", missing_values)
# print("Descriptive statistics for 'Latitude' column:")
# print(latitude_stats)

# null_values = a['Longitude'].isnull().sum()
# # Check for missing values (non-null values) in a specific column
# missing_values = a['Longitude'].notna().sum()
# # Get descriptive statistics for a numerical column (e.g., 'Latitude')
# longitude_stats = a['Longitude'].describe()
# print("Null values in 'Longitude' column:", null_values)
# print("Missing values (non-null) in 'Longitude' column:", missing_values)
# print("Descriptive statistics for 'Longitude' column:")
# print(longitude_stats)

df = a.dropna(subset=['Latitude', 'Longitude'])

df.to_csv('cleaned_data.csv', index=True)

# Create an empty list to store GeoJSON strings
geojson_strings = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Extract latitude and longitude values from the row
    latitude = row['Latitude']
    longitude = row['Longitude']

    # Create a GeoJSON string for the current row
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        },
        "properties": {
            "Latitude": latitude,
            "Longitude": longitude
        }
    }
    # Convert the feature to a GeoJSON string and append it to the list
    geojson_strings.append(json.dumps(feature))

# Print the length of the GeoJSON strings list and the first few GeoJSON strings for inspection
# print("Length of GeoJSON strings list:", len(geojson_strings))
# for i in range(min(5, len(geojson_strings))):
#     print("GeoJSON string", i+1, ":", geojson_strings[i])

df['geom'] = geojson_strings

# Define a function to format GeoJSON strings to the specified format
def format_point(geojson_str):
    # Parse GeoJSON string to a dictionary
    geojson_obj = json.loads(geojson_str)
    # Extract coordinates from the GeoJSON object
    coordinates = geojson_obj['geometry']['coordinates']
    # Format coordinates into the specified format
    return f"POINT({coordinates[0]} {coordinates[1]})"

# Apply the format_point function to the 'geom' column
df['geom'] = df['geom'].apply(format_point)
df.to_csv('naptan_with_geomcolumn.csv', index=True)