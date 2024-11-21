"""
A program to process SERA data using Python rather than Excel.
Started on 10/6/2022 by Seth Weiss
"""
import pandas as pd
from pathlib import Path

from file_loader import FileLoader
import cash_flow_by_item as cfbi
import input_consumption as ic
import expense_matrix as em
from cash_flow_aggregated import CashFlowAggregated

import timeit

start_time = timeit.default_timer()


###################### Define constants #####################
# Use the DECIMAL_PLACES constant to control the size of the values printed to the console.
DECIMAL_PLACES = 2

# Use YAML_PREPEND to tell the program where the yaml file for the SERA project is.
# If the src folder is inside the SERA project directory, use Path().absolute().parent.absolute() for the prepend
YAML_PREPEND = ".."      #Path().absolute().parent.absolute()  # Use this line if the src folder is in the SERA results directory

# Alternatively, if src is not within the SERA project directory, use the following line with the correct path to the directory.
# YAML_PREPEND = "C:/Users/SWEISS/Documents/SERA Post Processing/Test Cases for Seth/With Existings"

YAML_FILE = "/scenarioLCOH.yaml"

SERA_OUTPUT_COL_HEADERS = [
                            'Year',
                            'Infrastucture_ID',
                            'Network_ID',
                            'Technology',
                            'Length',
                            'Production',
                            'Nameplate_Capacity',
                            'Lifetime'
                        ]
COST_SUMS = {}


################### Console print settings #########################
pd.set_option("display.max_columns", None)
# pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option('display.precision', DECIMAL_PLACES)  # Used to control the number of decimals displayed for floating point values. 


############ Load files and build initial DataFrames ##############
loader = FileLoader(yaml=YAML_FILE, prepend=YAML_PREPEND)

ANALYSIS_RANGE = loader.get_analysis_range()

dfs = loader.get_frames()

construction_df = dfs['construction_df']
flow_df = dfs['flow_df']
prod_cost_df = dfs['prod_cost_df']
deliv_cost_df = dfs['deliv_cost_df']
prod_inputs_df = dfs['prod_inputs_df']
deliv_inputs_df = dfs['deliv_inputs_df']
demand_df = dfs['demand_df']
feedstock_prices_df = dfs['feedstock_prices_df']
census_div_df = dfs['census_div_df']
existings_df = dfs['existings_df']
crf_df = dfs['crf_df']


############## Calculate CashFlowByItem cols #####################
# start cfbi df from construction_df
cash_flow_by_item = pd.DataFrame(construction_df[SERA_OUTPUT_COL_HEADERS])

# split the cfbi df to make manipulation easier
(cfbi_deliv, cfbi_prod, cfbi_existing) = cfbi.split_on_production(cash_flow_by_item)

cfbi_deliv_builder = cfbi.CashFlowByItemColBuilder(
                        cfbi_df=cfbi_deliv,
                        costfile_df=deliv_cost_df,
                        census_div=census_div_df,
                        inputs_df=deliv_inputs_df,
                        crf_df=crf_df
                    )

cfbi_prod_builder = cfbi.CashFlowByItemColBuilder(
                        cfbi_df=cfbi_prod,
                        costfile_df=prod_cost_df,
                        census_div=census_div_df,
                        inputs_df=prod_inputs_df,
                        crf_df=crf_df
                    )

cfbi_existing_builder = cfbi.CashFlowByItemColBuilder(
                            cfbi_df=cfbi_existing,
                            costfile_df=existings_df,
                            census_div=census_div_df,
                            inputs_df=prod_inputs_df
                        )

cfbi_deliv_builder.build_columns()
cfbi_prod_builder.build_columns()
cfbi_existing_builder.build_columns()

cfbi_deliv = cfbi_deliv_builder.get_df()
cfbi_prod = cfbi_prod_builder.get_df()
cfbi_existing = cfbi_existing_builder.get_df()


################### Inputs by Type Matrix ###################
materials = ic.get_material_categories(prod_inputs_df['Material'], deliv_inputs_df['Material'])

deliv_input_matrix = ic.InputConsumptionMatrix(
                        input_df=deliv_inputs_df,
                        cfbi_df=cfbi_deliv,
                        materials=materials
                    )

prod_input_matrix = ic.InputConsumptionMatrix(
                        input_df=prod_inputs_df,
                        cfbi_df=cfbi_prod,
                        materials=materials
                    )

deliv_input_matrix.build_inputs_consumption_matrix()
prod_input_matrix.build_inputs_consumption_matrix()

cfbi_deliv = cfbi_deliv.join(deliv_input_matrix.get_matrix())
cfbi_prod = cfbi_prod.join(prod_input_matrix.get_matrix())


############### Combine CFBI DFs for Expence Matrices ###################
cfbi_combined = cfbi.combine_and_sort(cfbi_deliv, cfbi_prod, cfbi_existing)


################## CRF Expense Matrix #######################
em.insert_index(cfbi_combined)

crf_matrix = em.ExpenseMatrix(cfbi_combined, expense='CRF', analysis_range=ANALYSIS_RANGE)
crf_matrix.fill_matrix()

COST_SUMS['crf_costs_sums'] = crf_matrix.get_sums()


################## Fixed OpEx Expense Matrix ##################
fixed_opex_mtx = em.ExpenseMatrix(
                    cfbi_combined,
                    expense='FixedOpEx % of CapEx',
                    analysis_range=ANALYSIS_RANGE
                )

fixed_opex_mtx.fill_matrix()

COST_SUMS['fixed_opex_sums'] = fixed_opex_mtx.get_sums()


################### Pivot Flow ###################
pivot_flow = em.PivotFlow(flow_df=flow_df, value_name='Production+Flow [kg]')
pivot_flow.build_pivot_flow()


################### Var OpEx Expense Matrix ###################
var_opex_mtx = em.VarOpExMatrix(cfbi_df=cfbi_combined, pivot_flow=pivot_flow, analysis_range=ANALYSIS_RANGE)
var_opex_mtx.build_var_opex_mtx()

COST_SUMS['var_opex_sums'] = var_opex_mtx.get_var_opex_sums()


################# Feedstock&Energy var OpEx Matrix #####################
feedstock_and_energy_opex_mtx = em.FeedstockAndEnergyVarOpExMatrix(
                                        pivot_flow=pivot_flow,
                                        cfbi_df=cfbi_combined,
                                        feedstock_prices_df=feedstock_prices_df,
                                        materials=materials,
                                        analysis_range=ANALYSIS_RANGE
                                    )

feedstock_and_energy_opex_mtx.build_matrix()

COST_SUMS['feedstock_and_energy_opex_sums'] = feedstock_and_energy_opex_mtx.get_feedstock_and_energy_sums()


# ##################### Cash Flow Aggregated ####################
cash_flow_aggregated = CashFlowAggregated(
                            flow_df=flow_df,
                            demand_df=demand_df,
                            analysis_range=ANALYSIS_RANGE,
                            cost_sums=COST_SUMS
                        )

cash_flow_aggregated.build_cfa()

total_time = timeit.default_timer()
print("Total build time:", total_time - start_time)

cash_flow_aggregated.display_graph()

