#!/usr/bin/env python3
import json
import pandas as pd
from collections import Counter

# city coordinates for all cocktail origins
city_coords = {
    'New Orleans, Louisiana': {'lat': 29.9511, 'lon': -90.0715, 'display': 'New Orleans, LA'},
    'Paris': {'lat': 48.8566, 'lon': 2.3522, 'display': 'Paris, France'},
    'USA': {'lat': 39.8283, 'lon': -98.5795, 'display': 'USA (unknown city)'},  # geographic center of USA
    'Los Angeles, California': {'lat': 34.0522, 'lon': -118.2437, 'display': 'Los Angeles, CA'},
    'Louisville, Kentucky': {'lat': 38.2527, 'lon': -85.7585, 'display': 'Louisville, KY'},
    'Florence': {'lat': 43.7696, 'lon': 11.2558, 'display': 'Florence, Italy'},
    'New York, New York': {'lat': 40.7128, 'lon': -74.0060, 'display': 'New York, NY'},
    'Brussels': {'lat': 50.8503, 'lon': 4.3517, 'display': 'Brussels, Belgium'},
    'Havana': {'lat': 23.1136, 'lon': -82.3666, 'display': 'Havana, Cuba'},
    'Boston, Massachusetts': {'lat': 42.3601, 'lon': -71.0589, 'display': 'Boston, MA'},
    'Kentucky': {'lat': 37.8393, 'lon': -84.2700, 'display': 'Kentucky, USA'},
    'Dufftown, Scotland': {'lat': 57.4486, 'lon': -3.1272, 'display': 'Dufftown, Scotland'},
    'San Francisco, California': {'lat': 37.7749, 'lon': -122.4194, 'display': 'San Francisco, CA'},
    'London': {'lat': 51.5074, 'lon': -0.1278, 'display': 'London, UK'},
    'Toronto, Ontario': {'lat': 43.6532, 'lon': -79.3832, 'display': 'Toronto, Canada'},
    'Tortola': {'lat': 18.4207, 'lon': -64.6400, 'display': 'Tortola, BVI'},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528, 'display': 'Mexico (unknown city)'},
    'Philadelphia, Pennsylvania': {'lat': 39.9526, 'lon': -75.1652, 'display': 'Philadelphia, PA'},
    'Cape Cod, Massachusetts': {'lat': 41.6688, 'lon': -70.2962, 'display': 'Cape Cod, MA'},
    'Bermuda': {'lat': 32.3078, 'lon': -64.7505, 'display': 'Bermuda'}
}

# load cocktail data
with open('cocktail_history.json', 'r') as f:
    data = json.load(f)

# count cocktails by city
city_counts = Counter(entry['city_of_origin'] for entry in data)

# create location data with counts
locations = []
for city, count in city_counts.items():
    if city in city_coords:
        locations.append({
            'city': city_coords[city]['display'],
            'lat': city_coords[city]['lat'],
            'lon': city_coords[city]['lon'],
            'count': count
        })

# save location data
with open('cocktail_locations.json', 'w') as f:
    json.dump(locations, f, indent=2)

print(f"mapped {len(locations)} unique locations")
print("\ntop origins by cocktail count:")
for loc in sorted(locations, key=lambda x: x['count'], reverse=True)[:10]:
    print(f"  {loc['city']}: {loc['count']}")

# now create the visualization
import plotly.graph_objects as go

# create figure
fig = go.Figure()

# add scattergeo for cocktail origins
fig.add_trace(go.Scattergeo(
    lon=[loc['lon'] for loc in locations],
    lat=[loc['lat'] for loc in locations],
    text=[f"{loc['city']}<br>{loc['count']} cocktail{'s' if loc['count'] > 1 else ''}" for loc in locations],
    mode='markers',
    marker=dict(
        size=[loc['count'] * 3 + 8 for loc in locations],  # scale by count
        color=[loc['count'] for loc in locations],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title="Number of<br>Cocktails"
        ),
        line=dict(width=0.5, color='white')
    ),
    hovertemplate='<b>%{text}</b><extra></extra>',
    name=''
))

fig.update_layout(
    title=dict(
        text='VCL Cocktail Origins by City (2015-2025)',
        font=dict(size=20)
    ),
    geo=dict(
        scope='world',
        projection_type='natural earth',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        showlakes=True,
        lakecolor='rgb(230, 240, 255)',
        showcountries=True,
        countrycolor='rgb(204, 204, 204)'
    ),
    height=700,
    margin=dict(l=0, r=0, t=50, b=0)
)

# save as html
fig.write_html('cocktail_origin_map.html')
print("\ncreated interactive map: cocktail_origin_map.html")

# also create a US-focused version
fig_us = go.Figure()

us_locations = [loc for loc in locations if -170 < loc['lon'] < -60 and 15 < loc['lat'] < 72]

fig_us.add_trace(go.Scattergeo(
    lon=[loc['lon'] for loc in us_locations],
    lat=[loc['lat'] for loc in us_locations],
    text=[f"{loc['city']}<br>{loc['count']} cocktail{'s' if loc['count'] > 1 else ''}" for loc in us_locations],
    mode='markers+text',
    textposition='top center',
    textfont=dict(size=9),
    marker=dict(
        size=[loc['count'] * 4 + 10 for loc in us_locations],
        color=[loc['count'] for loc in us_locations],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title="Number of<br>Cocktails"
        ),
        line=dict(width=1, color='white')
    ),
    hovertemplate='<b>%{text}</b><extra></extra>',
    name=''
))

fig_us.update_layout(
    title=dict(
        text='VCL Cocktail Origins - North America Focus',
        font=dict(size=20)
    ),
    geo=dict(
        scope='north america',
        projection_type='albers usa',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        showlakes=True,
        lakecolor='rgb(230, 240, 255)',
        showcountries=True,
        countrycolor='rgb(204, 204, 204)'
    ),
    height=700,
    margin=dict(l=0, r=0, t=50, b=0)
)

fig_us.write_html('cocktail_origin_map_us.html')
print("created US-focused map: cocktail_origin_map_us.html")
