from folium import Map, Marker
import pandas as pd

def create_map(data):
    """
    Create a map with markers for each location in the data.

    Parameters:
    - data: DataFrame containing 'latitude', 'longitude', and 'location' columns.

    Returns:
    - folium.Map object with markers.
    """
    if data.empty:
        return None

    # Initialize the map centered around the mean latitude and longitude
    m = Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

    # Add markers for each location
    for _, row in data.iterrows():
        Marker(location=[row['latitude'], row['longitude']], popup=row['location']).add_to(m)

    return m

def save_map(m, file_path):
    """
    Save the folium map to an HTML file.

    Parameters:
    - m: folium.Map object to save.
    - file_path: Path to save the HTML file.
    """
    if m is not None:
        m.save(file_path)