import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class PortfolioData:
    def __init__(self):
        # Sample data - in a real app, this would come from a database
        self.portfolio = pd.DataFrame({
            'Security': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
            'Quantity': [100, 50, 75, 25, 150],
            'Purchase_Price': [150.2, 250.5, 100.2, 500.8, 150.5],
            'Sector': ['Technology', 'Technology', 'Technology', 'Consumer', 'Automotive']
        })
        self.update_prices()
    
    def update_prices(self):
        """Update current prices using yfinance"""
        current_prices = []
        
        for ticker in self.portfolio['Security']:
            try:
                stock = yf.Ticker(ticker)
                print(f"Querying ticker: {ticker}")
                #print(f"Full info: {stock.info}")  # Print the entire info for troubleshooting
                current_price = stock.info.get('regularMarketPrice', None)
                
                if current_price is None:
                    print(f"No regularMarketPrice found for {ticker}. Attempting to fetch last close.")
                    historical_data = stock.history(period='1d')
                    current_price = historical_data['Close'].iloc[-1] if not historical_data.empty else 0
                
                print(f"Current price for {ticker}: {current_price}")
                current_prices.append(current_price)
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                current_prices.append(self._get_sample_price(ticker))
        
        self.portfolio['Current_Price'] = current_prices
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
        self.portfolio['Market_Value'] = self.portfolio['Quantity'] * self.portfolio['Current_Price']
        self.portfolio['Cost_Basis'] = self.portfolio['Quantity'] * self.portfolio['Purchase_Price']
        self.portfolio['Gain_Loss'] = self.portfolio['Market_Value'] - self.portfolio['Cost_Basis']
        self.portfolio['Return'] = (self.portfolio['Gain_Loss'] / self.portfolio['Cost_Basis'] * 100).round(2)
    
    def get_portfolio_summary(self):
        """Get summary metrics for the portfolio"""
        return {
            'total_value': self.portfolio['Market_Value'].sum(),
            'total_gain_loss': self.portfolio['Gain_Loss'].sum(),
            'total_return': (self.portfolio['Gain_Loss'].sum() / self.portfolio['Cost_Basis'].sum() * 100),
            'holdings': len(self.portfolio)
        }
    
    def get_portfolio_df(self):
        """Get the complete portfolio dataframe"""
        return self.portfolio
    
    def get_sector_allocation(self):
        """Get sector-wise allocation"""
        return self.portfolio.groupby('Sector')['Market_Value'].sum().reset_index()
    
    def get_sector_performance(self):
        """Get sector-wise performance"""
        return self.portfolio.groupby('Sector')['Return'].mean().reset_index()