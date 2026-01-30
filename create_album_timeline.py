#!/usr/bin/env python3
import json
import plotly.graph_objects as go
from collections import defaultdict

# load album data
with open('vcl_albums.json', 'r') as f:
    albums = json.load(f)

# filter out TBA entries
real_albums = [a for a in albums if a['artist'] != 'Various']

# sort by release year
real_albums.sort(key=lambda x: x['release_year'])

# host colors (same as cocktail viz for consistency)
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
for album in real_albums:
    by_presenter[album['presenter']].append(album)

# create figure
fig = go.Figure()

# add traces by presenter
for presenter in sorted(by_presenter.keys()):
    presenter_albums = by_presenter[presenter]

    fig.add_trace(go.Scatter(
        x=[a['release_year'] for a in presenter_albums],
        y=[i for i, a in enumerate(real_albums) if a in presenter_albums],
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
                     'released: %{x}<br>' +
                     f'presented by: {presenter}<br>' +
                     '<extra></extra>'
    ))

# add vertical lines for decade markers
fig.add_vline(x=1970, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="1970s")
fig.add_vline(x=1980, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="1980s")
fig.add_vline(x=1990, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="1990s")
fig.add_vline(x=2000, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="2000s")
fig.add_vline(x=2010, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="2010s")
fig.add_vline(x=2020, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="2020s")

fig.update_layout(
    title=dict(
        text='VCL Album Timeline by Release Year<br><sub>colored by presenter</sub>',
        font=dict(size=20)
    ),
    xaxis_title='release year',
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
    margin=dict(l=50, r=350, t=80, b=50)
)

fig.write_html('album_timeline.html')
print("created album timeline: album_timeline.html")

# stats
print(f"\ntotal albums on timeline: {len(real_albums)}")
print(f"year range: {min(a['release_year'] for a in real_albums)} - {max(a['release_year'] for a in real_albums)}")

print("\nalbums per presenter:")
for presenter in sorted(by_presenter.keys()):
    print(f"  {presenter}: {len(by_presenter[presenter])}")

# decade breakdown
from collections import Counter
decade_counts = Counter()
for album in real_albums:
    decade = str(album['release_year'])[:3] + '0s'
    decade_counts[decade] += 1

print("\nalbums by decade:")
for decade in sorted(decade_counts.keys()):
    print(f"  {decade}: {decade_counts[decade]}")
