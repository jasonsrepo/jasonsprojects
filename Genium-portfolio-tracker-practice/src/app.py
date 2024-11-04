import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    'https://fonts.googleapis.com/css2?family=Bitter:wght@400&family=Poppins:wght@300&display=swap'
                ],
                meta_tags=[{'name': 'viewport',
                          'content': 'width=device-width, initial-scale=1.0'}]
                )

# Sample data
sample_portfolio = pd.DataFrame({
    'Security': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
    'Quantity': [100, 50, 75, 25, 150],
    'Current_Price': [180.5, 2750.2, 335.8, 3300.5, 850.2],
    'Purchase_Price': [150.2, 2500.5, 300.2, 3000.8, 700.5],
    'Sector': ['Technology', 'Technology', 'Technology', 'Consumer', 'Automotive']
})

# Calculate portfolio metrics
sample_portfolio['Market_Value'] = sample_portfolio['Quantity'] * sample_portfolio['Current_Price']
sample_portfolio['Cost_Basis'] = sample_portfolio['Quantity'] * sample_portfolio['Purchase_Price']
sample_portfolio['Gain_Loss'] = sample_portfolio['Market_Value'] - sample_portfolio['Cost_Basis']
sample_portfolio['Return'] = (sample_portfolio['Gain_Loss'] / sample_portfolio['Cost_Basis'] * 100).round(2)

# Corrected chart theme
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

# Create the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Portfolio Analytics Dashboard", 
                   className="text-center mb-4 mt-4",
                   style={'color': '#00FFB3'})
        ])
    ]),
    
    # Portfolio Summary Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Value", className="card-title text-center", style={'color': '#00FFB3'}),
                    html.H2(f"${sample_portfolio['Market_Value'].sum():,.2f}", 
                           className="text-center",
                           style={'color': '#FFFFFF'})
                ])
            ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Gain/Loss", className="card-title text-center", style={'color': '#00FFB3'}),
                    html.H2(f"${sample_portfolio['Gain_Loss'].sum():,.2f}",
                           className="text-center",
                           style={'color': '#FFFFFF'})
                ])
            ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Overall Return", className="card-title text-center", style={'color': '#00FFB3'}),
                    html.H2(f"{(sample_portfolio['Gain_Loss'].sum() / sample_portfolio['Cost_Basis'].sum() * 100):,.2f}%",
                           className="text-center",
                           style={'color': '#FFFFFF'})
                ])
            ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
        ], width=4)
    ]),
    
    # Charts Row
    dbc.Row([
        # Portfolio Composition
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Portfolio Composition",
                              style={'backgroundColor': 'rgba(0,0,0,0)', 'border-bottom': '1px solid #FFFFFF', 'color': '#00FFB3'}),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.pie(sample_portfolio, 
                                    values='Market_Value', 
                                    names='Security',
                                    title='Holdings Distribution',
                                    template="plotly_dark",
                                    color_discrete_sequence=px.colors.sequential.Viridis)
                        .update_layout(**chart_theme)
                    )
                ])
            ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
        ], width=6),
        
        # Performance by Sector
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sector Performance",
                              style={'backgroundColor': 'rgba(0,0,0,0)', 'border-bottom': '1px solid #FFFFFF', 'color': '#00FFB3'}),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.bar(sample_portfolio.groupby('Sector')['Return'].mean().reset_index(),
                                    x='Sector',
                                    y='Return',
                                    title='Average Return by Sector',
                                    template="plotly_dark",
                                    color_discrete_sequence=px.colors.sequential.Viridis)
                        .update_layout(**chart_theme)
                    )
                ])
            ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
        ], width=6)
    ]),
    
    # Holdings Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Portfolio Holdings",
                              style={'backgroundColor': 'rgba(0,0,0,0)', 'border-bottom': '1px solid #FFFFFF', 'color': '#00FFB3'}),
                dbc.CardBody([
                    html.Div([
                        dbc.Table.from_dataframe(
                            sample_portfolio[['Security', 'Quantity', 'Current_Price', 
                                           'Market_Value', 'Return']].round(2),
                            striped=True,
                            bordered=True,
                            hover=True,
                            dark=True,
                            style={'color': '#FFFFFF'}
                        )
                    ])
                ])
            ], style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
        ])
    ])
    
], fluid=True, style={'backgroundColor': '#16282d', 'minHeight': '100vh', 'color': '#FFFFFF'})

if __name__ == '__main__':
    app.run_server(debug=True)