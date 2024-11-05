from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """Base class for all portfolio strategies"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    @abstractmethod
    def analyze(self, holdings_data):
        """
        Analyze holdings data and return signals/recommendations
        
        Args:
            holdings_data (pd.DataFrame): Holdings data with columns for Security, 
                                        Current_Price, Average_Cost, Return, etc.
        
        Returns:
            dict: Analysis results including recommendations and metrics
        """
        pass