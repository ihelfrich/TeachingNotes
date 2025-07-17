import numpy as np
import matplotlib.pyplot as plt
from prospect_theory_agents import BehavioralMarket

def run_market_comparison(n_periods=100, n_runs=10):
    """
    Compare markets with different behavioral compositions
    """
    behavioral_fractions = [0.0, 0.2, 0.5, 0.8, 1.0]
    results = {}
    
    for frac in behavioral_fractions:
        mispricings = []
        volatilities = []
        volumes = []
        
        for run in range(n_runs):
            np.random.seed(run)
            market = BehavioralMarket(n_agents=100, behavioral_fraction=frac)
            data = market.simulate(n_periods)
            
            prices = np.array(data['prices'])
            fundamentals = np.array(data['fundamentals'])
            
            mispricing = np.mean(np.abs(prices - fundamentals))
            volatility = np.std(np.diff(prices) / prices[:-1])
            volume = np.mean(data['volumes'])
            
            mispricings.append(mispricing)
            volatilities.append(volatility)
            volumes.append(volume)
        
        results[frac] = {
            'mispricing': np.mean(mispricings),
            'volatility': np.mean(volatilities),
            'volume': np.mean(volumes),
            'mispricing_std': np.std(mispricings),
            'volatility_std': np.std(volatilities),
            'volume_std': np.std(volumes)
        }
    
    return results

def plot_market_comparison(results):
    """
    Plot comparison of market efficiency metrics
    """
    fractions = list(results.keys())
    mispricings = [results[f]['mispricing'] for f in fractions]
    volatilities = [results[f]['volatility'] for f in fractions]
    volumes = [results[f]['volume'] for f in fractions]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    ax1.plot(fractions, mispricings, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Fraction of Behavioral Agents')
    ax1.set_ylabel('Average Mispricing')
    ax1.set_title('Market Efficiency vs Behavioral Composition')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(fractions, volatilities, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('Fraction of Behavioral Agents')
    ax2.set_ylabel('Price Volatility')
    ax2.set_title('Volatility vs Behavioral Composition')
    ax2.grid(True, alpha=0.3)
    
    ax3.plot(fractions, volumes, 'go-', linewidth=2, markersize=8)
    ax3.set_xlabel('Fraction of Behavioral Agents')
    ax3.set_ylabel('Trading Volume')
    ax3.set_title('Volume vs Behavioral Composition')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def analyze_agent_performance(market):
    """
    Analyze performance differences between agent types
    """
    agent_performance = {}
    
    for agent in market.agents:
        agent_type = agent.agent_type
        if agent_type not in agent_performance:
            agent_performance[agent_type] = []
        agent_performance[agent_type].append(agent.wealth)
    
    results = {}
    for agent_type, wealths in agent_performance.items():
        results[agent_type] = {
            'mean_wealth': np.mean(wealths),
            'std_wealth': np.std(wealths),
            'count': len(wealths)
        }
    
    return results

def simulate_crisis_scenario(n_agents=100, crisis_period=50):
    """
    Simulate market behavior during a crisis (fundamental value drop)
    """
    market = BehavioralMarket(n_agents=n_agents, behavioral_fraction=0.8)
    
    normal_periods = 30
    for _ in range(normal_periods):
        market.step()
    
    market.fundamental_value *= 0.7
    
    crisis_periods = 20
    for _ in range(crisis_periods):
        market.step()
    
    recovery_periods = 30
    market.fundamental_volatility *= 0.5
    for _ in range(recovery_periods):
        market.step()
    
    return {
        'prices': market.price_history,
        'fundamentals': market.fundamental_history,
        'volumes': market.volume_history,
        'crisis_start': normal_periods,
        'recovery_start': normal_periods + crisis_periods
    }

def plot_crisis_scenario(data):
    """
    Plot market behavior during crisis scenario
    """
    periods = range(len(data['prices']))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    ax1.plot(periods, data['prices'], 'b-', linewidth=2, label='Market Price')
    ax1.plot(periods, data['fundamentals'], 'g--', linewidth=2, label='Fundamental Value')
    ax1.axvline(data['crisis_start'], color='red', linestyle=':', alpha=0.7, label='Crisis Start')
    ax1.axvline(data['recovery_start'], color='orange', linestyle=':', alpha=0.7, label='Recovery Start')
    ax1.set_ylabel('Price')
    ax1.set_title('Market Crisis Simulation')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(periods, data['volumes'], 'purple', linewidth=2)
    ax2.axvline(data['crisis_start'], color='red', linestyle=':', alpha=0.7)
    ax2.axvline(data['recovery_start'], color='orange', linestyle=':', alpha=0.7)
    ax2.set_xlabel('Period')
    ax2.set_ylabel('Trading Volume')
    ax2.set_title('Trading Volume During Crisis')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig
