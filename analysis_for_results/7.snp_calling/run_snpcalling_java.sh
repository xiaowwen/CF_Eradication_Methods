#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40
#SBATCH --time=24:00:00
#SBATCH --job-name=jSNPCalling
#SBATCH --output=jSNPCalling_outlog.txt

module load java

java -jar SNPCallingPipeline.jar gethqsnps conf.intra.txt 
java -jar SNPCallingPipeline.jar getintraclonalsnps conf.intra.txt
java -jar SNPCallingPipeline.jar snpchecker conf.intra.txt
java -jar SNPCallingPipeline.jar snpfilter conf.intra.txt
java -jar SNPCallingPipeline.jar createalignment conf.intra.txt
