import numpy as np
import random
from mesa import Agent, Model, DataCollector
from mesa.space import MultiGrid

class ProspectTheoryAgent(Agent):
    """
    An agent that makes decisions according to prospect theory
    """
    
    def __init__(self, unique_id, model, agent_type='behavioral', 
                 alpha=0.88, beta=0.88, lambda_param=2.25, gamma=0.61):
        super().__init__(unique_id, model)
        self.agent_type = agent_type
        self.wealth = 100.0
        self.reference_point = self.wealth
        self.alpha = alpha
        self.beta = beta
        self.lambda_param = lambda_param
        self.gamma = gamma
        self.holdings = 0
        self.last_price = None
        
    def prospect_value(self, outcome):
        """Calculate prospect theory value for an outcome"""
        if outcome >= 0:
            return outcome ** self.alpha
        else:
            return -self.lambda_param * ((-outcome) ** self.beta)
    
    def probability_weight(self, prob):
        """Apply probability weighting function"""
        if prob <= 0:
            return 0
        if prob >= 1:
            return 1
        return (prob ** self.gamma) / ((prob ** self.gamma + (1 - prob) ** self.gamma) ** (1 / self.gamma))
    
    def evaluate_trade(self, current_price, fundamental_value):
        """Evaluate whether to buy, sell, or hold"""
        if self.agent_type == 'rational':
            return self.rational_decision(current_price, fundamental_value)
        else:
            return self.behavioral_decision(current_price, fundamental_value)
    
    def rational_decision(self, current_price, fundamental_value):
        """Make rational decision based on fundamental value"""
        if fundamental_value > current_price * 1.02:
            return 'buy'
        elif fundamental_value < current_price * 0.98:
            return 'sell'
        else:
            return 'hold'
    
    def behavioral_decision(self, current_price, fundamental_value):
        """Make behavioral decision using prospect theory"""
        if self.holdings > 0:
            gain_loss = current_price - self.reference_point
            
            if gain_loss > 0:
                sell_utility = self.prospect_value(gain_loss)
                hold_utility = self.probability_weight(0.6) * self.prospect_value(gain_loss * 1.1)
                if sell_utility > hold_utility:
                    return 'sell'
            else:
                sell_utility = self.prospect_value(gain_loss)
                hold_utility = self.probability_weight(0.4) * self.prospect_value(gain_loss * 0.9)
                if hold_utility > sell_utility:
                    return 'hold'
                else:
                    return 'sell'
        
        else:
            expected_gain = fundamental_value - current_price
            buy_utility = self.probability_weight(0.6) * self.prospect_value(expected_gain)
            
            if buy_utility > 0 and self.wealth >= current_price:
                return 'buy'
        
        return 'hold'
    
    def execute_trade(self, action, price):
        """Execute the trading decision"""
        if action == 'buy' and self.wealth >= price and self.holdings == 0:
            self.wealth -= price
            self.holdings = 1
            self.reference_point = price
            return 1
        elif action == 'sell' and self.holdings > 0:
            self.wealth += price
            self.holdings = 0
            return -1
        return 0
    
    def step(self):
        """Agent step function"""
        current_price = self.model.current_price
        fundamental_value = self.model.fundamental_value
        
        action = self.evaluate_trade(current_price, fundamental_value)
        trade_volume = self.execute_trade(action, current_price)
        
        self.model.total_volume += abs(trade_volume)
        
        if self.last_price is not None and self.agent_type == 'anchored':
            self.reference_point = 0.7 * self.reference_point + 0.3 * self.last_price
        
        self.last_price = current_price

class BehavioralMarket(Model):
    """
    A market model with behavioral and rational agents
    """
    
    def __init__(self, n_agents=100, behavioral_fraction=0.8, fundamental_volatility=0.1):
        super().__init__()
        self.n_agents = n_agents
        self.behavioral_fraction = behavioral_fraction
        self.fundamental_volatility = fundamental_volatility
        
        self.schedule = self
        
        self.fundamental_value = 100.0
        self.current_price = 100.0
        self.total_volume = 0
        
        self.price_history = [self.current_price]
        self.fundamental_history = [self.fundamental_value]
        self.volume_history = [0]
        
        for i in range(self.n_agents):
            if i < int(n_agents * behavioral_fraction):
                agent_type = random.choice(['prospect_theory', 'loss_averse', 'anchored'])
                alpha = np.random.normal(0.88, 0.1)
                beta = np.random.normal(0.88, 0.1)
                lambda_param = np.random.normal(2.25, 0.5)
                gamma = np.random.normal(0.61, 0.1)
            else:
                agent_type = 'rational'
                alpha = beta = lambda_param = gamma = 1.0
            
            agent = ProspectTheoryAgent(i, self, agent_type, 
                                     max(0.1, alpha), max(0.1, beta), 
                                     max(1.0, lambda_param), max(0.1, min(1.0, gamma)))
            self.agents.append(agent)
        
        self.datacollector = DataCollector(
            model_reporters={
                "Price": "current_price",
                "Fundamental": "fundamental_value", 
                "Volume": "total_volume",
                "Mispricing": lambda m: abs(m.current_price - m.fundamental_value)
            }
        )
    
    def update_price(self):
        """Update market price based on supply and demand"""
        buy_pressure = sum(1 for agent in self.agents 
                          if agent.evaluate_trade(self.current_price, self.fundamental_value) == 'buy')
        sell_pressure = sum(1 for agent in self.agents 
                           if agent.evaluate_trade(self.current_price, self.fundamental_value) == 'sell')
        
        net_pressure = (buy_pressure - sell_pressure) / self.n_agents
        
        price_change = net_pressure * 0.1 * self.current_price
        noise = np.random.normal(0, 0.01 * self.current_price)
        
        self.current_price = max(1.0, self.current_price + price_change + noise)
    
    def update_fundamental(self):
        """Update fundamental value with random walk"""
        change = np.random.normal(0, self.fundamental_volatility * self.fundamental_value)
        self.fundamental_value = max(1.0, self.fundamental_value + change)
    
    def step(self):
        """Model step function"""
        self.total_volume = 0
        
        self.update_fundamental()
        for agent in self.agents:
            agent.step()
        self.update_price()
        
        self.price_history.append(self.current_price)
        self.fundamental_history.append(self.fundamental_value)
        self.volume_history.append(self.total_volume)
        
        self.datacollector.collect(self)
    
    def simulate(self, n_periods):
        """Run simulation for n periods"""
        for _ in range(n_periods):
            self.step()
        
        return {
            'prices': self.price_history,
            'fundamentals': self.fundamental_history,
            'volumes': self.volume_history
        }
