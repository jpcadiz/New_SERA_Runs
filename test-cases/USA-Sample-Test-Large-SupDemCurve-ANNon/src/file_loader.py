"""
A class to handle the loading of dataframes from the files found in a YAML file
"""

import pandas as pd
import yaml


class FileLoader:
    def __init__(self, yaml, prepend=""):
        """
        Takes a yaml file as an argument with an optional prepend string for the filepath.
        """
        self.prepend = prepend
        self.yaml = yaml
        self.frames = {}
        self.analysis_range = []
        self.load()


    def load(self):
        """
        Opens the YAML file and extracts filepaths to create DataFrame objects. 
        Packages each DataFrame in a dictionary
        """
        with open(f"{self.prepend}{self.yaml}", "r") as stream:
            try:
                print("Loading YAML file...")
                yam = yaml.safe_load(stream)
                self.frames['construction_df'] = pd.read_csv(f"{self.prepend}/{yam['infrastructureFiles']['constructionFile']}", sep='\t')
                self.frames['flow_df'] = pd.read_csv(f"{self.prepend}/{yam['infrastructureFiles']['flowFile']}", sep='\t')
                self.frames['prod_cost_df'] = pd.read_csv(f"{self.prepend}/{yam['processLibraryFiles'][0]['costsFile']}", sep='\t')
                self.frames['deliv_cost_df'] = pd.read_csv(f"{self.prepend}/{yam['processLibraryFiles'][1]['costsFile']}", sep='\t')
                self.frames['prod_inputs_df'] = pd.read_csv(f"{self.prepend}/{yam['processLibraryFiles'][0]['inputsFile']}", sep='\t')
                self.frames['deliv_inputs_df'] = pd.read_csv(f"{self.prepend}/{yam['processLibraryFiles'][1]['inputsFile']}", sep='\t')
                self.frames['demand_df'] = pd.read_csv(f"{self.prepend}/{yam['demandFiles'][0]}", sep='\t')
                self.frames['feedstock_prices_df'] = pd.read_csv(f"{self.prepend}/{yam['priceFiles'][0]}", sep='\t')
                self.frames['census_div_df'] = pd.read_csv(f"{self.prepend}/{yam['networkFiles']['zoneFiles'][0]}", sep='\t')
                self.frames['existings_df'] = pd.read_csv(f"{self.prepend}/{yam['networkFiles']['existingFiles'][0]}", sep='\t')
                self.frames['crf_df'] = pd.read_csv(f"{self.prepend}/{yam['crfFiles'][0]}", index_col=0,)
                self.analysis_range.append(yam['firstYear'])
                self.analysis_range.append(yam['lastYear'] + 1)
                print("YAML file load complete")
            except yaml.YAMLError as exc:
                print("Error loading YAML file", exc)


    def get_frames(self):
        """
        Return the dictionary of DataFrame objects. 
        """
        return self.frames
    

    def get_analysis_range(self):
        """
        Return the analysis range in the form of a range object.
        """
        print(f'Analysis range: {self.analysis_range[0]}-{self.analysis_range[1] - 1}')
        return range(self.analysis_range[0], self.analysis_range[1])


