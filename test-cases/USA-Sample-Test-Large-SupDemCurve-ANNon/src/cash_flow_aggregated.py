"""
Module containing methods to build a Cash Flow Aggregated object.
"""
import pandas as pd
import matplotlib.pyplot as plt


COLS_TO_PRINT = [
    'Year',
    'Capital',
    'FixOpEx',
    'VarOpEx',
    'Energy & feedstock',
    'US Average'
]


GRAPH_DATA_COLS = [
    'Year',
    'Capital',
    'FixOpEx',
    'VarOpEx',
    'Energy & feedstock'
]


GRAPH_US_AVG = [
    'Year',
    'US Average'
]


COL_HEADERS = {
    'VAR': 'Variable',
    'INF_ID': 'Infrastucture_ID',
    'YEAR': 'Year',
    'PERIOD': 'Period',
    'TECH': 'Technology',
    'PROD': 'Production_kg',
    'FLOW': 'Flow_kg',
    'LOSS': 'Loss_kg',
    'COST': 'Cost',
    'SALVAGE': 'Salvage_Value',
    'LIFE': 'Lifetime',
    'NON-FUEL_STN_DMND': 'Biofuels'
}


class CashFlowAggregated():
    def __init__(self, **kwargs) -> None:
        self.df = pd.DataFrame()
        self.flow_df = kwargs.get('flow_df', None)
        self.demand_df = kwargs.get('demand_df', None)
        self.analysis_range = kwargs.get('analysis_range', None)
        self.cost_sums = kwargs.get('cost_sums', None)
        self.h2_prod_list = []
        self.fuel_station_demand_list = []
        self.non_fuel_station_deman_list = []


    def sum_by_year(self, df: pd.DataFrame, year, return_col):
        return df.loc[df['Year'] == year][return_col].sum()


    def build_demand_cols(self):
        for year in self.analysis_range:
            self.h2_prod_list.append(self.sum_by_year(self.flow_df, year, COL_HEADERS['PROD']))
            self.fuel_station_demand_list.append(self.sum_by_year(self.demand_df, year, 'Fueling-Station'))
            self.non_fuel_station_deman_list.append(self.sum_by_year(self.demand_df, year, COL_HEADERS['NON-FUEL_STN_DMND']))

    
    def add_starter_cols(self):
        self.df = pd.DataFrame({'Year': [year for year in self.analysis_range],
                                    'Hydrogen production (kg/y)': self.h2_prod_list,
                                    'Fueling-Station Demand (kg/y)': self.fuel_station_demand_list,
                                    'Non-Fueling-Station Demand (kg/y)': self.non_fuel_station_deman_list})
        

    def add_total_demand(self):
        self.df['Total hydrogen demand (kg/y)'] = self.df['Fueling-Station Demand (kg/y)'] + self.df['Non-Fueling-Station Demand (kg/y)']


    def add_production_over_demand(self):
        self.df['Production/demand'] = self.df['Hydrogen production (kg/y)'].divide(self.df['Total hydrogen demand (kg/y)'])


    def add_cost_cols(self):
        self.df['CRF costs ($/y)'] = self.cost_sums['crf_costs_sums']
        self.df['FixedOpEx costs ($/y)'] = self.cost_sums['fixed_opex_sums']
        self.df['VarOpEx ($/y)'] = self.cost_sums['var_opex_sums']
        self.df['Feedstock costs ($/y)'] = self.cost_sums['feedstock_and_energy_opex_sums']


    def add_dollars_per_units_produced(self):
        self.df['Capital'] = self.df['CRF costs ($/y)'].div(self.df['Hydrogen production (kg/y)'])
        self.df['FixOpEx'] = self.df['FixedOpEx costs ($/y)'].div(self.df['Hydrogen production (kg/y)'])
        self.df['VarOpEx'] = self.df['VarOpEx ($/y)'].div(self.df['Hydrogen production (kg/y)'])
        self.df['Energy & feedstock'] = self.df['Feedstock costs ($/y)'].div(self.df['Hydrogen production (kg/y)'])
        self.df['US Average'] = self.df.loc[:, 'Capital':'Energy & feedstock'].sum(axis=1)
    

    def build_cfa(self):
        print("Building Cash Flow Aggregated...")
        self.build_demand_cols()
        self.add_starter_cols()
        self.add_total_demand()
        self.add_production_over_demand()
        self.add_cost_cols()
        self.add_dollars_per_units_produced()
        print("Cash Flow Aggregated complete")
        self.print_columns()


    def print_columns(self):
        """
        Prints selected columns to the console
        """
        cols_to_print = self.df[COLS_TO_PRINT]
        print(cols_to_print)


    def display_graph(self):
        plt.close("all")
        graph_data = self.df[GRAPH_DATA_COLS]
        us_avg = self.df[GRAPH_US_AVG]
        ax = graph_data.plot.area(x='Year')
        us_avg.plot(ax=ax, x='Year')
        plt.show()
        
    

    



