from .base_strategy import BaseStrategy
import pandas as pd

class MomentumStrategy(BaseStrategy):
    """Simple momentum strategy based on returns"""
    
    def __init__(self):
        super().__init__(
            name="Momentum Strategy",
            description="Identifies top and bottom performers based on returns"
        )
    
    def analyze(self, holdings_data):
        # Sort holdings by return
        sorted_holdings = holdings_data.sort_values('Return', ascending=False)
        
        # Get top and bottom performers
        top_performers = sorted_holdings.head(2)
        bottom_performers = sorted_holdings.tail(2)
        
        # Calculate average return
        avg_return = holdings_data['Return'].mean()
        
        return {
            'summary': f"Average portfolio return: {avg_return:.2f}%",
            'recommendations': [
                "Consider increasing positions in top performers:",
                *[f"- {row['Security']} ({row['Return']:.2f}%)" 
                  for _, row in top_performers.iterrows()],
                "\nConsider reducing exposure to underperformers:",
                *[f"- {row['Security']} ({row['Return']:.2f}%)" 
                  for _, row in bottom_performers.iterrows()]
            ],
            'metrics': {
                'avg_return': avg_return,
                'top_performers': top_performers[['Security', 'Return']].to_dict('records'),
                'bottom_performers': bottom_performers[['Security', 'Return']].to_dict('records')
            }
        }