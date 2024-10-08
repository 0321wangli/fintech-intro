from portfolio_analysis.asset import Asset
import pandas as pd
import numpy as np

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
    def sd(self):
        return self.daily_returns.std()

    @property
    def annualized_sd(self):
        return self.daily_returns.std() * np.sqrt(252)

    @property
    def return_risk_ratio(self):
        return self.annualized_return / self.annualized_sd

    @property
    def risk_contribution_equal_weight(self):
        risk_contribution = {}
        for asset in self.assets:
            asset_cov_with_portfolio = asset.daily_returns.cov(self.daily_returns)
            risk_contribution[asset.name] = (asset.weight * asset_cov_with_portfolio) / self.sd
        total_risk_contribution = sum(risk_contribution.values())
        return {asset: rc / total_risk_contribution for asset, rc in risk_contribution.items()}
    
    @property
    def covariance_matrix(self): # not related to weights
        return pd.concat([asset.daily_returns for asset in self.assets], axis=1).cov()

    @property
    def correlation_matrix(self): # not related to weights
        return pd.concat([asset.daily_returns for asset in self.assets], axis=1).corr()

    def test(self):
        print(self.annualized_sd ** 2)
        # wT * cov_matrix * w
        print(252 * np.dot(np.dot([asset.weight for asset in self.assets], self.covariance_matrix.values), [asset.weight for asset in self.assets]))

    def test2(self):
        print(self.covariance_matrix)
        print(self.assets[0].sd ** 2)
        print(self.assets[1].sd ** 2)
        print(self.assets[2].sd ** 2)


