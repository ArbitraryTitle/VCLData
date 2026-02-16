#!/usr/bin/env python3
import json
import plotly.graph_objects as go
from collections import defaultdict

# load album data
with open('Music/Data/vcl_albums.json', 'r') as f:
    albums = json.load(f)

# filter albums with release years
albums_with_years = [a for a in albums if a.get('release_year')]

# organize by presenter and decade
presenter_data = defaultdict(lambda: defaultdict(int))

for album in albums_with_years:
    year = album['release_year']
    decade = (year // 10) * 10  # e.g., 1975 -> 1970, 1984 -> 1980
    presenter = album['presenter']
    presenter_data[presenter][decade] += 1

# get all decades and presenters
all_decades = sorted(set(decade for presenter_decades in presenter_data.values() for decade in presenter_decades.keys()))
presenters = sorted(presenter_data.keys())

# decade colors (color gradient from older to newer)
decade_colors = {
    1960: '#8c564b',  # brown
    1970: '#e377c2',  # pink
    1980: '#7f7f7f',  # gray
    1990: '#bcbd22',  # yellow-green
    2000: '#17becf',  # cyan
    2010: '#ff7f0e',  # orange
    2020: '#d62728'   # red
}

# create figure
fig = go.Figure()

# add a bar for each decade
for decade in all_decades:
    counts = [presenter_data[presenter].get(decade, 0) for presenter in presenters]

    fig.add_trace(go.Bar(
        name=f"{decade}s",
        x=presenters,
        y=counts,
        marker_color=decade_colors.get(decade, '#333333'),
        hovertemplate=f'<b>%{{x}}</b><br>' +
                     f'{decade}s: %{{y}} albums<br>' +
                     '<extra></extra>'
    ))

fig.update_layout(
    title=dict(
        text='VCL Presenter Album Preferences by Decade<br><sub>Each presenter\'s albums broken down by release decade</sub>',
        font=dict(size=20)
    ),
    xaxis_title='Presenter',
    yaxis_title='Number of Albums',
    barmode='stack',
    height=600,
    showlegend=True,
    legend=dict(
        title="Decade",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    hovermode='x unified',
    margin=dict(l=80, r=150, t=100, b=80)
)

fig.write_html('Music/Viz/presenter_decade_breakdown.html')
print("created presenter decade breakdown: Music/Viz/presenter_decade_breakdown.html")

# stats
print(f"\ntotal albums analyzed: {len(albums_with_years)}")

print("\nalbums per presenter:")
for presenter in presenters:
    total = sum(presenter_data[presenter].values())
    print(f"  {presenter}: {total} albums total")
    decade_list = sorted(presenter_data[presenter].items())
    print(f"    Decades: {', '.join([f'{d}s ({c})' for d, c in decade_list])}")

print("\nmost popular decade per presenter:")
for presenter in presenters:
    if presenter_data[presenter]:
        top_decade = max(presenter_data[presenter].items(), key=lambda x: x[1])
        print(f"  {presenter}: {top_decade[0]}s ({top_decade[1]} albums)")
