import pandas as pd
import yfinance as yf
from datetime import datetime

class PortfolioData:
    def __init__(self):
        # Sample data structure with multiple portfolios and purchase history
        self.holdings = pd.DataFrame({
            'Portfolio': [
                'Growth', 'Growth', 'Growth', 'Growth', 'Growth', 'Growth',
                'Income', 'Income', 'Income', 'Income', 'Income', 'Income',
                'Speculative', 'Speculative', 'Speculative', 'Speculative', 'Speculative', 'Speculative'
            ],
            'Security': [
                'AAPL', 'AAPL', 'GOOGL', 'META', 'NVDA', 'NFLX',            # Growth
                'MSFT', 'JNJ', 'PEP', 'PG', 'T', 'VZ',                       # Income
                'TSLA', 'AMZN', 'RIVN', 'SPCE', 'PLTR', 'BYND'              # Speculative
            ],
            'Purchase_Date': [
                '2023-01-15', '2023-06-20', '2023-03-10', '2023-07-12', '2023-02-25', '2023-04-18',   # Growth
                '2023-02-01', '2023-05-20', '2023-09-15', '2023-08-12', '2023-06-05', '2023-03-22',   # Income
                '2023-04-01', '2023-05-15', '2023-07-01', '2023-09-07', '2023-10-02', '2023-08-11'    # Speculative
            ],
            'Quantity': [
                50, 50, 50, 40, 75, 30,           # Growth
                50, 100, 80, 60, 200, 120,        # Income
                150, 25, 60, 500, 300, 80         # Speculative
            ],
            'Purchase_Price': [
                150.2, 175.5, 250.5, 320.7, 180.3, 450.6,        # Growth
                100.2, 175.8, 160.4, 143.2, 27.5, 35.1,          # Income
                150.5, 500.8, 70.2, 6.5, 22.3, 105.5             # Speculative
            ],
            'Sector': [
                'Technology', 'Technology', 'Technology', 'Technology', 'Technology', 'Entertainment',  # Growth
                'Technology', 'Healthcare', 'Consumer', 'Consumer', 'Telecom', 'Telecom',              # Income
                'Automotive', 'Consumer', 'Automotive', 'Aerospace', 'Technology', 'Consumer'         # Speculative
            ]
        })
        
        # Convert date string to datetime
        self.holdings['Purchase_Date'] = pd.to_datetime(self.holdings['Purchase_Date'])
        
        # Calculate cost basis for each purchase
        self.holdings['Cost_Basis'] = self.holdings['Quantity'] * self.holdings['Purchase_Price']
        
        self.update_prices()
    
    def update_prices(self):
        """Update current prices using yfinance"""
        unique_tickers = self.holdings['Security'].unique()
        current_prices = {}
        
        for ticker in unique_tickers:
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.info.get('regularMarketPrice', None)
                
                if current_price is None:
                    historical_data = stock.history(period='1d')
                    current_price = historical_data['Close'].iloc[-1] if not historical_data.empty else 0
                
                current_prices[ticker] = current_price
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                current_prices[ticker] = self._get_sample_price(ticker)
        
        # Add current prices to holdings
        self.holdings['Current_Price'] = self.holdings['Security'].map(current_prices)
        self._calculate_metrics()
    
    def _get_sample_price(self, ticker):
        """Fallback sample prices"""
        sample_prices = {
            'AAPL': 180.5,
            'GOOGL': 2750.2,
            'MSFT': 335.8,
            'AMZN': 3300.5,
            'TSLA': 850.2
        }
        return sample_prices.get(ticker, 0)
    
    def _calculate_metrics(self):
        """Calculate portfolio metrics"""
        self.holdings['Market_Value'] = self.holdings['Quantity'] * self.holdings['Current_Price']
        self.holdings['Gain_Loss'] = self.holdings['Market_Value'] - self.holdings['Cost_Basis']
        self.holdings['Return'] = (self.holdings['Gain_Loss'] / self.holdings['Cost_Basis'] * 100).round(2)
        
        # Calculate aggregated holdings by security and portfolio
        self.aggregated_holdings = self.holdings.groupby(['Portfolio', 'Security', 'Sector']).agg({
            'Quantity': 'sum',
            'Cost_Basis': 'sum',
            'Market_Value': 'sum',
            'Gain_Loss': 'sum',
            'Current_Price': 'last'  # Take the most recent price
        }).reset_index()
        
        self.aggregated_holdings['Return'] = (
            self.aggregated_holdings['Gain_Loss'] / self.aggregated_holdings['Cost_Basis'] * 100
        ).round(2)
        
        self.aggregated_holdings['Average_Cost'] = (
            self.aggregated_holdings['Cost_Basis'] / self.aggregated_holdings['Quantity']
        ).round(2)
    
    def get_portfolios(self):
        """Get list of available portfolios"""
        return sorted(self.holdings['Portfolio'].unique())
    
    def get_portfolio_summary(self, portfolio=None):
        """Get summary metrics for the selected portfolio"""
        data = self.holdings if portfolio is None else self.holdings[self.holdings['Portfolio'] == portfolio]
        
        return {
            'total_value': data['Market_Value'].sum(),
            'total_gain_loss': data['Gain_Loss'].sum(),
            'total_cost': data['Cost_Basis'].sum(),
            'total_return': (data['Gain_Loss'].sum() / data['Cost_Basis'].sum() * 100).round(2),
            'holdings': len(data['Security'].unique())
        }
    
    def get_holdings_summary(self, portfolio=None):
        """Get aggregated holdings for the selected portfolio"""
        if portfolio is None:
            return self.aggregated_holdings
        return self.aggregated_holdings[self.aggregated_holdings['Portfolio'] == portfolio]
    
    def get_holdings_detail(self, portfolio=None):
        """Get detailed holdings with purchase history"""
        if portfolio is None:
            return self.holdings
        return self.holdings[self.holdings['Portfolio'] == portfolio]
    
    def get_sector_allocation(self, portfolio=None):
        """Get sector-wise allocation for selected portfolio"""
        data = self.get_holdings_summary(portfolio)
        return data.groupby('Sector')['Market_Value'].sum().reset_index()
    
    def get_sector_performance(self, portfolio=None):
        """Get sector-wise performance for selected portfolio"""
        data = self.get_holdings_summary(portfolio)
        return data.groupby('Sector')['Return'].mean().reset_index()