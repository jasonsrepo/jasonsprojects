import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go

class DashboardComponents:
    def __init__(self, chart_theme):
        self.chart_theme = chart_theme
    
    def create_header(self, portfolios):
        """Create dashboard header with portfolio selector"""
        return dbc.Row([
            dbc.Col([
                html.H1("Portfolio Analytics Dashboard", 
                       className="text-center mb-4 mt-4",
                       style={'color': '#00FFB3'})
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Portfolio", className="card-title", style={'color': '#00FFB3'}),
                        dcc.Dropdown(
                            id='portfolio-selector',
                            options=[{'label': p, 'value': p} for p in portfolios],
                            value=portfolios[0] if portfolios else None,
                            style={'color': 'black'}
                        )
                    ])
                ], style={'backgroundColor': 'rgba(0,0,0,0)', 'border': 'none'})
            ], width=4, style={'marginLeft' : 'auto'})
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
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Cost", className="card-title text-center", style={'color': '#00FFB3'}),
                        html.H2(f"${portfolio_summary['total_cost']:,.2f}",
                               className="text-center",
                               style={'color': '#FFFFFF'})
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Gain/Loss", className="card-title text-center", style={'color': '#00FFB3'}),
                        html.H2(f"${portfolio_summary['total_gain_loss']:,.2f}",
                               className="text-center",
                               style={'color': '#FFFFFF'})
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Overall Return", className="card-title text-center", style={'color': '#00FFB3'}),
                        html.H2(f"{portfolio_summary['total_return']:,.2f}%",
                               className="text-center",
                               style={'color': '#FFFFFF'})
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=3)
        ])
    
    def create_charts_row(self, holdings_data):
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
                            id='portfolio-composition',
                            figure=px.pie(holdings_data, 
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
                            id='sector-performance',
                            figure=self.create_sector_performance_chart(holdings_data)
                        )
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 
                                          'border': '1px solid #FFFFFF'})
            ], width=6)
        ])
    
    def create_holdings_tables(self, holdings_summary, holdings_detail):
        """Create holdings summary and detail tables"""
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Holdings Summary",
                                 style={'backgroundColor': 'rgba(0,0,0,0)', 
                                      'border-bottom': '1px solid #FFFFFF', 
                                      'color': '#00FFB3'}),
                    dbc.CardBody([
                        html.Div([
                            dbc.Table.from_dataframe(
                                holdings_summary[['Security', 'Quantity', 'Average_Cost',
                                                'Current_Price', 'Market_Value', 'Cost_Basis',
                                                'Return']].round(2),
                                striped=True,
                                bordered=True,
                                hover=True,
                                dark=True,
                                style={'color': '#FFFFFF'}
                            )
                        ])
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 
                                          'border': '1px solid #FFFFFF'})
            ], width=12),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Purchase History",
                                 style={'backgroundColor': 'rgba(0,0,0,0)', 
                                      'border-bottom': '1px solid #FFFFFF', 
                                      'color': '#00FFB3'}),
                    dbc.CardBody([
                        html.Div([
                            dbc.Table.from_dataframe(
                                holdings_detail[['Security', 'Purchase_Date', 'Quantity',
                                               'Purchase_Price', 'Current_Price',
                                               'Market_Value', 'Cost_Basis',
                                               'Return']].round(2),
                                striped=True,
                                bordered=True,
                                hover=True,
                                dark=True,
                                style={'color': '#FFFFFF'}
                            )
                        ])
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=12)
        ])
    
    def create_sector_performance_chart(self, holdings_data):
        """Create sector performance chart"""
        sector_perf = holdings_data.groupby('Sector')['Return'].mean().reset_index()
        fig = px.bar(sector_perf,
                    x='Sector',
                    y='Return',
                    title='Average Return by Sector',
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Bluyl)
        fig.update_layout(**self.chart_theme)
        return fig

    def create_strategy_section(self, available_strategies):
        """Create strategy selection and analysis section"""
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Strategy Analysis",
                                 style={'backgroundColor': 'rgba(0,0,0,0)', 
                                      'border-bottom': '1px solid #FFFFFF', 
                                      'color': '#00FFB3'}),
                    dbc.CardBody([
                        html.Div([
                            html.H5("Select Strategy", style={'color': '#00FFB3'}),
                            dcc.Dropdown(
                                id='strategy-selector',
                                options=[
                                    {'label': details['name'], 'value': strategy_id}
                                    for strategy_id, details in available_strategies.items()
                                ],
                                value='momentum',
                                style={'color': 'black', 'marginBottom': '20px'}
                            ),
                            html.Div(id='strategy-description', style={'marginBottom': '20px'}),
                            html.Div(id='strategy-results')
                        ])
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #FFFFFF'})
            ], width=12)
        ])

    def create_strategy_results(self, results):
        """Create strategy results display"""
        return html.Div([
            html.H5("Analysis Results", style={'color': '#00FFB3', 'marginBottom': '15px'}),
            html.P(results['summary'], style={'color': '#FFFFFF'}),
            html.H6("Recommendations:", style={'color': '#00FFB3', 'marginTop': '15px'}),
            html.Div([
                html.P(rec, style={'color': '#FFFFFF', 'marginBottom': '5px'})
                for rec in results['recommendations']
            ])
        ])