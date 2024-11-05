import dash
from dash import html, Input, Output
import dash_bootstrap_components as dbc
from components.dashboard_components import DashboardComponents
from data.portfolio_data import PortfolioData

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    'https://fonts.googleapis.com/css2?family=Bitter:wght@400&family=Poppins:wght@300&display=swap'
                ],
                meta_tags=[{'name': 'viewport',
                          'content': 'width=device-width, initial-scale=1.0'}]
                )

# Chart theme settings
chart_theme = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {
        'color': '#FFFFFF',
        'family': 'Bitter'
    },
    'xaxis': {
        'gridcolor': 'rgba(255,255,255,0.1)',
        'color': '#FFFFFF'
    },
    'yaxis': {
        'gridcolor': 'rgba(255,255,255,0.1)',
        'color': '#FFFFFF'
    }
}

# Initialize components
portfolio_data = PortfolioData()
dashboard_components = DashboardComponents(chart_theme)

# Create layout
app.layout = dbc.Container([
    # Header with Portfolio Selector
    dashboard_components.create_header(portfolio_data.get_portfolios()),
    
    # Portfolio Summary Cards
    html.Div(id='summary-cards'),
    
    # Charts Row
    html.Div(id='charts-row'),
    
    # Holdings Tables
    html.Div(id='holdings-tables'),

    html.Br()
    
], fluid=True, style={'backgroundColor': '#16282d', 'minHeight': '100vh', 'color': '#FFFFFF'})

# Callback for updating summary cards
@app.callback(
    Output('summary-cards', 'children'),
    [Input('portfolio-selector', 'value')]
)
def update_summary_cards(selected_portfolio):
    summary = portfolio_data.get_portfolio_summary(selected_portfolio)
    return dashboard_components.create_summary_cards(summary)

# Callback for updating charts
@app.callback(
    Output('charts-row', 'children'),
    [Input('portfolio-selector', 'value')]
)
def update_charts(selected_portfolio):
    holdings_data = portfolio_data.get_holdings_summary(selected_portfolio)
    return dashboard_components.create_charts_row(holdings_data)

# Callback for updating holdings tables
@app.callback(
    Output('holdings-tables', 'children'),
    [Input('portfolio-selector', 'value')]
)
def update_holdings_tables(selected_portfolio):
    holdings_summary = portfolio_data.get_holdings_summary(selected_portfolio)
    holdings_detail = portfolio_data.get_holdings_detail(selected_portfolio)
    return dashboard_components.create_holdings_tables(holdings_summary, holdings_detail)

if __name__ == '__main__':
    app.run_server(debug=True)