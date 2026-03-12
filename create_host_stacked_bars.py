#!/usr/bin/env python3
import json
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

# load cocktail data
with open('Cocktail/Data/cocktail_history.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# group by host and country
country_by_host = df.groupby(['host', 'country_of_origin']).size().unstack(fill_value=0)

# group by host and primary liquor
liquor_by_host = df.groupby(['host', 'primary_liquor']).size().unstack(fill_value=0)

# create figure with buttons to switch between views
fig = go.Figure()

# add traces for country view (visible by default)
colors_country = {
    'USA': '#1f77b4',
    'France': '#ff7f0e',
    'Italy': '#2ca02c',
    'Cuba': '#d62728',
    'Belgium': '#9467bd',
    'Scotland': '#8c564b',
    'Canada': '#e377c2',
    'Bermuda': '#7f7f7f',
    'British Virgin Islands': '#bcbd22',
    'Mexico': '#17becf',
    'UK': '#aec7e8'
}

for country in country_by_host.columns:
    fig.add_trace(go.Bar(
        name=country,
        x=country_by_host.index,
        y=country_by_host[country],
        marker_color=colors_country.get(country, '#cccccc'),
        visible=True,
        hovertemplate='<b>%{x}</b><br>' + country + ': %{y}<extra></extra>'
    ))

# add traces for liquor view (hidden initially)
colors_liquor = {
    'whiskey': '#8B4513',
    'bourbon': '#D2691E',
    'rye': '#CD853F',
    'scotch': '#DEB887',
    'gin': '#87CEEB',
    'vodka': '#E6E6FA',
    'rum': '#F4A460',
    'tequila': '#FFD700',
    'brandy': '#CD5C5C',
    'other': '#808080'
}

for liquor in liquor_by_host.columns:
    fig.add_trace(go.Bar(
        name=liquor,
        x=liquor_by_host.index,
        y=liquor_by_host[liquor],
        marker_color=colors_liquor.get(liquor, '#cccccc'),
        visible=False,
        hovertemplate='<b>%{x}</b><br>' + liquor + ': %{y}<extra></extra>'
    ))

# create buttons to toggle between views
num_country_traces = len(country_by_host.columns)
num_liquor_traces = len(liquor_by_host.columns)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.5,
            xanchor="center",
            y=1.15,
            yanchor="top",
            buttons=[
                dict(
                    label="By Country",
                    method="update",
                    args=[
                        {"visible": [True] * num_country_traces + [False] * num_liquor_traces},
                        {"title": "Cocktails by Host - Stacked by Country of Origin",
                         "yaxis": {"title": "Number of Cocktails"}}
                    ]
                ),
                dict(
                    label="By Primary Liquor",
                    method="update",
                    args=[
                        {"visible": [False] * num_country_traces + [True] * num_liquor_traces},
                        {"title": "Cocktails by Host - Stacked by Primary Liquor",
                         "yaxis": {"title": "Number of Cocktails"}}
                    ]
                )
            ]
        )
    ]
)

fig.update_layout(
    title="Cocktails by Host - Stacked by Country of Origin",
    xaxis_title="Host",
    yaxis_title="Number of Cocktails",
    barmode='stack',
    height=600,
    showlegend=True,
    legend=dict(
        title="",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    margin=dict(t=100)
)

fig.write_html('Cocktail/Viz/cocktails_by_host_stacked.html')
print("created interactive stacked bar chart: cocktails_by_host_stacked.html")

# print summary stats
print("\ncocktails per host:")
host_counts = df['host'].value_counts().sort_index()
for host, count in host_counts.items():
    print(f"  {host}: {count}")

print("\nby country breakdown:")
print(country_by_host.to_string())

print("\nby liquor breakdown:")
print(liquor_by_host.to_string())
