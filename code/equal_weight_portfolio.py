import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# read the data
file_path = 'data//stock_prices_p2.csv'
df = pd.read_csv(file_path, parse_dates=['date'])

df.set_index('date', inplace=True)

df = df[['SPY', 'GOVT', 'GSG']]

print(df.head())

initial_capital = 1_000_000
equal_weight = 1 / 3

investment_per_asset = initial_capital * equal_weight

start_date_period1 = '2022-06-30'
end_date_period1 = '2023-06-30'

start_date_period2 = '2023-06-30'
end_date_period2 = '2024-06-30'

def calculate_portfolio_values(df, start_date, end_date):
    # Select data for the given time period
    df_period = df.loc[start_date:end_date]
    
    # Get the initial price of each asset at the start of the period
    spy_start_price = df_period.loc[start_date, 'SPY']
    govt_start_price = df_period.loc[start_date, 'GOVT']
    gsg_start_price = df_period.loc[start_date, 'GSG']
    
    # Print the initial prices for the given time period
    print(f"Initial Price ({start_date} to {end_date}):")
    print(f"SPY: {spy_start_price}")
    print(f"GOVT: {govt_start_price}")
    print(f"GSG: {gsg_start_price}")
    
    # Calculate the initial number of shares for each asset
    spy_shares = investment_per_asset / spy_start_price
    govt_shares = investment_per_asset / govt_start_price
    gsg_shares = investment_per_asset / gsg_start_price
    
    # Print the initial number of shares for each asset
    print(f"\nInitial Number of Shares ({start_date} to {end_date}):")
    print(f"SPY: {spy_shares}")
    print(f"GOVT: {govt_shares}")
    print(f"GSG: {gsg_shares}")
    
    # Calculate the portfolio value for each day in the given time period
    portfolio_value = (df_period['SPY'] * spy_shares) + \
                      (df_period['GOVT'] * govt_shares) + \
                      (df_period['GSG'] * gsg_shares)
    
    return df_period, portfolio_value

df_period1, portfolio_value_period1 = calculate_portfolio_values(df, start_date_period1, end_date_period1)
df_period2, portfolio_value_period2 = calculate_portfolio_values(df, start_date_period2, end_date_period2)

# Add the calculated portfolio values for both periods to the original DataFrame
df['Portfolio_Value_Period_1'] = portfolio_value_period1
df['Portfolio_Value_Period_2'] = portfolio_value_period2

# write the data into file
output_file_path = 'data//stock_prices_p2.csv'
df.to_csv(output_file_path)

# (ii) calculate the annualized return, volatility, and return/risk ratio
def calculate_annualized_metrics(portfolio_values):
    # calculate daily returns
    daily_returns = portfolio_values.pct_change().dropna()

    # calculate total return
    total_return = (portfolio_values.iloc[-1] / portfolio_values.iloc[0]) - 1
    annualized_return = (1 + total_return) ** (252 / len(portfolio_values)) - 1

    # calculate annualized volatility
    annualized_volatility = daily_returns.std() * np.sqrt(252)

    # calculate return/risk ratio
    return_risk_ratio = annualized_return / annualized_volatility

    return daily_returns, annualized_return, annualized_volatility, return_risk_ratio

daily_returns_p1, annualized_return_p1, annualized_volatility_p1, return_risk_ratio_p1 = calculate_annualized_metrics(portfolio_value_period1)
daily_returns_p2, annualized_return_p2, annualized_volatility_p2, return_risk_ratio_p2 = calculate_annualized_metrics(portfolio_value_period2)

print(f"Period 1 Annualized Return: {annualized_return_p1:.4f}")
print(f"Period 1 Annualized Volatility: {annualized_volatility_p1:.4f}")
print(f"Period 1 Return/Risk Ratio: {return_risk_ratio_p1:.4f}")

print(f"Period 2 Annualized Return: {annualized_return_p2:.4f}")
print(f"Period 2 Annualized Volatility: {annualized_volatility_p2:.4f}")
print(f"Period 2 Return/Risk Ratio: {return_risk_ratio_p2:.4f}")

# (iii) calculate the risk contribution of each asset
def calculate_risk_contribution(df_prices, portfolio_values):
    # calculate daily returns of each asset and the portfolio
    daily_returns = df_prices.pct_change().dropna()
    portfolio_daily_returns = portfolio_values.pct_change().dropna()

    # calculate portfolio volatility
    portfolio_volatility = portfolio_daily_returns.std() * np.sqrt(252)
    print(f"Portfolio Volatility: {portfolio_volatility}")

    risk_contribution = {}
    for asset in df_prices.columns:
        # calculate covariance of the asset with the portfolio
        asset_cov_with_portfolio = daily_returns[asset].cov(portfolio_daily_returns)

        # calculate risk contribution of the asset
        risk_contribution[asset] = (1 / 3 * asset_cov_with_portfolio) / portfolio_volatility

    # normalize the risk contributions
    total_risk_contribution = sum(risk_contribution.values())
    risk_contribution = {asset: rc / total_risk_contribution for asset, rc in risk_contribution.items()}

    return risk_contribution

risk_contribution_p1 = calculate_risk_contribution(df_period1, portfolio_value_period1)
risk_contribution_p2 = calculate_risk_contribution(df_period2, portfolio_value_period2)

print(f"Period 1 Risk Contribution: {risk_contribution_p1}")
print(f"Period 2 Risk Contribution: {risk_contribution_p2}")

# Calculate annualized standard deviation (volatility) for each asset
def calculate_annualized_std(df_period):
    # calculate daily returns
    daily_returns = df_period.pct_change().dropna()

    # calculate annualized std dev for each asset
    annualized_std = daily_returns.std() * np.sqrt(252)

    return annualized_std, daily_returns.corr()

# For Period 1
annualized_std_p1, correlation_matrix_p1 = calculate_annualized_std(df_period1)

print("Period 1 Annualized Standard Deviation (Volatility):")
print(annualized_std_p1)
print("\nPeriod 1 Correlation Matrix:")
print(correlation_matrix_p1)

def portfolio_volatility(weights, cov_matrix):
    # Portfolio volatility given asset weights and covariance matrix
    return np.sqrt(weights.T @ cov_matrix @ weights)

def risk_contribution_obj(weights, cov_matrix):
    # Objective to minimize: difference in risk contributions between assets
    portfolio_vol = portfolio_volatility(weights, cov_matrix)
    marginal_contributions = cov_matrix @ weights
    risk_contributions = weights * marginal_contributions / portfolio_vol
    return np.sum((risk_contributions - np.mean(risk_contributions)) ** 2)

def find_equal_risk_weights(daily_returns):
    # Calculate the covariance matrix of daily returns
    cov_matrix = daily_returns.cov() * 252  # Annualized covariance matrix

    # Initial guess for weights (equal weights)
    initial_weights = np.array([1/3, 1/3, 1/3])

    # Constraints: sum of weights must equal 1, and weights must be between 0 and 1
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = [(0, 1) for _ in range(3)]

    # Minimize the objective function to find equal-risk weights
    result = minimize(risk_contribution_obj, initial_weights, args=(cov_matrix,), 
                      method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x

# Get the optimal weights for Period 1
optimal_weights_p1 = find_equal_risk_weights(df_period1.pct_change().dropna())

print(f"Equal-Risk-Contribution Portfolio Weights (Period 1): {optimal_weights_p1}")

# Calculate the number of shares based on the optimal weights
spy_shares_erc = (optimal_weights_p1[0] * initial_capital) / df_period1.iloc[0]['SPY']
govt_shares_erc = (optimal_weights_p1[1] * initial_capital) / df_period1.iloc[0]['GOVT']
gsg_shares_erc = (optimal_weights_p1[2] * initial_capital) / df_period1.iloc[0]['GSG']

print(f"\nEqual-Risk-Contribution Portfolio Shares (Period 1):")
print(f"SPY: {spy_shares_erc}")
print(f"GOVT: {govt_shares_erc}")
print(f"GSG: {gsg_shares_erc}")

# Calculate the portfolio's annualized standard deviation with the equal-risk weights
def calculate_portfolio_std(weights, cov_matrix):
    return np.sqrt(weights.T @ cov_matrix @ weights)

# Calculate the covariance matrix for Period 1
cov_matrix_p1 = df_period1.pct_change().dropna().cov() * 252

# Calculate the portfolio standard deviation using the optimal weights
portfolio_std_erc_p1 = calculate_portfolio_std(optimal_weights_p1, cov_matrix_p1)

print(f"\nEqual-Risk-Contribution Portfolio Annualized Standard Deviation (Period 1): {portfolio_std_erc_p1:.4f}")

def calculate_portfolio_values_with_weights(df, weights, start_date, end_date):
    # Select data for the given time period
    df_period = df.loc[start_date:end_date]
    
    # Get the initial price of each asset at the start of the period
    spy_start_price = df_period.loc[start_date, 'SPY']
    govt_start_price = df_period.loc[start_date, 'GOVT']
    gsg_start_price = df_period.loc[start_date, 'GSG']
    
    # Calculate the initial number of shares for each asset based on the weights
    spy_shares = (weights[0] * initial_capital) / spy_start_price
    govt_shares = (weights[1] * initial_capital) / govt_start_price
    gsg_shares = (weights[2] * initial_capital) / gsg_start_price
    
    # Calculate the portfolio value for each day in the given time period
    portfolio_value = (df_period['SPY'] * spy_shares) + \
                      (df_period['GOVT'] * govt_shares) + \
                      (df_period['GSG'] * gsg_shares)
    
    return portfolio_value

# Calculate portfolio values for Period 2 using the equal-risk weights
portfolio_value_erc_p2 = calculate_portfolio_values_with_weights(df, optimal_weights_p1, start_date_period2, end_date_period2)

# Calculate the annualized return, volatility, and return/risk ratio for Period 2
daily_returns_erc_p2, annualized_return_erc_p2, annualized_volatility_erc_p2, return_risk_ratio_erc_p2 = calculate_annualized_metrics(portfolio_value_erc_p2)

print(f"\nEqual-Risk-Contribution Portfolio (Period 2):")
print(f"Annualized Return: {annualized_return_erc_p2:.4f}")
print(f"Annualized Volatility: {annualized_volatility_erc_p2:.4f}")
print(f"Return/Risk Ratio: {return_risk_ratio_erc_p2:.4f}")
