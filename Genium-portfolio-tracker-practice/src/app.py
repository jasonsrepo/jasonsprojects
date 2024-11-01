import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                          'content': 'width=device-width, initial-scale=1.0'}]
                )

# Create the basic layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Portfolio Analytics Dashboard", 
                   className="text-center mb-4 mt-4")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div("Welcome to the Portfolio Analytics Dashboard", 
                    className="text-center")
        ])
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
