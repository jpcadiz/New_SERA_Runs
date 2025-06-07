#!/bin/bash

#SBATCH --job-name=Exe_prodCF_NG_5_Year_147_Stations_10_Hours_2040_PEM_Only_init_iteration_point_0.3
#SBATCH --time 10:00:00
#SBATCH --account=sera
#SBATCH --chdir=/home/jpcadiz/New_SERA_Runs/Truck_Demand_Scenarios/Base_All_Delivery_Pathways_PEM_Only/Exe_prodCF_NG_5_Year_147_Stations_10_Hours_2040_init_iteration_point_0.3
#SBATCH -o SERA.log
#SBATCH --mail-user=jpcadiz@ucdavis.edu
#SBATCH --mail-type=ALL

module purge
module load xpressmp
module load gurobi

export PATH=$PATH:/home/jpcadiz/SERA2.0-ExternalUsers/SERA_exe_Compiled_Linux/bin


#Change path to reflect the correct scenario folder
cd /home/jpcadiz/New_SERA_Runs/Truck_Demand_Scenarios/Base_All_Delivery_Pathways_PEM_Only/Exe_prodCF_NG_5_Year_147_Stations_10_Hours_2040_init_iteration_point_0.3
SERA_exe /home/jpcadiz/New_SERA_Runs/Truck_Demand_Scenarios/Base_All_Delivery_Pathways_PEM_Only/Exe_prodCF_NG_5_Year_147_Stations_10_Hours_2040_init_iteration_point_0.3

