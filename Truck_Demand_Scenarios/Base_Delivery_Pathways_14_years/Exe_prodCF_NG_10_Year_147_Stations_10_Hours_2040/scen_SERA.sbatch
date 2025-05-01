#!/bin/bash

#SBATCH --job-name=Exe_prodCF_NG_10_Year_147_Stations_10_Hours_2040
#SBATCH --time 10:00:00
#SBATCH --account=sera
#SBATCH --chdir=/home/jpcadiz/New_SERA_Runs/Truck_Demand_Scenarios/Base_Delivery_Pathways_14_years/Exe_prodCF_NG_10_Year_147_Stations_10_Hours_2040
#SBATCH -o SERA.log
#SBATCH --mail-user=jpcadiz@ucdavis.edu
#SBATCH --mail-type=ALL

module purge
module load xpressmp
module load gurobi

export PATH=$PATH:/home/jpcadiz/SERA2.0-ExternalUsers/SERA_exe_Compiled_Linux/bin


#Change path to reflect the correct scenario folder
cd /home/jpcadiz/New_SERA_Runs/Truck_Demand_Scenarios/Base_Delivery_Pathways_14_years/Exe_prodCF_NG_10_Year_147_Stations_10_Hours_2040
SERA_exe /home/jpcadiz/New_SERA_Runs/Truck_Demand_Scenarios/Base_Delivery_Pathways_14_years/Exe_prodCF_NG_10_Year_147_Stations_10_Hours_2040

