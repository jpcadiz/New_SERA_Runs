#!/bin/bash

#SBATCH --job-name=Exe_prodCF_NG_25_Original
#SBATCH --time 48:00:00
#SBATCH --account=sera
#SBATCH --chdir=/home/jpcadiz/New_SERA_Runs/Exe_prodCF_NG_25_Original
#SBATCH -o SERA.log
#SBATCH --mail-user=jpcadiz@ucdavis.edu
#SBATCH --mail-type=ALL

module purge
module load xpressmp
module load gurobi

export PATH=$PATH:/home/jpcadiz/SERA2.0-ExternalUsers/SERA_exe_Compiled_Linux/bin


#Change path to reflect the correct scenario folder
cd /home/jpcadiz/New_SERA_Runs/Exe_prodCF_NG_25_Original
SERA_exe /home/jpcadiz/New_SERA_Runs/Exe_prodCF_NG_25_Original


