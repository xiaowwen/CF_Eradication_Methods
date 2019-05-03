#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40
#SBATCH --time=24:00:00
#SBATCH --job-name=test

module load gcc/7.3.0
module load lmdb/0.9.22
module load gmp/6.1.2
module load boost/1.66.0
module load blast+/2.7.1 

cd /home/d/dguttman/emmanuel/work/eradication_methods/quality_control/6.mlst_mlsa/

/home/d/dguttman/emmanuel/Software/anaconda3/bin/python create_blastDB_from_contigs_mlst.py /home/d/dguttman/emmanuel/work/reproduce_analysis/good_contigs_only_contigs /home/d/dguttman/emmanuel/work/eradication_methods/quality_control/6.mlst_mlsa/mlst_alleles 
