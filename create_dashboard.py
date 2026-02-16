#!/usr/bin/env python3
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict, Counter

# load data
with open('Cocktail/Data/cocktail_history.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# city coordinates
city_coords = {
    'New Orleans, Louisiana': {'lat': 29.9511, 'lon': -90.0715, 'display': 'New Orleans, LA'},
    'Paris': {'lat': 48.8566, 'lon': 2.3522, 'display': 'Paris, France'},
    'USA': {'lat': 39.8283, 'lon': -98.5795, 'display': 'USA (unknown city)'},
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

# prepare location data
city_counts = Counter(entry['city_of_origin'] for entry in data)
locations = []
for city, count in city_counts.items():
    if city in city_coords:
        locations.append({
            'city': city_coords[city]['display'],
            'lat': city_coords[city]['lat'],
            'lon': city_coords[city]['lon'],
            'count': count
        })

# create HTML with all visualizations
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>VCL Cocktail Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }

        .stat-card .number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }

        .stat-card .label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .nav-tabs {
            display: flex;
            background: white;
            padding: 0 2rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            overflow-x: auto;
            justify-content: center;
        }

        .nav-tab {
            padding: 1rem 2rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            white-space: nowrap;
            font-weight: 500;
        }

        .nav-tab:hover {
            background: #f8f8f8;
        }

        .nav-tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
        }

        .content {
            max-width: 1600px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        .viz-section {
            display: none;
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .viz-section.active {
            display: block;
        }

        .viz-section h2 {
            margin-bottom: 0.5rem;
            color: #333;
            font-size: 1.8rem;
        }

        .viz-section p {
            color: #666;
            margin-bottom: 2rem;
        }

        .chart-container {
            width: 100%;
            min-height: 600px;
        }

        .overview-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }

        @media (max-width: 768px) {
            .overview-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🍸 VCL Cocktail Dashboard</h1>
        <p>visualizing 10 years of cocktail presentations (2015-2025)</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="number">63</div>
            <div class="label">total cocktails</div>
        </div>
        <div class="stat-card">
            <div class="number">20</div>
            <div class="label">cities of origin</div>
        </div>
        <div class="stat-card">
            <div class="number">245</div>
            <div class="label">years of history</div>
        </div>
        <div class="stat-card">
            <div class="number">6</div>
            <div class="label">presenters</div>
        </div>
    </div>

    <div class="nav-tabs">
        <div class="nav-tab active" onclick="showTab('overview')">overview</div>
        <div class="nav-tab" onclick="showTab('map')">origin map</div>
        <div class="nav-tab" onclick="showTab('hosts')">by host</div>
        <div class="nav-tab" onclick="showTab('timeline')">timeline</div>
    </div>

    <div class="content">
        <div id="overview" class="viz-section active">
            <h2>collection overview</h2>
            <p>breakdown of all 63 cocktails across different dimensions</p>
            <div class="overview-grid">
                <div id="liquor-chart" class="chart-container"></div>
                <div id="era-chart" class="chart-container"></div>
            </div>
        </div>

        <div id="map" class="viz-section">
            <h2>cocktail origins map</h2>
            <p>geographic distribution of cocktail origins across the world</p>
            <div id="map-chart" class="chart-container"></div>
        </div>

        <div id="hosts" class="viz-section">
            <h2>cocktails by host</h2>
            <p>use the buttons to view stacked by country or liquor type</p>
            <div id="hosts-chart" class="chart-container"></div>
        </div>

        <div id="timeline" class="viz-section">
            <h2>cocktail timeline</h2>
            <p>all cocktails plotted by invention year, colored by presenter</p>
            <div id="timeline-chart" class="chart-container"></div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            document.querySelectorAll('.viz-section').forEach(section => {
                section.classList.remove('active');
            });

            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });

            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        {CHART_DATA}
    </script>
</body>
</html>
'''

# Generate all chart configurations
chart_data_js = ""

# 1. Overview - liquor bar chart and era timeline
liquor_counts = df['primary_liquor'].value_counts().sort_values(ascending=True)

liquor_fig = go.Figure()
liquor_fig.add_trace(go.Bar(
    x=liquor_counts.values,
    y=liquor_counts.index,
    orientation='h',
    marker=dict(
        color=['#8B4513', '#87CEEB', '#E6E6FA', '#F4A460', '#FFD700', '#CD5C5C', '#808080'],
    ),
    text=liquor_counts.values,
    textposition='auto',
))

liquor_fig.update_layout(
    title='cocktails by primary liquor',
    xaxis_title='count',
    yaxis_title='',
    height=400,
    margin=dict(l=100, r=20, t=60, b=40),
    showlegend=False
)

chart_data_js += f"var liquorData = {liquor_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('liquor-chart', liquorData.data, liquorData.layout, {responsive: true});\n\n"

# Era distribution
era_counts = Counter()
for year in df['year_invented'].dropna():
    if year < 1900:
        era = '1800s'
    elif year < 1920:
        era = '1900-1919'
    elif year < 1940:
        era = '1920-1939'
    elif year < 1960:
        era = '1940-1959'
    elif year < 1980:
        era = '1960-1979'
    elif year < 2000:
        era = '1980-1999'
    else:
        era = '2000+'
    era_counts[era] += 1

era_order = ['1800s', '1900-1919', '1920-1939', '1940-1959', '1960-1979', '1980-1999', '2000+']
era_values = [era_counts.get(era, 0) for era in era_order]

era_fig = go.Figure()
era_fig.add_trace(go.Bar(
    x=era_order,
    y=era_values,
    marker=dict(
        color=era_values,
        colorscale='Purples',
    ),
    text=era_values,
    textposition='auto',
))

era_fig.update_layout(
    title='cocktails by era',
    xaxis_title='era',
    yaxis_title='count',
    height=400,
    margin=dict(l=60, r=20, t=60, b=80),
    showlegend=False
)

chart_data_js += f"var eraData = {era_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('era-chart', eraData.data, eraData.layout, {responsive: true});\n\n"

# 2. Map
map_fig = go.Figure()
map_fig.add_trace(go.Scattergeo(
    lon=[loc['lon'] for loc in locations],
    lat=[loc['lat'] for loc in locations],
    text=[f"{loc['city']}<br>{loc['count']} cocktail{'s' if loc['count'] > 1 else ''}" for loc in locations],
    mode='markers',
    marker=dict(
        size=[loc['count'] * 3 + 8 for loc in locations],
        color=[loc['count'] for loc in locations],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="cocktails"),
        line=dict(width=0.5, color='white')
    ),
    hovertemplate='<b>%{text}</b><extra></extra>',
    name=''
))

map_fig.update_layout(
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
    margin=dict(l=0, r=0, t=0, b=0)
)

chart_data_js += f"var mapData = {map_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('map-chart', mapData.data, mapData.layout, {responsive: true});\n\n"

# 3. Hosts stacked bar
country_by_host = df.groupby(['host', 'country_of_origin']).size().unstack(fill_value=0)
liquor_by_host = df.groupby(['host', 'primary_liquor']).size().unstack(fill_value=0)

hosts_fig = go.Figure()

colors_country = {
    'USA': '#1f77b4', 'France': '#ff7f0e', 'Italy': '#2ca02c', 'Cuba': '#d62728',
    'Belgium': '#9467bd', 'Scotland': '#8c564b', 'Canada': '#e377c2', 'Bermuda': '#7f7f7f',
    'British Virgin Islands': '#bcbd22', 'Mexico': '#17becf', 'UK': '#aec7e8'
}

for country in country_by_host.columns:
    hosts_fig.add_trace(go.Bar(
        name=country,
        x=country_by_host.index,
        y=country_by_host[country],
        marker_color=colors_country.get(country, '#cccccc'),
        visible=True,
        hovertemplate='<b>%{x}</b><br>' + country + ': %{y}<extra></extra>'
    ))

colors_liquor = {
    'whiskey': '#8B4513', 'gin': '#87CEEB', 'vodka': '#E6E6FA', 'rum': '#F4A460',
    'tequila': '#FFD700', 'brandy': '#CD5C5C', 'other': '#808080'
}

for liquor in liquor_by_host.columns:
    hosts_fig.add_trace(go.Bar(
        name=liquor,
        x=liquor_by_host.index,
        y=liquor_by_host[liquor],
        marker_color=colors_liquor.get(liquor, '#cccccc'),
        visible=False,
        hovertemplate='<b>%{x}</b><br>' + liquor + ': %{y}<extra></extra>'
    ))

num_country_traces = len(country_by_host.columns)
num_liquor_traces = len(liquor_by_host.columns)

hosts_fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.5,
            xanchor="center",
            y=1.12,
            yanchor="top",
            buttons=[
                dict(
                    label="by country",
                    method="update",
                    args=[
                        {"visible": [True] * num_country_traces + [False] * num_liquor_traces},
                        {"title": ""}
                    ]
                ),
                dict(
                    label="by liquor",
                    method="update",
                    args=[
                        {"visible": [False] * num_country_traces + [True] * num_liquor_traces},
                        {"title": ""}
                    ]
                )
            ]
        )
    ],
    xaxis_title="host",
    yaxis_title="cocktails",
    barmode='stack',
    height=600,
    showlegend=True,
    margin=dict(l=60, r=20, t=80, b=60)
)

chart_data_js += f"var hostsData = {hosts_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('hosts-chart', hostsData.data, hostsData.layout, {responsive: true});\n\n"

# 4. Timeline
cocktails_with_years = [c for c in data if c.get('year_invented')]
cocktails_with_years.sort(key=lambda x: x['year_invented'])

host_colors = {
    'Chris': '#1f77b4', 'Joe': '#ff7f0e', 'John': '#2ca02c',
    'Lucas': '#d62728', 'Adam': '#9467bd', 'Eric': '#8c564b'
}

by_host = defaultdict(list)
for cocktail in cocktails_with_years:
    by_host[cocktail['host']].append(cocktail)

timeline_fig = go.Figure()

for host in sorted(by_host.keys()):
    cocktails = by_host[host]
    timeline_fig.add_trace(go.Scatter(
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
        hovertemplate='<b>%{text}</b><br>invented: %{x}<br>presented by: ' + host + '<br><extra></extra>'
    ))

timeline_fig.add_vline(x=1900, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="1900")
timeline_fig.add_vline(x=1920, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="prohibition")
timeline_fig.add_vline(x=1933, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="repeal")
timeline_fig.add_vline(x=2000, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="craft era")

timeline_fig.update_layout(
    title='',
    xaxis_title='year invented',
    yaxis=dict(showticklabels=False, title=''),
    height=1200,
    showlegend=True,
    hovermode='closest',
    margin=dict(l=60, r=300, t=20, b=60)
)

chart_data_js += f"var timelineData = {timeline_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('timeline-chart', timelineData.data, timelineData.layout, {responsive: true});\n\n"

# Create final HTML
final_html = html_template.replace('{CHART_DATA}', chart_data_js)

with open('Cocktail/Viz/vcl_cocktail_dashboard.html', 'w') as f:
    f.write(final_html)

print("created improved dashboard: Cocktail/Viz/vcl_cocktail_dashboard.html")
print("\nfixed issues:")
print("  - better overview: liquor bar chart + era distribution")
print("  - proper chart sizing: all charts now use full width")
print("  - responsive layout for all screen sizes")
