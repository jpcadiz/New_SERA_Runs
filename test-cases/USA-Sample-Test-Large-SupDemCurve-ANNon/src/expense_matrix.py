import pandas as pd
import numpy as np


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
    'LIFE': 'Lifetime'
}


def debug_cost_mtx_col(mtx: pd.DataFrame, year: int):
    """
    Prints a year column of a cost matrix for debugging purposes.

    Strips all 0 values and prints only filled values of the column
    """
    column = mtx.loc[(mtx[year] > 0), year]
    print(f"DEBUG: {mtx.name}[{year}] positive values:\n", column)
    print(f"Number of entries: {len(column)}")


def insert_index(df: pd.DataFrame) -> pd.Series:
    """
    Creates an Index column to the DataFrame.
    
    Index column makes building the expense matrix much easier and much more readable
    than trying to use the DataFrame's index values. 
    """
    return df.insert(0, 'Index', range(len(df)))


def prep_sums(df: pd.DataFrame) -> pd.Series:
    """
    Takes an expense matrix df, removes the 'Index' column, 
    and puts the sums of the remaining columns in a Series 
    """
    df2 = df.iloc[:, 1:]
    df2.fillna(0, inplace=True)
    sums = df2.apply(sum)
    sums = sums.reset_index(drop=True)
    return sums


class ExpenseMatrix():
    def __init__(self, cfbi_df: pd.DataFrame, expense: str, analysis_range: range) -> None:
        """
        ExpenseMatrix takes a CFBI DataFrame, an expense column and a range of years for analysis.
        """
        self.cfbi_df = cfbi_df
        self.matrix = pd.DataFrame(index=range(len(self.cfbi_df)),
                                       columns=analysis_range)
        self.expense = expense
            

    def insert_in_matrix(self, **kwargs):
        """
        Fills a DataFrame with given values according to year, index, and lifetime. 
        """
        index = kwargs.get('index')
        year = kwargs.get('year')
        lifetime = kwargs.get('lifetime')
        expense = kwargs.get('expense')
        mp = kwargs.get('mp')
        insert = 0

        for col in self.matrix.columns[1:]:
            if year <= col and year + lifetime > col:
                insert = expense * mp
                if insert == np.inf or insert == np.nan:
                    insert = 0 
                self.matrix.at[index, col] = insert


    def fill_matrix(self):
        """
        Inserts an index column in the matrix then uses apply() to fill the matrix with values
        from each row in the CFBI DataFrame. 
        """
        print(f'Building {self.expense} matrix...')
        insert_index(self.matrix)
        self.cfbi_df.apply(lambda row: self.insert_in_matrix(
                                                   index=row["Index"],
                                                   year=row['Year'],
                                                   lifetime=row[COL_HEADERS['LIFE']],
                                                   expense=row[self.expense],
                                                   mp=row['MP CapCost Estimate (2020$)']),
                            axis=1
                        )
        print(f'{self.expense} matrix complete')
        

    def get_matrix(self):
        return self.matrix
    

    def get_sums(self):
        sums = prep_sums(self.matrix)
        return sums
      

class PivotFlow():
    def __init__(self, flow_df: pd.DataFrame, value_name: str) -> None:
        self.flow_df = flow_df
        self.pivot_flow = pd.pivot_table
        self.value_name = value_name


    def _calculate_values(self) -> pd.Series:
        """
        Adds a column in flow_df to fill the pivot_table.

        Values are the sum of the Production and Flow columns.
        """
        self.flow_df[self.value_name] = self.flow_df[COL_HEADERS['PROD']].add(self.flow_df[COL_HEADERS['FLOW']]) 
        

    def _pivot(self) -> None:
        """
        Constructs a pivot table from the flow DataFrame.
        """
        return pd.pivot_table(
                                self.flow_df,
                                values=self.value_name,
                                index=COL_HEADERS['INF_ID'],
                                columns=COL_HEADERS['YEAR'],
                                fill_value=0
                            )
        

    def build_pivot_flow(self) -> None:
        """
        Calls calculate values and pivot to create the pivot_flow.
        """
        self._calculate_values()
        self.pivot_flow = self._pivot()
        
    
    def find_in_pivot_flow(self, inf_id, year):
        """
        Returns the value in the pivot_flow based on given inf_id (index) and year (col).

        For use in building VarOpExMatrix and FeedstockAndEnergyVarOpExMatrix
        """
        return self.pivot_flow.at[inf_id, year]
        

class VarOpExMatrix():
    def __init__(self, cfbi_df: pd.DataFrame, pivot_flow: PivotFlow, analysis_range: range) -> None:
        self.cfbi_df = cfbi_df
        self.pivot_flow = pivot_flow
        self.var_opex_mtx = pd.DataFrame(index=range(len(self.cfbi_df)),
                                columns=analysis_range)
    

    def insert_in_var_opex_mtx(self, **kwargs):
        """
        Finds a value in the Pivot Flow based on given year and inf_id and inserts it into the matrix.
        """
        index = kwargs.get('index')
        year = kwargs.get('year')
        inf_id = kwargs.get('inf_id')
        var_opex = kwargs.get('var_opex')
        insert = 0

        for col in self.var_opex_mtx.columns[1:]:
            if year <= col:
                insert = self.pivot_flow.find_in_pivot_flow(inf_id, col)
                self.var_opex_mtx.at[index, col] = insert * var_opex


    def build_var_opex_mtx(self):
        """
        Builds the Var OpEx Matrix
        """
        print('Building Var OpEx Matrix...')

        insert_index(self.var_opex_mtx)
        self.cfbi_df.apply(lambda row:
                           self.insert_in_var_opex_mtx(
                            index=row['Index'],
                            year=row[COL_HEADERS['YEAR']],
                            inf_id=row[COL_HEADERS['INF_ID']],
                            var_opex=row['VarOpEx $/kg']
                           ), axis=1)

        print('Var OpEx Matrix complete')


    def prep_sums(self, df: pd.DataFrame):
        """
        Takes an expense matrix df, removes the 'Index' column, 
        and puts the sums of the remaining columns in a Series 
        """
        df2 = df.iloc[:, 1:]
        df2.fillna(0, inplace=True)

        sums = df2.apply(sum)
        sums = sums.reset_index(drop=True)
        return sums
            

    def get_var_opex_sums(self):
        sums = self.prep_sums(self.var_opex_mtx)
        return sums


class FeedstockAndEnergyVarOpExMatrix():
    def __init__(self, pivot_flow: PivotFlow, cfbi_df: pd.DataFrame, feedstock_prices_df: pd.DataFrame, materials: list, analysis_range: range) -> None:
        self.pivot_flow = pivot_flow
        self.cfbi_df = cfbi_df
        self.feedstock_prices_mi = feedstock_prices_df.set_index(['Zone', 'Material', 'Year'])
        self.materials = materials
        self.feedstock_and_energy_mtx = pd.DataFrame(index=range(len(self.cfbi_df)),
                                        columns=analysis_range)
        self.input_sums_mtx = pd.DataFrame(index=range(len(self.cfbi_df)),
                                        columns=analysis_range,
                                        dtype=np.float64)
    

    def insert_in_base_mtx(self, **kwargs):
        """
        Finds a value in the pivot_flow based on given year and inf_id and inserts it into the matrix.

        Ensures that only positive values from the pivot_flow are added.
        """
        index = kwargs.get('index')
        year = kwargs.get('year')
        inf_id = kwargs.get('inf_id')
        insert = 0

        for col in self.feedstock_and_energy_mtx.columns[1:]:
            if year <= col:
                insert = self.pivot_flow.find_in_pivot_flow(inf_id, col)
                insert = insert if insert > 0 else 0
                self.feedstock_and_energy_mtx.at[index, col] = insert


    def prep_base_matrix(self):
        """
        Builds a base for the Feedstock and Energy Expense Matrix.

        Uses the positive pivot_flow values associated with Inf ID.
        """
        insert_index(self.feedstock_and_energy_mtx)
        self.cfbi_df.apply(lambda row:
                        self.insert_in_base_mtx(
                        index=row['Index'],
                        year=row[COL_HEADERS['YEAR']],
                        inf_id=row[COL_HEADERS['INF_ID']]
                    ), axis=1)


    def lookup_feedstock_price(self, zone, material, year) -> np.float64:
        """
        Searches a feestock MultiIndex and returns the Price based on given region, material, and year. 
        """
        try:
            return self.feedstock_prices_mi.loc[(zone, material, year), 'Price [$/unit]']
        except IndexError:
            return 0
        except KeyError:
            return 0
        

    def list_feestock_prices_by_material(self, region, year) -> list:
        """
        Creats a list of feedstock prices for each materail for a given year and region.
        """
        return [self.lookup_feedstock_price(region, material, year) for material in self.materials]
            

    def combine_feedstock_and_input_prices(self, input_prices: list, feedstock_prices: list) -> list:
        """
        Combines feestock price with input price by multiplication
        """
        return [np.round(input * feedstock, 18) for input, feedstock in zip(input_prices, feedstock_prices)]


    def sum_feedstock_prices(self, input_prices: list, region, year) -> np.float64:
        """
        Sums a list of feedstock prices.
        """
        combined_prices = self.combine_feedstock_and_input_prices(
            input_prices,
            self.list_feestock_prices_by_material(region, year)
        )
        return sum(combined_prices)


    def insert_in_matrix(self, **kwargs):
        """
        Inserts values into the input sums matrix.
        """
        index = kwargs.get('index')
        year = kwargs.get('year')
        input_prices = kwargs.get('input_prices')
        region = kwargs.get('region')

        for col in self.input_sums_mtx.columns[1:]:
            if year <= col:
                insert = self.sum_feedstock_prices(input_prices, region, col)
                self.input_sums_mtx.at[index, col] = insert


    def get_material_costs(self, index) -> pd.Series:
        """
        Locates the set of material costs of self.cfbi_df based on a given index.
        """
        row = self.cfbi_df.iloc[index]
        return row[self.materials]


    def material_costs_to_list(self, index) -> list:
        """
        Finds the material costs of self.cfbi_df at a given index and returns them as a list.
        """
        return self.get_material_costs(index).values.flatten().tolist()
    

    def fill_matrix(self):
        """
        Inserts an index column in the matrix then uses apply() to fill the matrix with values
        from each row in the CFBI DataFrame.
        """
        self.cfbi_df.apply(lambda row: self.insert_in_matrix(
            index=row["Index"],
            year=row['Year'], 
            input_prices=self.material_costs_to_list(row['Index']),
            region=row['Region'],
            ), axis=1)


    def build_matrix(self):
        """
        Builds the Feedstock and Energy Var OpEx Matrix
        """
        print("Building Feedstock and Energy VarOpEx Matrix...")
        self.prep_base_matrix()
        insert_index(self.input_sums_mtx)
        self.fill_matrix()
        self.feedstock_and_energy_mtx = self.feedstock_and_energy_mtx.mul(self.input_sums_mtx)
        print("Feedstock and Energy VarOpEx Matrix complete")


    def get_feedstock_and_energy_matrix(self):
        return self.feedstock_and_energy_mtx
    

    def get_feedstock_and_energy_sums(self):
        return prep_sums(self.feedstock_and_energy_mtx)

