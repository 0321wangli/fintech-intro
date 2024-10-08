import numpy as np
from scipy.optimize import minimize

def risk_contributions(weights, cov_matrix):
    """
    Calculate the risk contributions of each asset given the portfolio weights.
    """
    portfolio_volatility = np.sqrt(np.dot(np.dot(weights, cov_matrix), weights))
    marginal_risk_contributions = np.dot(cov_matrix, weights) / portfolio_volatility

    risk_contributions = weights * marginal_risk_contributions

    return risk_contributions

def erc_objective(weights, cov_matrix):
    """
    Objective function to minimize for Equal Risk Contribution (ERC).
    Minimize the squared differences between each pair of assets' risk contributions.
    """
    adjusted_risk_contributions = risk_contributions(weights, cov_matrix) * 3000 # Adjusted for numerical stability

    # Pairwise squared differences between risk contributions
    pairwise_diff = 0
    for i in range(len(weights)):
        for j in range(i + 1, len(weights)):
            pairwise_diff += (adjusted_risk_contributions[i] - adjusted_risk_contributions[j]) ** 2
    
    return pairwise_diff

def optimize_erc(cov_matrix, assets):
    """
    Optimize the portfolio weights for Equal Risk Contribution (ERC).
    """
    initial_weights = np.ones(assets) / assets  # Start with equal weights

    # Constraints: weights must sum to 1 and be non-negative
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = [(0, 1) for _ in range(assets)]  # Long-only, weights between 0 and 1

    # Minimize the ERC objective function
    result = minimize(erc_objective, initial_weights, args=(cov_matrix,), bounds=bounds, constraints=constraints)

    if result.success:

        adjusted_risk_contributions = risk_contributions(result.x, cov_matrix) * 3000
        # Print the adjusted risk contributions
        print("Adjusted risk contributions:", adjusted_risk_contributions)

        return result.x  # Optimized weights
    else:
        raise ValueError("Optimization failed")
