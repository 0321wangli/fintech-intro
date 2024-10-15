import pandas as pd

class Period:
    def __init__(self, start_date, end_date, df):
        self.start_date = start_date
        self.end_date = end_date
        self.df = df.loc[self.start_date:self.end_date]

    def get_asset_data(self, asset_name):
        return self.df[asset_name]

    def get_assets_data(self, asset_names):
        return self.df[asset_names]
