import pandas as pd
from portfolio_analysis.period import Period
from portfolio_analysis.asset import Asset
from portfolio_analysis.portfolio import Portfolio
from portfolio_analysis.utils import print_result_a

# Setup
initial_capital = 1_000_000
asset_names = ['SPY', 'GOVT', 'GSG']
weights = [1/3, 1/3, 1/3]

# Load data
file_path = 'data/stock_prices_p2.csv'
df = pd.read_csv(file_path, parse_dates=['date'])
df.set_index('date', inplace=True)

# Define periods
start_date_period1 = '2022-06-30'
end_date_period1 = '2023-06-30'
start_date_period2 = '2023-06-30'
end_date_period2 = '2024-06-30'

# Create Period objects
period1 = Period(start_date_period1, end_date_period1, df)
period2 = Period(start_date_period2, end_date_period2, df)

# Create Asset objects for each period
assets_period1 = [Asset(name, period1, weight) for name, weight in zip(asset_names, weights)]
assets_period2 = [Asset(name, period2, weight) for name, weight in zip(asset_names, weights)]

# Create Portfolio objects
portfolio_period1 = Portfolio(assets_period1)
portfolio_period2 = Portfolio(assets_period2)

# Process and print results
print_result_a(portfolio_period1, assets_period1, 'Period 1', 'data/portfolio_value_period1.csv')
print_result_a(portfolio_period2, assets_period2, 'Period 2', 'data/portfolio_value_period2.csv')
