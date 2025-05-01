#!/bin/bash

#SBATCH --job-name=BaseA_5Db_prodCF_NG
#SBATCH --time 48:00:00
#SBATCH --account=sera
#SBATCH --chdir=/home/ccyang/SERA-supply-chain-inputs/cases/BaseA_5Db_prodCF_NG
#SBATCH --output=BaseA_5Db_prodCF_NG.out 
#SBATCH --error=BaseA_5Db_prodCF_NG.err
#SBATCH --mail-user=ccyang@ucdavis.edu
#SBATCH --mail-type=ALL

module purge
module load conda
# module load julia
module load xpressmp
module load gurobi
export PATH=$PATH:/home/ccyang/julia_software/julia-1.7.3/bin/

cd /home/ccyang/SERA-supply-chain-inputs/cases/BaseA_5Db_prodCF_NG


julia run_case_gurobi.jl




