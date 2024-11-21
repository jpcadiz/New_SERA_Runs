"""
Module condtaining methods to build an Input Consumption Matrix
"""
import pandas as pd


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
    'LEN': 'Length'
}


def get_material_categories(production: pd.Series, delivery: pd.Series) -> list:
    """
    Takes a Series for produciton and a Series for delivery and returns a list of materials.

    The Series objects should be the materials column of an Inputs DataFrame
    """
    prod_materials = production.drop_duplicates().tolist()
    deliv_materials = delivery.drop_duplicates().tolist()

    materials = prod_materials + deliv_materials
    materials = [*set(materials)]
    materials = sorted(materials)

    return materials



class InputConsumptionMatrix():
    def __init__(self, **kwargs) -> None:
        self.input_df = kwargs.get('input_df', None)
        self.cfbi_df = kwargs.get('cfbi_df', None)
        self.materials = kwargs.get('materials')
        self.inputs_matrix = pd.DataFrame()


    def reindex_inputs(self):
        """
        Re-index the inputs DataFrame into a MultiIndex object and sort the index. 
        """
        self.input_mi = self.input_df.set_index(['Material', 'Technology', 'Year', 'Nameplate Capacity [kg/yr]'])
        self.input_mi = self.input_mi.sort_index()


    def consumption_with_distance(self, consumption, len):
        """
        Multiplies the consumption value by the length for one-way trip. 
        """
        if consumption is not pd.Series:
            return consumption * (len * 1)
        else:
            return consumption.iloc[0] * (len * 1)


    def find_input_consumption_by_material(self, mat, tech, year, npc, len):
        """
        Takes a Data Frame of inputs by material and returns the consumption based on year, material, and technology.  
        """
        try:
            if mat == 'Diesel [gal]':
                consumptions = self.input_mi.loc[(mat, tech, year, npc), 'Consumption [unit/km/kg]']
                return self.consumption_with_distance(consumptions, len)
                
            else:
                consumptions = self.input_mi.loc[(mat, tech, year, npc), 'Consumption [unit/kg]']

                if type(consumptions) is not pd.Series:
                    return consumptions
                else:
                    return consumptions.iloc[0]

        except KeyError:
            return 0

    
    def build_inputs_consumption_matrix(self):
        """
        Builds a pd.Series object for each material and adds it to the input consumption matrix. 
        """
        print(f'Building inputs consumption matrix for {self.cfbi_df.name}...')
        self.reindex_inputs()
        for mat in self.materials:
            self.inputs_matrix[mat] = self.cfbi_df.apply(lambda row:
                                                         self.find_input_consumption_by_material(
                                                            mat,
                                                            row[COL_HEADERS['TECH']],
                                                            row['YearToLookUp Inputs'],
                                                            row['NameplateCapacityToLookUp for inputs (kg/y)'],
                                                            row[COL_HEADERS['LEN']]
                                                        ), axis=1
                                                    )
        print(f'Inputs consumption matrix for {self.cfbi_df.name} complete')

    
    def get_matrix(self):
        """
        Returns the inputs consumption matrix
        """
        return self.inputs_matrix

