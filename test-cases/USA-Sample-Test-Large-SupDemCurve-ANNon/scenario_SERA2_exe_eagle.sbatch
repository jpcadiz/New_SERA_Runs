#!/bin/bash

#SBATCH --job-name=USA-Sample-Test-Large-SupDemCurve-ANNon
#SBATCH --time=0-00:10:00
#SBATCH -A sera
#SBATCH --mem=150G
#SBATCH -o USA-Sample-Test-Large-SupDemCurve-ANNon.log
#SBATCH --mail-user=jbracci@nrel.gov
#SBATCH --mail-type=ALL

module purge
module load xpressmp
module load gurobi

export PATH=$PATH:/lustre/eaglefs/projects/sera/SERA2.0/SERA_exe_Compiled_Eagle/bin

chmod a+x SERA_exe

SERA_exe /lustre/eaglefs/projects/sera/SERA2.0_dev/SERA.jl/USA-Sample-Test-Large-SupDemCurve-ANNon




