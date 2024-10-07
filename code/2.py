import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

initial_capital = 1_000_000
asset_names = ['SPY', 'GOVT', 'GSG']
weights = [1/3, 1/3, 1/3]

# read the data
file_path = 'data//stock_prices_p2.csv'
df = pd.read_csv(file_path, parse_dates=['date'])
df.set_index('date', inplace=True)

start_date_period1 = '2022-06-30'
end_date_period1 = '2023-06-30'
start_date_period2 = '2023-06-30'
end_date_period2 = '2024-06-30'

class Period:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    @property
    def df(self):
        return df.loc[self.start_date:self.end_date]

    @property
    def SPY(self):
        return self.df.loc[self.start_date:self.end_date, 'SPY']

    @property
    def GOVT(self):
        return self.df.loc[self.start_date:self.end_date, 'GOVT']

    @property
    def GSG(self):
        return self.df.loc[self.start_date:self.end_date, 'GSG']

    @property
    def SPY_GOVT_GSG(self):
        return self.df.loc[self.start_date:self.end_date, ['SPY', 'GOVT', 'GSG']]

class Asset:
    def __init__(self, name, period: Period, weight):
        self.name = name
        self.period = period
        self.weight = weight
        self.df_prices = period.df[self.name]
        self.initial_price = 1_000_000 * weight
        self.start_price = self.df_prices.loc[period.start_date]
        self.initial_shares = self.initial_price / self.start_price
        self.daily_returns = self.df_prices.pct_change().dropna()

class Portfolio:
    def __init__(self, assets):
        self.assets = assets

    @property
    def portfolio_value(self):
        portfolio_value = pd.Series(0, index=self.assets[0].df_prices.index)

        for asset in self.assets:
            asset_value = asset.df_prices * asset.initial_shares
            portfolio_value += asset_value

        return portfolio_value
    
    @property
    def daily_returns(self):
        return self.portfolio_value.pct_change().dropna()

    @property
    def annualized_return(self):
        total_return = (self.portfolio_value.iloc[-1] / self.portfolio_value.iloc[0]) - 1
        annualized_return = (1 + total_return) ** (252 / len(self.portfolio_value)) - 1
        return annualized_return

    @property
    def annualized_sd(self):
        return self.daily_returns.std() * np.sqrt(252)

    @property
    def return_risk_ratio(self):
        return self.annualized_return / self.annualized_sd

    @property
    def risk_contribution(self):
        risk_contribution = {}

        for asset in self.assets:
            asset_cov_with_portfolio = asset.daily_returns.cov(self.daily_returns)
            risk_contribution[asset.name] = (asset.weight * asset_cov_with_portfolio) / self.annualized_sd

        # Normalize the risk contribution
        total_risk_contribution = sum(risk_contribution.values())
        risk_contribution = {asset: rc / total_risk_contribution for asset, rc in risk_contribution.items()}

        return risk_contribution

period1 = Period(start_date_period1, end_date_period1)
period2 = Period(start_date_period2, end_date_period2)

assets_period1 = [Asset(name, period1, weight) for name, weight in zip(asset_names, weights)]
assets_period2 = [Asset(name, period2, weight) for name, weight in zip(asset_names, weights)]

portfolio_period1 = Portfolio(assets_period1)
portfolio_period2 = Portfolio(assets_period2)

def print_result_a(portfolio, assets, period_name, csv_filename):
    print(f'\n{period_name}')

    # Print the number of shares of each asset at the beginning of the period
    for asset in assets:
        print(f'Number of shares of {asset.name} at the beginning of the period: {asset.initial_shares}')

    # Save the portfolio value for each day to a CSV file
    portfolio.portfolio_value.to_csv(csv_filename)

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

# Period 1
print_result_a(portfolio_period1, assets_period1, 'Period 1', 'portfolio_value_period1.csv')

# Period 2
print_result_a(portfolio_period2, assets_period2, 'Period 2', 'portfolio_value_period2.csv')
