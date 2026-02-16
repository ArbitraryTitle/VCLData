#!/usr/bin/env python3
import json
import plotly.graph_objects as go
from collections import defaultdict

# load cocktail data
with open('Cocktail/Data/cocktail_history.json', 'r') as f:
    data = json.load(f)

# filter out any without invention years
cocktails_with_years = [c for c in data if c.get('year_invented')]

# sort by invention year
cocktails_with_years.sort(key=lambda x: x['year_invented'])

# color scheme for hosts
host_colors = {
    'Chris': '#1f77b4',
    'Joe': '#ff7f0e',
    'John': '#2ca02c',
    'Lucas': '#d62728',
    'Adam': '#9467bd',
    'Eric': '#8c564b'
}

# group by host for the legend
by_host = defaultdict(list)
for cocktail in cocktails_with_years:
    by_host[cocktail['host']].append(cocktail)

# create figure
fig = go.Figure()

# add traces by host (for legend grouping)
for host in sorted(by_host.keys()):
    cocktails = by_host[host]

    fig.add_trace(go.Scatter(
        x=[c['year_invented'] for c in cocktails],
        y=[i for i, c in enumerate(cocktails_with_years) if c in cocktails],
        mode='markers+text',
        name=host,
        marker=dict(
            size=12,
            color=host_colors[host],
            line=dict(width=1, color='white')
        ),
        text=[c['cocktail'] for c in cocktails],
        textposition='middle right',
        textfont=dict(size=9),
        hovertemplate='<b>%{text}</b><br>' +
                     'Invented: %{x}<br>' +
                     f'Presented by: {host}<br>' +
                     '<extra></extra>'
    ))

# add vertical lines for major eras
fig.add_vline(x=1900, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="1900")
fig.add_vline(x=1920, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="Prohibition")
fig.add_vline(x=1933, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="Repeal")
fig.add_vline(x=2000, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="Craft Era")

fig.update_layout(
    title=dict(
        text='VCL Cocktail Timeline by Invention Year<br><sub>Colored by Presenter (2015-2025 Meetings)</sub>',
        font=dict(size=20)
    ),
    xaxis_title='Year Invented',
    yaxis=dict(
        showticklabels=False,
        title=''
    ),
    height=1200,
    showlegend=True,
    legend=dict(
        title="Presenter",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    hovermode='closest',
    margin=dict(l=50, r=300, t=100, b=50)
)

fig.write_html('Cocktail/Viz/cocktail_timeline.html')
print("created cocktail timeline: Cocktail/Viz/cocktail_timeline.html")

# stats
print(f"\ntotal cocktails on timeline: {len(cocktails_with_years)}")
print(f"date range: {min(c['year_invented'] for c in cocktails_with_years)} - {max(c['year_invented'] for c in cocktails_with_years)}")

print("\ncocktails per host on timeline:")
for host in sorted(by_host.keys()):
    print(f"  {host}: {len(by_host[host])}")
