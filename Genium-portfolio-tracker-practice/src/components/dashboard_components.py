import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go

class DashboardComponents:
    def __init__(self, chart_theme):
        self.chart_theme = chart_theme
    
    def create_header(self):
        """Create dashboard header"""
        return dbc.Row([
            dbc.Col([
                html.H1("Portfolio Analytics Dashboard", 
                       className="text-center mb-4 mt-4",
                       style={'color': '#00FFB3'})
            ])
        ])
    
    def create_summary_cards(self, portfolio_summary):
        """Create summary metric cards"""
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Value", className="card-title text-center", style={'color': '#00FFB3'}),
                        html.H2(f"${portfolio_summary['total_value']:,.2f}", 
                               className="text-center",
                               style={'color': '#FFFFFF'})
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Gain/Loss", className="card-title text-center", style={'color': '#00FFB3'}),
                        html.H2(f"${portfolio_summary['total_gain_loss']:,.2f}",
                               className="text-center",
                               style={'color': '#FFFFFF'})
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Overall Return", className="card-title text-center", style={'color': '#00FFB3'}),
                        html.H2(f"{portfolio_summary['total_return']:,.2f}%",
                               className="text-center",
                               style={'color': '#FFFFFF'})
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=4)
        ])
    
    def create_charts_row(self, portfolio_data):
        """Create charts row"""
        return dbc.Row([
            # Portfolio Composition
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Portfolio Composition",
                                 style={'backgroundColor': 'rgba(0,0,0,0)', 
                                      'border-bottom': '1px solid #FFFFFF', 
                                      'color': '#00FFB3'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=px.pie(portfolio_data, 
                                        values='Market_Value', 
                                        names='Security',
                                        title='Holdings Distribution',
                                        template="plotly_dark",
                                        color_discrete_sequence=px.colors.sequential.Bluyl)
                            .update_layout(**self.chart_theme)
                        )
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 
                                          'border': '1px solid #FFFFFF'})
            ], width=6),
            
            # Sector Performance
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Sector Performance",
                                 style={'backgroundColor': 'rgba(0,0,0,0)', 
                                      'border-bottom': '1px solid #FFFFFF', 
                                      'color': '#00FFB3'}),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=self.create_sector_performance_chart(portfolio_data)
                        )
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 
                                          'border': '1px solid #FFFFFF'})
            ], width=6)
        ])
    
    def create_holdings_table(self, portfolio_data):
        """Create holdings table"""
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Portfolio Holdings",
                                 style={'backgroundColor': 'rgba(0,0,0,0)', 
                                      'border-bottom': '1px solid #FFFFFF', 
                                      'color': '#00FFB3'}),
                    dbc.CardBody([
                        html.Div([
                            dbc.Table.from_dataframe(
                                portfolio_data[['Security', 'Quantity', 'Current_Price', 
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
    
    def create_sector_performance_chart(self, portfolio_data):
        """Create sector performance chart"""
        sector_perf = portfolio_data.groupby('Sector')['Return'].mean().reset_index()
        fig = px.bar(sector_perf,
                    x='Sector',
                    y='Return',
                    title='Average Return by Sector',
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Bluyl)
        fig.update_layout(**self.chart_theme)
        return fig