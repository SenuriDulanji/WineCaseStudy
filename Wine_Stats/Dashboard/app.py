import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Load the wine data
data = pd.read_csv("Cleared winestats.csv")

# List of food columns (everything after Country_region)
food_columns = list(data.columns)
region_index = food_columns.index('Country_region')
food_columns = food_columns[region_index + 1:]  # food columns start after Region

external_stylesheets = [
    {
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "🍷 Wine Analytics"

# Define layout
app.layout = html.Div([
    html.Img(src='./assets/wine.jpg', className="header-image"),
    html.H1("Wine Analytics", className="header-title"),
    html.P("Explore the highest-rated wines by country. Discover which wine names stand out!", className="header-description"),

    # Dropdowns in dashboard

    #Country Dropdown
    html.Div([
        html.Label('Select a Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in sorted(data['Country'].unique())],
            placeholder="Select a Country"
        )
    ], style={'margin-bottom': '20px'}),

    #Region Dropdown
    html.Div([
        html.Label('Select a Region:'),
        dcc.Dropdown(
            id='region-dropdown',
            placeholder="Select a Region"
        )
    ], style={'margin-bottom': '20px'}),


    # Graphs
    dcc.Graph(id='Alcohol-content-graph'),
    dcc.Graph(id='Number-of-Ratings-graph'),
    dcc.Graph(id='scatter1-graph'),
    dcc.Graph(id='scatter2-graph'),
    dcc.Graph(id='boxplot-graph'),

    #Wine Dropdown
    html.Div([
        html.Label('Select a Wine:'),
        dcc.Dropdown(
            id='wine-dropdown',
            placeholder="Select a Wine Name"
        )
    ], style={'margin-bottom': '20px'}),
    dcc.Graph(id='taste-pie-chart'),

    #Winery DropDown
    html.Div([
        html.Label('Select a Winery:'),
        dcc.Dropdown(
            id='winery-dropdown',
            placeholder="Select a Winery"
        )
    ], style={'margin-bottom': '20px'}),
    html.Div(id='country-food-suggestions'),

    #Graphs
    dcc.Graph(id='food-heatmap'),
    dcc.Graph(id='top-foods-bar-chart'),
], className="container")


# Update regions when a country is selected
@app.callback(
    Output('region-dropdown', 'options'),
    Input('country-dropdown', 'value')
)
def update_region_dropdown(selected_country):
    if selected_country:
        filtered_data = data[data['Country'] == selected_country]
        regions = filtered_data['Country_region'].apply(lambda x: str(x).strip().title()).unique()
        return [{'label': region, 'value': region} for region in sorted(regions)]
    return []

# Update wineries when a country and region are selected
@app.callback(
    Output('winery-dropdown', 'options'),
    [Input('country-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_winery_dropdown(selected_country, selected_region):
    if selected_country:
        filtered_data = data[data['Country'] == selected_country]
        if selected_region:
            filtered_data = filtered_data[filtered_data['Country_region'].astype(str).apply(lambda x: x.strip().title()) == selected_region]
        wineries = filtered_data['Winery'].unique()
        return [{'label': winery, 'value': winery} for winery in sorted(wineries)]
    return []

# Update wines when a country and region are selected
@app.callback(
    Output('wine-dropdown', 'options'),
    [Input('country-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_wine_dropdown(selected_country, selected_region):
    if selected_country:
        filtered_data = data[data['Country'] == selected_country]
        if selected_region:
            filtered_data = filtered_data[filtered_data['Country_region'].astype(str).apply(lambda x: x.strip().title()) == selected_region]
        wines = filtered_data['Name'].unique()
        return [{'label': wine, 'value': wine} for wine in sorted(wines)]
    return []


@app.callback(
    [Output('Alcohol-content-graph', 'figure'),
     Output('Number-of-Ratings-graph', 'figure'),
     Output('scatter1-graph', 'figure'),
     Output('scatter2-graph', 'figure'),
     Output('boxplot-graph', 'figure'),
     Output('taste-pie-chart', 'figure'),
     Output('country-food-suggestions', 'children'),
     Output('food-heatmap', 'figure'),
     Output('top-foods-bar-chart', 'figure')],
    
    [Input('country-dropdown', 'value'),
     Input('region-dropdown', 'value'),
     Input('wine-dropdown', 'value'),
     Input('winery-dropdown', 'value')]
)

def update_graphs(selected_country, selected_region, selected_wine, selected_winery):
    filtered_data = data[data["Country"] == selected_country]

    if selected_region:
        filtered_data = filtered_data[
            filtered_data["Country_region"].astype(str).apply(lambda x: x.strip().title()) == selected_region
        ]

    if selected_winery:
        winery_data = filtered_data[filtered_data["Winery"] == selected_winery]
    else:
        winery_data = filtered_data

    # Alcohol content graph
    AlcoholContent_figure = {
        "data": [
            go.Scatter(
                x=filtered_data["Name"],
                y=filtered_data["Alcohol content"],
                mode='lines+markers',
                line=dict(color='purple'),
                name='Alcohol content'
            )
        ],
        "layout": go.Layout(
            title=f"Alcohol Content of Wines in {selected_country}",
            xaxis_title="Wine Name",
            yaxis_title="Alcohol Content (%)",
        )
    }

    # Number of ratings graph
    noOfRating_figure = {
        "data": [
            go.Scatter(
                x=filtered_data["Name"],
                y=filtered_data["Number of Ratings"],
                mode='lines+markers',
                line=dict(color='red'),
                name='Number of Ratings'
            )
        ],
        "layout": go.Layout(
            title=f"Popularity of Wines in {selected_country}",
            xaxis_title="Wine Name",
            yaxis_title="Number of Ratings",
        )
    }

    # Scatter plot Rating vs Price
    scatter1_figure = {
        "data": [
            go.Scatter(
                x=filtered_data["Rating"],
                y=filtered_data["Price"],
                mode='markers',
                marker=dict(color='purple', size=8, opacity=0.7, line=dict(width=1, color='black')),
                text=filtered_data["Name"],
                hovertemplate="Wine: %{text}<br>Rating: %{x}<br>Price: $%{y:.2f}<extra></extra>",
                name="Wines"
            )
        ],
        "layout": go.Layout(
            title=f"Wine Rating vs Price in {selected_country}",
            xaxis_title="Rating",
            yaxis_title="Price (USD)",
            hovermode="closest"
        )
    }

     # Scatter plot Alcohol Content vs Price
    scatter2_figure = {
        "data": [
            go.Scatter(
                x=filtered_data["Alcohol content"],
                y=filtered_data["Price"],
                mode='markers',
                marker=dict(color='purple', size=8, opacity=0.7, line=dict(width=1, color='black')),
                text=filtered_data["Name"],
                hovertemplate="Wine: %{text}<br>Alcohol content: %{x}<br>Price: $%{y:.2f}<extra></extra>",
                name="Wines"
            )
        ],
        "layout": go.Layout(
            title=f"Alcohol content vs Price in {selected_country}",
            xaxis_title="Alcohol content",
            yaxis_title="Price (USD)",
            hovermode="closest"
        )
    }

    # Boxplot for Price Distribution
    price_figure = {
        "data": [
            go.Box(
                y=filtered_data["Price"],
                name=selected_country,
                boxpoints='all',
                jitter=0.5,
                pointpos=-1.8,
                marker=dict(color='orange'),
                line=dict(color='black')
            )
        ],
        "layout": go.Layout(
            title=f"Wine Price Distribution in {selected_country}",
            yaxis_title="Price (USD)",
            showlegend=False
        )
    }

    # Taste Pie Chart
    if selected_wine:
        wine_data = filtered_data[filtered_data['Name'] == selected_wine]
        if not wine_data.empty:
            wine_row = wine_data.iloc[0]
            labels = ['Bold', 'Tannin', 'Sweet', 'Acidic']
            values = [wine_row['Bold'], wine_row['Tannin'], wine_row['Sweet'], wine_row['Acidic']]

            pie_figure = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
            pie_figure.update_layout(title_text=f"Taste Profile: {selected_wine}")
        else:
            pie_figure = go.Figure()
    else:
        pie_figure = go.Figure()

    # Food Suggestions
    food_suggestions = []
    for food in food_columns:
        if (winery_data[food] == True).any():
            food_suggestions.append(food)

    if not food_suggestions:
        food_suggestions_div = html.Div(f"No food suggestions for {selected_winery or selected_country}.", className="food-suggestions")
    else:
        food_suggestions_div = html.Div([
            html.H4(f"🍷 Food Suggestions for {selected_winery or selected_country}:", className="food-suggestions-h4"),
            html.Ul([html.Li(food) for food in food_suggestions])
        ], style={"marginTop": "20px"}, className="food-suggestions")


    # Food Heatmap
    heatmap_data = data.groupby('Country')[food_columns].sum()

    heatmap_figure = px.imshow(
        heatmap_data.T,
        labels=dict(x="Country", y="Food", color="Number of Wines"),
        color_continuous_scale="Reds",
        aspect="auto",
    )

    heatmap_figure.update_layout(
        title="🍽️ Food Pairing Popularity Across Countries",
        xaxis_title="Country",
        yaxis_title="Food",
        autosize=True,
        height=700,
    )

    # Top 5 Foods Bar Chart
    food_counts = filtered_data[food_columns].sum()
    top_foods = food_counts.sort_values(ascending=False).head(5)

    bar_figure = go.Figure(data=[
        go.Bar(
            x=top_foods.index,
            y=top_foods.values,
            marker_color='indianred'
        )
    ])

    bar_figure.update_layout(
        title=f"🍽️ Top 5 Food Pairings for Wines from {selected_country}",
        xaxis_title="Food",
        yaxis_title="Number of Wines",
        height=500,
    )

    return AlcoholContent_figure, noOfRating_figure,scatter1_figure, scatter2_figure, price_figure, pie_figure, food_suggestions_div, heatmap_figure, bar_figure

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
