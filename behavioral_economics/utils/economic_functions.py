import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def prospect_value_function(x, alpha=0.88, beta=0.88, lambda_param=2.25):
    """
    Prospect theory value function
    
    Parameters:
    x: outcome relative to reference point
    alpha: curvature parameter for gains (0 < alpha < 1)
    beta: curvature parameter for losses (0 < beta < 1)  
    lambda_param: loss aversion parameter (lambda > 1)
    
    Returns:
    Subjective value according to prospect theory
    """
    if isinstance(x, (list, np.ndarray)):
        return np.array([prospect_value_function(xi, alpha, beta, lambda_param) for xi in x])
    
    if x >= 0:
        return x ** alpha
    else:
        return -lambda_param * ((-x) ** beta)

def probability_weighting_function(p, gamma=0.61):
    """
    Probability weighting function from prospect theory
    
    Parameters:
    p: objective probability
    gamma: weighting parameter (gamma < 1 typically)
    
    Returns:
    Decision weight
    """
    if isinstance(p, (list, np.ndarray)):
        return np.array([probability_weighting_function(pi, gamma) for pi in p])
    
    if p <= 0:
        return 0
    if p >= 1:
        return 1
    
    return (p ** gamma) / ((p ** gamma + (1 - p) ** gamma) ** (1 / gamma))

def calculate_prospect_value(outcomes, probabilities, alpha=0.88, beta=0.88, lambda_param=2.25, gamma=0.61):
    """
    Calculate overall prospect value for a gamble
    
    Parameters:
    outcomes: list of outcomes relative to reference point
    probabilities: list of probabilities (must sum to 1)
    alpha, beta, lambda_param, gamma: prospect theory parameters
    
    Returns:
    Overall prospect value
    """
    if len(outcomes) != len(probabilities):
        raise ValueError("Outcomes and probabilities must have same length")
    
    if not np.isclose(sum(probabilities), 1.0):
        raise ValueError("Probabilities must sum to 1")
    
    total_value = 0
    for outcome, prob in zip(outcomes, probabilities):
        value = prospect_value_function(outcome, alpha, beta, lambda_param)
        weight = probability_weighting_function(prob, gamma)
        total_value += weight * value
    
    return total_value

def endowment_effect_ratio(lambda_param=2.25):
    """
    Calculate the predicted WTA/WTP ratio from loss aversion
    
    Parameters:
    lambda_param: loss aversion parameter
    
    Returns:
    Predicted ratio of willingness to accept to willingness to pay
    """
    return 1 + (1 / lambda_param)

def anchoring_adjustment(anchor, true_value, alpha=0.5):
    """
    Model anchoring and adjustment process
    
    Parameters:
    anchor: initial anchor value
    true_value: true/target value
    alpha: adjustment parameter (0 = no adjustment, 1 = complete adjustment)
    
    Returns:
    Final estimate after anchoring and adjustment
    """
    return anchor + alpha * (true_value - anchor)

def mental_accounting_utility(consumption_vector, weights, utility_functions):
    """
    Calculate utility under mental accounting
    
    Parameters:
    consumption_vector: consumption in each mental account
    weights: importance weights for each account
    utility_functions: list of utility functions for each account
    
    Returns:
    Total utility under mental accounting
    """
    if len(consumption_vector) != len(weights) or len(weights) != len(utility_functions):
        raise ValueError("All inputs must have same length")
    
    total_utility = 0
    for consumption, weight, utility_func in zip(consumption_vector, weights, utility_functions):
        total_utility += weight * utility_func(consumption)
    
    return total_utility

def plot_prospect_theory_functions(alpha=0.88, beta=0.88, lambda_param=2.25, gamma=0.61):
    """
    Plot the key functions from prospect theory
    
    Parameters:
    alpha, beta, lambda_param, gamma: prospect theory parameters
    
    Returns:
    matplotlib figure with subplots
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    x = np.linspace(-100, 100, 1000)
    v = prospect_value_function(x, alpha, beta, lambda_param)
    
    ax1.plot(x, v, 'b-', linewidth=2)
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Outcome (relative to reference point)')
    ax1.set_ylabel('Subjective Value')
    ax1.set_title('Prospect Theory Value Function')
    ax1.grid(True, alpha=0.3)
    
    p = np.linspace(0.01, 0.99, 100)
    w = probability_weighting_function(p, gamma)
    
    ax2.plot(p, w, 'r-', linewidth=2, label='Probability Weighting')
    ax2.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Linear (Rational)')
    ax2.set_xlabel('Objective Probability')
    ax2.set_ylabel('Decision Weight')
    ax2.set_title('Probability Weighting Function')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def simulate_disposition_effect(n_stocks=1000, purchase_price=100, lambda_param=2.25, alpha=0.88, beta=0.88):
    """
    Simulate the disposition effect in stock trading
    
    Parameters:
    n_stocks: number of stocks to simulate
    purchase_price: original purchase price
    lambda_param, alpha, beta: prospect theory parameters
    
    Returns:
    Dictionary with simulation results
    """
    np.random.seed(42)
    
    current_prices = np.random.normal(purchase_price, 20, n_stocks)
    gains_losses = current_prices - purchase_price
    
    sell_probabilities = []
    for gl in gains_losses:
        utility_sell = prospect_value_function(gl, alpha, beta, lambda_param)
        
        if gl > 0:
            prob_sell = 1 / (1 + np.exp(-utility_sell)) * 1.5
        else:
            prob_sell = 1 / (1 + np.exp(-utility_sell)) * 0.3
        
        sell_probabilities.append(min(prob_sell, 1.0))
    
    sell_probabilities = np.array(sell_probabilities)
    
    winning_stocks = gains_losses > 0
    losing_stocks = gains_losses < 0
    
    return {
        'gains_losses': gains_losses,
        'sell_probabilities': sell_probabilities,
        'winning_stocks': winning_stocks,
        'losing_stocks': losing_stocks,
        'avg_win_sell_prob': np.mean(sell_probabilities[winning_stocks]),
        'avg_loss_sell_prob': np.mean(sell_probabilities[losing_stocks])
    }
