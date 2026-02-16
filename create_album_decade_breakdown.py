#!/usr/bin/env python3
import json
import plotly.graph_objects as go
from collections import defaultdict

# load album data
with open('Music/Data/vcl_albums.json', 'r') as f:
    albums = json.load(f)

# filter albums with release years
albums_with_years = [a for a in albums if a.get('release_year')]

# organize by decade and presenter
decade_data = defaultdict(lambda: defaultdict(int))

for album in albums_with_years:
    year = album['release_year']
    decade = (year // 10) * 10  # e.g., 1975 -> 1970, 1984 -> 1980
    presenter = album['presenter']
    decade_data[presenter][decade] += 1

# get all decades and presenters
all_decades = sorted(set(decade for presenter_decades in decade_data.values() for decade in presenter_decades.keys()))
presenters = sorted(decade_data.keys())

# host colors (same as timeline)
host_colors = {
    'Chris': '#1f77b4',
    'Joe': '#ff7f0e',
    'John': '#2ca02c',
    'Lucas': '#d62728',
    'Adam': '#9467bd',
    'Eric': '#8c564b'
}

# create figure
fig = go.Figure()

# add a bar for each presenter
for presenter in presenters:
    counts = [decade_data[presenter].get(decade, 0) for decade in all_decades]

    fig.add_trace(go.Bar(
        name=presenter,
        x=[f"{decade}s" for decade in all_decades],
        y=counts,
        marker_color=host_colors.get(presenter, '#333333'),
        hovertemplate=f'<b>{presenter}</b><br>' +
                     '%{x}: %{y} albums<br>' +
                     '<extra></extra>'
    ))

fig.update_layout(
    title=dict(
        text='VCL Albums by Decade and Presenter<br><sub>Distribution of album release dates across decades</sub>',
        font=dict(size=20)
    ),
    xaxis_title='Decade',
    yaxis_title='Number of Albums',
    barmode='stack',
    height=600,
    showlegend=True,
    legend=dict(
        title="Presenter",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    hovermode='x unified',
    margin=dict(l=80, r=150, t=100, b=80)
)

fig.write_html('Music/Viz/album_decade_breakdown.html')
print("created album decade breakdown: Music/Viz/album_decade_breakdown.html")

# stats
print(f"\ntotal albums analyzed: {len(albums_with_years)}")
print(f"decade range: {min(all_decades)}s - {max(all_decades)}s")

print("\nalbums per decade:")
for decade in all_decades:
    total = sum(decade_data[p].get(decade, 0) for p in presenters)
    print(f"  {decade}s: {total} albums")

print("\nalbums per presenter by decade:")
for presenter in presenters:
    total = sum(decade_data[presenter].values())
    print(f"  {presenter}: {total} albums total")
    for decade in all_decades:
        count = decade_data[presenter].get(decade, 0)
        if count > 0:
            print(f"    {decade}s: {count}")
