from .base_strategy import BaseStrategy
import pandas as pd

class RebalancingStrategy(BaseStrategy):
    """Simple equal-weight rebalancing strategy"""
    
    def __init__(self):
        super().__init__(
            name="Rebalancing Strategy",
            description="Suggests portfolio rebalancing to maintain equal weights"
        )
    
    def analyze(self, holdings_data):

        # Make copy to remove warning
        holdings_data = holdings_data.copy()

        print(holdings_data)

        # Calculate current weights
        total_value = holdings_data['Market_Value'].sum()
        holdings_data['Current_Weight'] = (holdings_data['Market_Value'] / total_value * 100).round(2)
        
        # Calculate target weight (equal-weight)
        target_weight = round(100 / len(holdings_data), 2)
        
        # Calculate weight difference
        holdings_data['Weight_Diff'] = holdings_data['Current_Weight'] - target_weight
        
        # Sort by absolute weight difference
        rebalance_needs = holdings_data.sort_values('Weight_Diff', key=abs, ascending=False)
        
        # Get positions needing significant rebalancing (>2% difference)
        significant_diff = rebalance_needs[abs(rebalance_needs['Weight_Diff']) > 2]
        
        return {
            'summary': f"Target weight per position: {target_weight:.2f}%",
            'recommendations': [
                "Positions requiring rebalancing:",
                *[f"- {row['Security']}: {row['Current_Weight']:.2f}% "
                  f"({'increase' if row['Weight_Diff'] < 0 else 'decrease'} "
                  f"by {abs(row['Weight_Diff']):.2f}%)"
                  for _, row in significant_diff.iterrows()]
            ],
            'metrics': {
                'target_weight': target_weight,
                'rebalance_needs': significant_diff[['Security', 'Current_Weight', 'Weight_Diff']].to_dict('records')
            }
        }