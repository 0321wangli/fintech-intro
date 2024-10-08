import matplotlib.pyplot as plt
import numpy as np
from optimize.erc import optimize_erc
from portfolio_analysis.asset import Asset
from portfolio_analysis.portfolio import Portfolio

def print_result(portfolio, period_name, file_path):
    """
    Print the answer of Part2-a.
    """

    print(f'\n{period_name}')
    
    # Print the number of shares of each asset at the beginning of the period
    for asset in portfolio.assets:
        print(f'Number of shares of {asset.name} at the beginning of the period: {asset.initial_shares}')

    # Save the portfolio value for each day to a CSV file
    portfolio.portfolio_value.to_csv(file_path)

    # Print the annualized return of the portfolio
    print(f'Annualized return of the portfolio: {portfolio.annualized_return}')

    # Print the annualized standard deviation of the portfolio
    print(f'Annualized standard deviation of the portfolio: {portfolio.annualized_sd}')

    # Print the return-risk ratio of the portfolio
    print(f'Return-risk ratio of the portfolio: {portfolio.return_risk_ratio}')

    # Calculate and print the risk contribution of each asset
    risk_contributions = portfolio.risk_contribution_equal_weight
    print('Risk contribution of each asset:')
    for asset, rc in risk_contributions.items():
        print(f'{asset}: {rc}')

def print_result_optimized(portfolio, period_name):
    """
    Print the answer of Part2-b.
    """

    print(f'\n{period_name}')

    # Print the standard deviation and annualized standard deviation for each asset in period 1
    for asset in portfolio.assets:
        print(f'{asset.name} standard deviation: {asset.sd}')
        print(f'{asset.name} annualized standard deviation: {asset.annualized_sd}')

    # Print the correlation matrix
    print(f"Correlation matrix for {period_name}:")
    print(portfolio.correlation_matrix)

    # Optimize Equal Risk Contribution (ERC) portfolio
    optimal_weights = optimize_erc(portfolio.covariance_matrix, len(portfolio.assets)) # wait
    print(f'Optimal weights: {optimal_weights}')

    # Construct a new portfolio using the optimized weights
    assets_optimal = [Asset(asset.name, asset.period, weight) for asset, weight in zip(portfolio.assets, optimal_weights)]
    portfolio_optimal = Portfolio(assets_optimal)

    # Print the number of shares of each asset in the optimized portfolio
    for asset in assets_optimal:
        print(f'Number of shares of {asset.name} in the optimal portfolio: {asset.initial_shares}')

    # Print the annualized standard deviation of the optimized portfolio
    print(f'Annualized standard deviation of the optimal portfolio: {portfolio_optimal.annualized_sd}')

    # Print the annualized return of the optimized portfolio
    print(f'Annualized return of the optimal portfolio: {portfolio_optimal.annualized_return}')

    # Print the return-risk ratio of the optimized portfolio
    print(f'Return-risk ratio of the optimal portfolio: {portfolio_optimal.return_risk_ratio}')

    # Return the optimized portfolio
    return portfolio_optimal



def plot_portfolio_value(portfolio, period_name):
    portfolio.portfolio_value.plot(title=f'Portfolio Value Over Time - {period_name}', ylabel='Portfolio Value', xlabel='Date')
    plt.show()

def plot_portfolio_risk_contribution(portfolios):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = [f'Portfolio {i+1}' for i in range(len(portfolios))]
    asset_names = list(portfolios[0].risk_contribution_equal_weight.keys())
    
    risk_contributions = {asset: [] for asset in asset_names}
    for portfolio in portfolios:
        for asset, contribution in portfolio.risk_contribution_equal_weight.items():
            risk_contributions[asset].append(contribution * 100)
    
    bottom = np.zeros(len(portfolios))
    for asset in asset_names:
        ax.bar(labels, risk_contributions[asset], width=0.3, bottom=bottom, label=asset)
        bottom += risk_contributions[asset]
    
    ax.set_title('Equal-Weight Portfolio Risk Decomposition', fontsize=16, fontweight='bold')
    ax.set_xlabel('Portfolio', fontsize=12)
    ax.set_ylabel('Risk Contribution (%)', fontsize=12)
    
    ax.set_ylim(0, 110)
    ax.set_yticks(range(0, 101, 10))
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=len(asset_names), fontsize=10)
    
    for i in range(len(labels)):
        total = sum(risk_contributions[asset][i] for asset in asset_names)
        ax.text(i, 105, f'{total:.0f}%', ha='center', va='bottom', fontsize=9)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
