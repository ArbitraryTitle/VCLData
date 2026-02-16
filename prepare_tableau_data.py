#!/usr/bin/env python3
import json
import csv
import pandas as pd

# load main data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

# city coordinates for mapping
city_coords = {
    'New Orleans, Louisiana': {'lat': 29.9511, 'lon': -90.0715},
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'USA': {'lat': 39.8283, 'lon': -98.5795},
    'Los Angeles, California': {'lat': 34.0522, 'lon': -118.2437},
    'Louisville, Kentucky': {'lat': 38.2527, 'lon': -85.7585},
    'Florence': {'lat': 43.7696, 'lon': 11.2558},
    'New York, New York': {'lat': 40.7128, 'lon': -74.0060},
    'Brussels': {'lat': 50.8503, 'lon': 4.3517},
    'Havana': {'lat': 23.1136, 'lon': -82.3666},
    'Boston, Massachusetts': {'lat': 42.3601, 'lon': -71.0589},
    'Kentucky': {'lat': 37.8393, 'lon': -84.2700},
    'Dufftown, Scotland': {'lat': 57.4486, 'lon': -3.1272},
    'San Francisco, California': {'lat': 37.7749, 'lon': -122.4194},
    'London': {'lat': 51.5074, 'lon': -0.1278},
    'Toronto, Ontario': {'lat': 43.6532, 'lon': -79.3832},
    'Tortola': {'lat': 18.4207, 'lon': -64.6400},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528},
    'Philadelphia, Pennsylvania': {'lat': 39.9526, 'lon': -75.1652},
    'Cape Cod, Massachusetts': {'lat': 41.6688, 'lon': -70.2962},
    'Bermuda': {'lat': 32.3078, 'lon': -64.7505}
}

# add lat/lon and era to each entry
for entry in data:
    city = entry['city_of_origin']
    if city in city_coords:
        entry['latitude'] = city_coords[city]['lat']
        entry['longitude'] = city_coords[city]['lon']
    else:
        entry['latitude'] = None
        entry['longitude'] = None

    # add era for easier filtering
    year = entry.get('year_invented')
    if year:
        if year < 1900:
            entry['era'] = '1800s'
        elif year < 1920:
            entry['era'] = '1900-1919'
        elif year < 1940:
            entry['era'] = '1920-1939'
        elif year < 1960:
            entry['era'] = '1940-1959'
        elif year < 1980:
            entry['era'] = '1960-1979'
        elif year < 2000:
            entry['era'] = '1980-1999'
        else:
            entry['era'] = '2000+'
    else:
        entry['era'] = 'Unknown'

# save enhanced CSV for Tableau
fieldnames = [
    'meeting_number', 'date', 'host', 'cocktail',
    'country_of_origin', 'city_of_origin', 'latitude', 'longitude',
    'primary_liquor', 'whiskey_type', 'year_invented', 'era'
]

with open('cocktail_history_tableau.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("created tableau-ready file: cocktail_history_tableau.csv")
print("\ncolumns included:")
for field in fieldnames:
    print(f"  - {field}")

# create summary stats file for reference
df = pd.DataFrame(data)
stats = {
    'total_cocktails': len(df),
    'unique_hosts': df['host'].nunique(),
    'unique_countries': df['country_of_origin'].nunique(),
    'unique_cities': df['city_of_origin'].nunique(),
    'date_range': f"{df['date'].min()} to {df['date'].max()}",
    'year_range': f"{int(df['year_invented'].min())} to {int(df['year_invented'].max())}",
    'most_common_liquor': df['primary_liquor'].mode()[0],
    'most_common_country': df['country_of_origin'].mode()[0]
}

with open('tableau_data_summary.txt', 'w') as f:
    f.write("VCL COCKTAIL DATA SUMMARY\n")
    f.write("=" * 50 + "\n\n")
    for key, value in stats.items():
        f.write(f"{key}: {value}\n")

    f.write("\n" + "=" * 50 + "\n")
    f.write("BREAKDOWN BY HOST\n")
    f.write("=" * 50 + "\n")
    host_counts = df['host'].value_counts()
    for host, count in host_counts.items():
        f.write(f"{host}: {count} cocktails\n")

print("\ncreated data summary: tableau_data_summary.txt")
