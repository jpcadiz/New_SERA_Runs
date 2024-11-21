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

export PATH=$PATH:/kfs2/projects/sera/julia/julia-1.9.2/bin/

cd /kfs2/projects/sera/SERA2.0_dev/SERA.jl

julia --project /kfs2/projects/sera/SERA2.0_dev/SERA.jl/examples/sera_development/USA-Sample-Test-Large-SupDemCurve-ANNon/run_case_hpc.jl

# export LD_LIBRARY_PATH=/projects/mbap/sera/bin/lib



