"""
Module containing methods to build a Cash Flow By Item matrix.
"""
import pandas as pd
import numpy as np
from bisect import bisect_right

COL_HEADERS = {
    'YEAR': 'Year',
    'INF_ID': 'Infrastucture_ID',
    'NTWRK_ID': 'Network_ID',
    'TECH': 'Technology',
    'LEN': 'Length',
    'PROD': 'Production',
    'NPC': 'Nameplate_Capacity',
    'LIFE': 'Lifetime'
}


def combine_and_sort(df1: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame) -> pd.DataFrame:
    """
    Takes 3 dataframes, combines them, and sorts them by index.
    """
    frames = [df1, df2, df3]
    combined = pd.concat(frames)
    combined.sort_index(inplace=True)
    return combined

    
def split_on_production(df: pd.DataFrame):
    """
    Splits a DataFrame into three subsets based on production and existing infrastructure.
    Returns a tuple containing each subset.
    """
    deliv_df = df[(df[COL_HEADERS['PROD']] == 'No')]
    deliv_df.name = 'deliv_df'
    prod_df = df[(df[COL_HEADERS['PROD']] != 'No')]
    prod_df = prod_df[(prod_df[COL_HEADERS['LIFE']] != 1000)]
    prod_df.name = 'prod_df'
    existing_df = df[(df[COL_HEADERS['LIFE']] == 1000)]
    existing_df.name = 'existing_df'
    return (deliv_df, prod_df, existing_df)


class ClosestMatcher():
    """
    Class containing methods used for finding the closest match for a value in a DataFrame.
    """

    def get_closest(self, search_list, target):
        """
        Finds the closest value to a target in a given list-like object.

        search_list must already be sorted.
        """
        position = bisect_right(search_list, target)
        if position == 0:
            return search_list[position]
        else:
            return search_list[position-1]


    def get_closest_year(self, lookup_df: pd.DataFrame, technology, target_year: int):
        """
        Searches a lookup df for the closest year in a technology to the target without exceeding that target.
        """
        try:
            search_list = lookup_df.loc[(technology)].index.get_level_values(0)
            return self.get_closest(search_list, target_year)
        except KeyError:
            return 0


    def get_closest_nameplate(self, lookup_df: pd.DataFrame, technology, lookup_year, target_npc: int) -> int:
        """
        Searches the lookup DataFrame for the closest nameplate capacity in a year within a technology.

        Returns the closest nameplate capacity to the target without exceeding that target.
        """
        try:
            sorted_df = lookup_df.sort_index(level=0)
            search_list = sorted_df.loc[(technology, lookup_year)].index
            return self.get_closest(search_list, target_npc)
        except KeyError:
            return 0


class MultiIndexSearcher():
    """
    Class with methods for searching a MultiIndex object
    """
    def __init__(self) -> None:
        self.cm = ClosestMatcher()


    def get_year_from_mi(self, df: pd.DataFrame, mi: pd.MultiIndex):
        """
        Searches a MultiIndex object and looks for the closest year to the year entry for each row in a DataFrame
        """
        years = df.apply(lambda row: self.cm.get_closest_year(
            mi,
            row[COL_HEADERS['TECH']],
            row[COL_HEADERS['YEAR']]), axis=1)
        return years


    def get_npc_from_mi(self, df: pd.DataFrame, mi: pd.DataFrame, year_col: pd.Series) -> pd.Series:
        """
        Gets the Nameplate Capacity [kg/yr] for lookup of a DataFrame.
        """
        npcs = df.apply(lambda row: self.cm.get_closest_nameplate(
            mi, 
            row[COL_HEADERS['TECH']],
            row[year_col],
            row[COL_HEADERS['NPC']]), axis=1)
        return npcs.round()


class CensusDivSearcher():
    """
    Class to house the methods used for searching a census div
    """
    def find_region_in_census_div(self, census_div: pd.DataFrame, network_id: str):
        """
        Returns the value in 'Zone' of census_div for the row matching a given 'Network ID'
        """
        try:
            region =  census_div.iat[census_div.loc[census_div['Network ID'] == network_id].index[0], 1]
        except IndexError as e:
            print(f"Error: {network_id} not found in census_div. Please ensure the correct source file is being uploaded.")
            raise e

        return region

    def get_regions(self, df:pd.DataFrame, census_div: pd.DataFrame) -> pd.Series:
        """
        Iterates through each row of a Data Frame and builds a Series based on matching 'Network ID' fields.
        """
        regions = df.apply(lambda row: self.find_region_in_census_div(census_div, row[COL_HEADERS['NTWRK_ID']]), axis=1)
        return regions
    

class CostFileSearcher():
    """
    Class to house methods for seraching cost files and returning values.
    """
    def _find_value_in_cost_file(self, costfile_df: pd.DataFrame, target_col, **lookup_matchers):
        """
        Searches a DataFrame for a value in a column based on given lookup matchers.  
        """
        try:
            return costfile_df.loc[tuple(lookup_matchers.values()), target_col]
        except KeyError:
            return 0


    def find_in_cost_file(self, df: pd.DataFrame, costfile_df: pd.MultiIndex, target_col):
        """
        Takes a DataFrame and uses apply to get values to match on in a MultiIndex costfile.

        Searches the MultiIndex for a value in a specified column.  
        """
        values = df.apply(lambda row: self._find_value_in_cost_file(
            costfile_df,
            tech=row['Technology'],
            year=row['YearToLookup Costs'],
            npc=row['NameplateCapacityToLookUp for base capacity (kg/y)'],
            target_col=target_col), axis=1)
        return values
    

    def get_existings_costs(self, df: pd.DataFrame, costfile_df: pd.MultiIndex, target_col):
        """
        Builds a Series of costs from existings based on Network_ID and Year.
        """
        values = df.apply(lambda row: 
                          self._find_value_in_cost_file(
                                costfile_df,
                                target_col=target_col,
                                network_id=row[COL_HEADERS['NTWRK_ID']],
                                year=row[COL_HEADERS['YEAR']]
                            ),
                        axis=1
                    )
        return values


class CrfGetter():
    """
    Class to get crfs from a given DataFrame.
    """
    def __init__(self, crf_df: pd.DataFrame) -> None:
        self.crf_df = crf_df


    def convert_col_headers_to_int(self) -> None:
        """
        Converts column headers from str to int.

        The column headers in crf_df represent the system lifetime. 
        """
        self.crf_df.columns = self.crf_df.columns.map(int)


    def extract_crf_series(self) -> pd.Series:
        """
        Returns the CRF row as a Series.
        """
        return self.crf_df.loc['CRF']
    

    def get_crfs(self, df: pd.DataFrame) -> pd.Series:
        """
        Return the Capital Recover Factor for each item in a Data Frame according to its lifetime.
        """
        self.convert_col_headers_to_int()
        crf_series = self.extract_crf_series() 
        crfs = df.apply(lambda row: crf_series.get(row[COL_HEADERS['LIFE']]), axis=1)
        return crfs


class CashFlowByItemColBuilder():
    """
    The main class for calculating and building columns of the Cash Flow By Item object. 
    """
    def __init__(self, cfbi_df: pd.DataFrame, costfile_df: pd.DataFrame, census_div: pd.DataFrame, inputs_df: pd.DataFrame, **kwargs) -> None:
        self.df = cfbi_df
        self.costfile_df = costfile_df
        self.census_div = census_div
        self.inputs_df = inputs_df
        self.crf = CrfGetter(kwargs.get('crf_df'))
        self.ms = MultiIndexSearcher()
        self.cds = CensusDivSearcher()
        self.cfs = CostFileSearcher()
    

    def insert_at_end(self, col_name: str, col_values):
        self.df.insert(len(self.df.columns), col_name, col_values)

    
    def calculate_base_sys_capex(self):
        """
        Calculates and inserts the BaseSysCapEx

        Checks the name of the DataFrame and performs a different calculation accordingly.
        For production, the BaseSysCapEx is simply the Cap Cost.
        For delivery, the BaseSysCapEx is (CapCost + CapCost/km * Length)
        """
        cap_cost = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Capital Cost [$]')
        self.insert_at_end('Capital Cost [$]', cap_cost)

        if self.df.name == 'prod_df':
            base_sys_capex = cap_cost

        elif self.df.name == 'deliv_df':
            deliv_cap_cost_km = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Capital Cost [$/km]')
            self.insert_at_end('Capital Cost [$/km]', deliv_cap_cost_km)

            cap_cost_times_length = deliv_cap_cost_km.mul(self.df[COL_HEADERS['LEN']] * 1)
            base_sys_capex = cap_cost_times_length + cap_cost

        self.insert_at_end('BaseSysCapEx (before scaling factor) $2020', base_sys_capex)


    def calculate_fixed_opex_percent_of_capex(self):
        """
        Calculates and inserts the FixedOpEx % of CapEx

        Checks the name of the DataFrame and performs a different calculation accordingly.
        NOTE: There is a dependency for calculate_base_sys_capex to be called before this method!
        """
        capcost = self.df['Capital Cost [$]']
        fixed_opcost_dollar_year = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Fixed Operating Cost [$/yr]')
        fixed_opcost_fraction_capcost = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Fixed Operating Cost [fraction of CapCost/y]')

        if self.df.name == 'prod_df':
            self.insert_at_end('FixedOpEx % of CapEx', fixed_opcost_fraction_capcost)

        elif self.df.name == 'deliv_df':
                fixed_opcost_dollar_km_year = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Fixed Operating Cost [$/km/yr]')

                # NOTE: try/except is not the way to do this! 
                # It's only written this way to mimic the IFERROR from Excel until a better understanding of the calculation
                try:
                    fixed_opex = fixed_opcost_fraction_capcost.add(fixed_opcost_dollar_km_year.div(capcost).replace(np.inf, 0).replace(np.nan, 0), fill_value=0)

                except:
                    fixed_opex = fixed_opcost_dollar_year.mul(capcost)

                self.insert_at_end('FixedOpEx % of CapEx', fixed_opex)


    def calculate_var_opex(self):
        """
        Calculates and inserts VarOpEx $/kg

        Checks the name of the DataFrame and performs a different calculation accordingly.
        """
        if self.df.name == 'deliv_df':
            deliv_var_opex = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Variable Operating Cost [$/kg]')
            self.insert_at_end('Variable Operating Cost [$/kg]', deliv_var_opex)

            deliv_var_opex_km = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Variable Operating Cost [$/km/kg]')
            self.insert_at_end('Variable Operating Cost [$/km/kg]', deliv_var_opex_km)

            total_deliv_var_opex = self.df['Variable Operating Cost [$/kg]'].add(self.df['Variable Operating Cost [$/km/kg]'].mul(self.df[COL_HEADERS['LEN']]))
            self.insert_at_end('VarOpEx $/kg', total_deliv_var_opex)

        elif self.df.name == 'prod_df':
            prod_var_opex = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Variable Operating Cost [$/kg]')
            self.insert_at_end('VarOpEx $/kg', prod_var_opex)

        elif self.df.name == 'existing_df':
            self.costfile_df = self.costfile_df.set_index(['Network ID', 'Year'])
            existing_var_opex = self.cfs.get_existings_costs(self.df, self.costfile_df, 'Cost [$/kg]')
            self.insert_at_end('VarOpEx $/kg', existing_var_opex)


    def get_mp_capcost_estimate(self, df: pd.DataFrame) -> pd.Series:
        """
        Return the MP CapCost estimate of a Data Frame.

        Assumes the Data Frame already has the following columns:
            'Nameplate Capacity [kg/yr]'
            'NameplateCapacityToLookUp for base capacity (kg/d)'
            'Scaling Exponent'
            'BaseSysCapEx (before scaling factor) $2020'
        """
        npc_kg_dy = df[COL_HEADERS['NPC']].div(365)
        npc_kg_dy = npc_kg_dy.apply(np.float64)         # This cast avoids ZeroDivisionError
        npc_to_lookup_kg_dy = df['NameplateCapacityToLookUp for base capacity (kg/d)']
        scaling_exp = df['Scaling Exponent']
        base_sys_capex = df['BaseSysCapEx (before scaling factor) $2020']
        mp = base_sys_capex * (npc_kg_dy.div(npc_to_lookup_kg_dy))**scaling_exp
        return mp


    def reindex_df(self, df: pd.DataFrame) -> pd.MultiIndex:
        """
        Converts a given DataFrame to a MultiIndex with the index hierarchy of Tech, Year, NPC
        """
        return df.set_index(['Technology', 'Year', 'Nameplate Capacity [kg/yr]'])


    def round_npcs(self, df: pd.DataFrame) -> pd.Series:
        """
        Returns a Series object with the rounded values of the NPC of a given DataFrame
        """
        return df['Nameplate Capacity [kg/yr]'].round()


    def build_columns(self):
        """
        Builds and inserts a number of columns that are needed to build expense matrices.
        """
        print(f"Building {self.df.name} columns...")
        self.inputs_df['Nameplate Capacity [kg/yr]'] = self.round_npcs(self.inputs_df)
        self.inputs_df = self.reindex_df(self.inputs_df)
        if self.df.name != 'existing_df':
            self.costfile_df['Nameplate Capacity [kg/yr]'] = self.round_npcs(self.costfile_df)
            self.costfile_df = self.reindex_df(self.costfile_df)
            year_to_lookup_costs = self.ms.get_year_from_mi(self.df, self.costfile_df)
            self.insert_at_end('YearToLookup Costs', year_to_lookup_costs)
            npc_kgyr_base_capacity = self.ms.get_npc_from_mi(self.df, self.costfile_df, 'YearToLookup Costs')
            self.insert_at_end('NameplateCapacityToLookUp for base capacity (kg/y)', npc_kgyr_base_capacity)
            npc_kgdy_base_capacity = npc_kgyr_base_capacity.div(365)
            self.insert_at_end('NameplateCapacityToLookUp for base capacity (kg/d)', npc_kgdy_base_capacity)
            scaling_exponents = self.cfs.find_in_cost_file(self.df, self.costfile_df, 'Scaling Exponent')
            self.insert_at_end('Scaling Exponent', scaling_exponents)
            crfs = self.crf.get_crfs(self.df)
            self.insert_at_end('CRF', crfs)
            self.calculate_base_sys_capex()
            mp_capcost = self.get_mp_capcost_estimate(self.df)
            self.insert_at_end('MP CapCost Estimate (2020$)', mp_capcost)
            self.calculate_fixed_opex_percent_of_capex()
            year_to_lookup_inputs = self.ms.get_year_from_mi(self.df, self.inputs_df)
            self.insert_at_end('YearToLookUp Inputs', year_to_lookup_inputs)
            regions = self.cds.get_regions(self.df, self.census_div)
            self.insert_at_end('Region', regions)
            npc_kgyr_inputs = self.ms.get_npc_from_mi(self.df, self.inputs_df, 'YearToLookUp Inputs')
            self.insert_at_end('NameplateCapacityToLookUp for inputs (kg/y)', npc_kgyr_inputs)
        self.calculate_var_opex()
        print(f"{self.df.name} columns complete")


    def get_df(self):
        return self.df

