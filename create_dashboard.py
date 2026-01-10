#!/usr/bin/env python3
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict, Counter

# load data
with open('cocktail_history.json', 'r') as f:
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
            max-width: 1400px;
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
            margin-bottom: 1rem;
            color: #333;
        }

        .viz-section p {
            color: #666;
            margin-bottom: 2rem;
        }

        .chart-container {
            width: 100%;
            min-height: 600px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🍸 VCL Cocktail Dashboard</h1>
        <p>Visualizing 10 years of cocktail presentations (2015-2025)</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="number">63</div>
            <div class="label">Total Cocktails</div>
        </div>
        <div class="stat-card">
            <div class="number">20</div>
            <div class="label">Cities of Origin</div>
        </div>
        <div class="stat-card">
            <div class="number">245</div>
            <div class="label">Years of History</div>
        </div>
        <div class="stat-card">
            <div class="number">6</div>
            <div class="label">Presenters</div>
        </div>
    </div>

    <div class="nav-tabs">
        <div class="nav-tab active" onclick="showTab('overview')">Overview</div>
        <div class="nav-tab" onclick="showTab('map')">Origin Map</div>
        <div class="nav-tab" onclick="showTab('hosts')">By Host</div>
        <div class="nav-tab" onclick="showTab('timeline')">Timeline</div>
    </div>

    <div class="content">
        <div id="overview" class="viz-section active">
            <h2>Overview</h2>
            <p>Breakdown of cocktails by liquor type and country of origin</p>
            <div id="overview-chart" class="chart-container"></div>
        </div>

        <div id="map" class="viz-section">
            <h2>Cocktail Origins Map</h2>
            <p>Geographic distribution of cocktail origins across the world</p>
            <div id="map-chart" class="chart-container"></div>
        </div>

        <div id="hosts" class="viz-section">
            <h2>Cocktails by Host</h2>
            <p>Use the buttons to view stacked by country or liquor type</p>
            <div id="hosts-chart" class="chart-container"></div>
        </div>

        <div id="timeline" class="viz-section">
            <h2>Cocktail Timeline</h2>
            <p>All cocktails plotted by invention year, colored by presenter</p>
            <div id="timeline-chart" class="chart-container"></div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // hide all sections
            document.querySelectorAll('.viz-section').forEach(section => {
                section.classList.remove('active');
            });

            // remove active from all tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // show selected section
            document.getElementById(tabName).classList.add('active');

            // activate clicked tab
            event.target.classList.add('active');
        }

        // Chart data will be inserted here
        {CHART_DATA}
    </script>
</body>
</html>
'''

# Generate all chart configurations
chart_data_js = "// Overview Chart\n"

# 1. Overview - pie charts for liquor and country
liquor_counts = df['primary_liquor'].value_counts()
country_counts = df['country_of_origin'].value_counts()

overview_fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type':'pie'}, {'type':'pie'}]],
    subplot_titles=('By Primary Liquor', 'By Country of Origin')
)

overview_fig.add_trace(
    go.Pie(labels=liquor_counts.index, values=liquor_counts.values, name="Liquor"),
    row=1, col=1
)

overview_fig.add_trace(
    go.Pie(labels=country_counts.index, values=country_counts.values, name="Country"),
    row=1, col=2
)

overview_fig.update_layout(height=600, showlegend=True)
chart_data_js += f"var overviewData = {overview_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('overview-chart', overviewData.data, overviewData.layout);\n\n"

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
        colorbar=dict(title="Number of<br>Cocktails"),
        line=dict(width=0.5, color='white')
    ),
    hovertemplate='<b>%{text}</b><extra></extra>',
    name=''
))

map_fig.update_layout(
    title='',
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
chart_data_js += "Plotly.newPlot('map-chart', mapData.data, mapData.layout);\n\n"

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
            y=1.15,
            yanchor="top",
            buttons=[
                dict(
                    label="By Country",
                    method="update",
                    args=[
                        {"visible": [True] * num_country_traces + [False] * num_liquor_traces},
                        {"title": ""}
                    ]
                ),
                dict(
                    label="By Primary Liquor",
                    method="update",
                    args=[
                        {"visible": [False] * num_country_traces + [True] * num_liquor_traces},
                        {"title": ""}
                    ]
                )
            ]
        )
    ],
    xaxis_title="Host",
    yaxis_title="Number of Cocktails",
    barmode='stack',
    height=600,
    showlegend=True,
    margin=dict(t=100)
)

chart_data_js += f"var hostsData = {hosts_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('hosts-chart', hostsData.data, hostsData.layout);\n\n"

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
        hovertemplate='<b>%{text}</b><br>Invented: %{x}<br>Presented by: ' + host + '<br><extra></extra>'
    ))

timeline_fig.add_vline(x=1900, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="1900")
timeline_fig.add_vline(x=1920, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="Prohibition")
timeline_fig.add_vline(x=1933, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="Repeal")
timeline_fig.add_vline(x=2000, line_dash="dash", line_color="gray", opacity=0.3, annotation_text="Craft Era")

timeline_fig.update_layout(
    title='',
    xaxis_title='Year Invented',
    yaxis=dict(showticklabels=False, title=''),
    height=1200,
    showlegend=True,
    hovermode='closest',
    margin=dict(l=50, r=300, t=50, b=50)
)

chart_data_js += f"var timelineData = {timeline_fig.to_json()};\n"
chart_data_js += "Plotly.newPlot('timeline-chart', timelineData.data, timelineData.layout);\n\n"

# Create final HTML
final_html = html_template.replace('{CHART_DATA}', chart_data_js)

with open('vcl_cocktail_dashboard.html', 'w') as f:
    f.write(final_html)

print("created comprehensive dashboard: vcl_cocktail_dashboard.html")
print("\nthe dashboard includes:")
print("  - overview tab: pie charts showing distribution")
print("  - origin map tab: world map of cocktail origins")
print("  - by host tab: stacked bar chart with country/liquor toggle")
print("  - timeline tab: historical timeline of all cocktails")
print("\nopen vcl_cocktail_dashboard.html in your browser to view")
