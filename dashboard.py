import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("data/superstore.csv")
df.columns = df.columns.str.lower().str.replace('.', '_')
df['order_date'] = pd.to_datetime(df['order_date'])

# App initialization
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Business Performance Dashboard", style={'textAlign': 'center'}),

    # Filters
    html.Div([
        dcc.Dropdown(
            id='region_filter',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            multi=True,
            placeholder="Select Region"
        ),
        dcc.Dropdown(
            id='category_filter',
            options=[{'label': c, 'value': c} for c in df['category'].unique()],
            multi=True,
            placeholder="Select Category"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    # KPI Cards
    html.Div(id='kpi_cards', style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}),

    # Charts
    dcc.Graph(id='sales_by_region'),
    dcc.Graph(id='profit_by_category'),
    dcc.Graph(id='monthly_sales')
])

# Callbacks
@app.callback(
    Output('kpi_cards', 'children'),
    Output('sales_by_region', 'figure'),
    Output('profit_by_category', 'figure'),
    Output('monthly_sales', 'figure'),
    Input('region_filter', 'value'),
    Input('category_filter', 'value')
)
def update_dashboard(region, category):
    filtered = df.copy()

    if region:
        filtered = filtered[filtered['region'].isin(region)]
    if category:
        filtered = filtered[filtered['category'].isin(category)]

    # KPIs
    total_sales = round(filtered['sales'].sum(), 2)
    total_profit = round(filtered['profit'].sum(), 2)
    total_quantity = int(filtered['quantity'].sum())

    kpis = [
        html.Div(f"Total Sales: {total_sales}", style={'fontSize': 20}),
        html.Div(f"Total Profit: {total_profit}", style={'fontSize': 20}),
        html.Div(f"Total Quantity: {total_quantity}", style={'fontSize': 20})
    ]

    # Charts
    sales_region_fig = px.bar(
        filtered.groupby('region', as_index=False)['sales'].sum(),
        x='region', y='sales',
        title='Sales by Region'
    )

    profit_category_fig = px.bar(
        filtered.groupby('category', as_index=False)['profit'].sum(),
        x='category', y='profit',
        title='Profit by Category'
    )

    monthly = filtered.resample('M', on='order_date')['sales'].sum().reset_index()
    monthly_sales_fig = px.line(
        monthly, x='order_date', y='sales',
        title='Monthly Sales Trend'
    )

    return kpis, sales_region_fig, profit_category_fig, monthly_sales_fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)
