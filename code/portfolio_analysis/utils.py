def print_result_a(portfolio, assets, period_name, file_path):
    print(f'\n{period_name}')
    
    # Print the number of shares of each asset at the beginning of the period
    for asset in assets:
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
    risk_contribution = portfolio.risk_contribution
    print('Risk contribution of each asset:')
    for asset, rc in risk_contribution.items():
        print(f'{asset}: {rc}')

def plot_portfolio_value(portfolio, period_name):
    portfolio.portfolio_value.plot(title=f'Portfolio Value Over Time - {period_name}', ylabel='Portfolio Value', xlabel='Date')
    
