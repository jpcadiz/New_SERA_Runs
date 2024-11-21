#!/bin/bash

#SBATCH --job-name=USA-Sample-Test-Large-SupDemCurve-ANNon
#SBATCH --time=0-00:10:00
#SBATCH -A sera
#SBATCH --mem=150G
#SBATCH --chdir=/home/jpcadiz/New_SERA_Runs/test-cases/USA-Sample-Test-Large-SupDemCurve-ANNon
#SBATCH -o USA-Sample-Test-Large-SupDemCurve-ANNon.log
#SBATCH --mail-user=jpcadiz@ucdavis.edu
#SBATCH --mail-type=ALL

module purge
module load xpressmp
module load gurobi

export PATH=$PATH:/home/jpcadiz/SERA2.0-ExternalUsers/SERA_exe_Compiled_Linux/bin

#Change path to reflect the correct scenario folder
cd /home/jpcadiz/New_SERA_Runs/test-cases/USA-Sample-Test-Large-SupDemCurve-ANNon
SERA_exe /home/jpcadiz/New_SERA_Runs/test-cases/USA-Sample-Test-Large-SupDemCurve-ANNon


