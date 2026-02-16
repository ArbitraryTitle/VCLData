#!/usr/bin/env python3
import json
import plotly.graph_objects as go
from collections import defaultdict
import datetime

# load album data
with open('Music/Data/vcl_albums.json', 'r') as f:
    albums = json.load(f)

# filter out TBA entries and albums without dates
real_albums = [a for a in albums if a.get('release_date')]

# convert dates and sort
albums_with_dates = []
for album in real_albums:
    try:
        date_obj = datetime.datetime.strptime(album['release_date'], '%Y-%m-%d')
        album['date_obj'] = date_obj
        albums_with_dates.append(album)
    except:
        print(f"Warning: couldn't parse date for {album['artist']} - {album['album_title']}")

albums_with_dates.sort(key=lambda x: x['date_obj'])

# host colors (same as before)
host_colors = {
    'Chris': '#1f77b4',
    'Joe': '#ff7f0e',
    'John': '#2ca02c',
    'Lucas': '#d62728',
    'Adam': '#9467bd',
    'Eric': '#8c564b'
}

# group by presenter
by_presenter = defaultdict(list)
for album in albums_with_dates:
    by_presenter[album['presenter']].append(album)

# create figure
fig = go.Figure()

# add traces by presenter
for presenter in sorted(by_presenter.keys()):
    presenter_albums = by_presenter[presenter]

    fig.add_trace(go.Scatter(
        x=[a['date_obj'] for a in presenter_albums],
        y=[i for i, a in enumerate(albums_with_dates) if a in presenter_albums],
        mode='markers+text',
        name=presenter,
        marker=dict(
            size=10,
            color=host_colors[presenter],
            line=dict(width=1, color='white')
        ),
        text=[f"{a['artist']} - {a['album_title']}" for a in presenter_albums],
        textposition='middle right',
        textfont=dict(size=8),
        hovertemplate='<b>%{text}</b><br>' +
                     'released: %{x|%B %d, %Y}<br>' +
                     f'presented by: {presenter}<br>' +
                     '<extra></extra>'
    ))

# add vertical lines for decade markers using shapes
shapes = []
annotations = []
for year in [1970, 1980, 1990, 2000, 2010, 2020]:
    decade_date = datetime.datetime(year, 1, 1)
    shapes.append(
        dict(
            type='line',
            x0=decade_date,
            x1=decade_date,
            y0=0,
            y1=1,
            yref='paper',
            line=dict(
                color='gray',
                width=1,
                dash='dash'
            ),
            opacity=0.3
        )
    )
    annotations.append(
        dict(
            x=decade_date,
            y=1,
            yref='paper',
            text=f"{year}s",
            showarrow=False,
            yshift=10,
            font=dict(size=10, color='gray')
        )
    )

fig.update_layout(
    title=dict(
        text='VCL Album Timeline by Exact Release Date<br><sub>colored by presenter</sub>',
        font=dict(size=20)
    ),
    xaxis=dict(
        title='release date',
        tickformat='%Y',
        dtick='M60'  # tick every 5 years
    ),
    yaxis=dict(
        showticklabels=False,
        title=''
    ),
    height=1400,
    showlegend=True,
    legend=dict(
        title="presenter",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    hovermode='closest',
    margin=dict(l=50, r=350, t=80, b=50),
    shapes=shapes,
    annotations=annotations
)

fig.write_html('Music/Viz/album_timeline_full_dates.html')
print("created album timeline with full dates: Music/Viz/album_timeline_full_dates.html")

# stats
print(f"\ntotal albums on timeline: {len(albums_with_dates)}")
print(f"date range: {albums_with_dates[0]['date_obj'].strftime('%B %d, %Y')} - {albums_with_dates[-1]['date_obj'].strftime('%B %d, %Y')}")

print("\nalbums per presenter:")
for presenter in sorted(by_presenter.keys()):
    print(f"  {presenter}: {len(by_presenter[presenter])}")

# find albums released on same day
from collections import Counter
date_counts = Counter(a['release_date'] for a in albums_with_dates)
duplicates = [(date, count) for date, count in date_counts.items() if count > 1]
if duplicates:
    print("\nalbums released on same day:")
    for date, count in sorted(duplicates):
        print(f"  {date}: {count} albums")
        same_day = [a for a in albums_with_dates if a['release_date'] == date]
        for a in same_day:
            print(f"    - {a['artist']} - {a['album_title']}")
