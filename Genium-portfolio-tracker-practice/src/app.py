import dash
from dash import html
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
    # Header
    dashboard_components.create_header(),
    
    # Portfolio Summary Cards
    dashboard_components.create_summary_cards(portfolio_data.get_portfolio_summary()),
    
    # Charts Row
    dashboard_components.create_charts_row(portfolio_data.get_portfolio_df()),
    
    # Holdings Table
    dashboard_components.create_holdings_table(portfolio_data.get_portfolio_df())
    
], fluid=True, style={'backgroundColor': '#16282d', 'minHeight': '100vh', 'color': '#FFFFFF'})

if __name__ == '__main__':
    app.run_server(debug=True)