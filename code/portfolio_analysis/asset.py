from portfolio_analysis.period import Period
import numpy as np

class Asset:
    def __init__(self, name, period, weight, initial_capital=1_000_000):
        self.name = name
        self.period = period
        self.weight = weight
        self.df_prices = period.get_asset_data(self.name)
        self.initial_price = initial_capital * weight
        self.start_price = self.df_prices.iloc[0]
        self.initial_shares = self.initial_price / self.start_price
        self.daily_returns = self.df_prices.pct_change().dropna()
        self.sd = self.daily_returns.std()
        self.annualized_sd = self.sd * np.sqrt(252)
