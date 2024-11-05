from .momentum_strategy import MomentumStrategy
from .rebalancing_strategy import RebalancingStrategy

class StrategyFactory:
    """Factory class for creating strategy instances"""
    
    @staticmethod
    def get_available_strategies():
        """Returns list of available strategies"""
        return {
            'momentum': {
                'name': 'Momentum Strategy',
                'description': 'Identifies top and bottom performers based on returns'
            },
            'rebalancing': {
                'name': 'Rebalancing Strategy',
                'description': 'Suggests portfolio rebalancing to maintain equal weights'
            }
        }
    
    @staticmethod
    def create_strategy(strategy_id):
        """Creates and returns a strategy instance"""
        strategies = {
            'momentum': MomentumStrategy,
            'rebalancing': RebalancingStrategy
        }
        
        strategy_class = strategies.get(strategy_id)
        if not strategy_class:
            raise ValueError(f"Unknown strategy: {strategy_id}")
        
        return strategy_class()