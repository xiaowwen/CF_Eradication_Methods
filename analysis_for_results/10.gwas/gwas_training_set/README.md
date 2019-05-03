This folder contains the GWAS analysis (mainly on SNPs) using the PySEER python package. To download and install this
package see: https://pyseer.readthedocs.io/en/master/installation.html.

In the snps directory, there are 3 subdirectories:

1. fixed_effects/: the gwas analysis in this directory uses PCA analysis of inter-seqeunce distances to control
   for population structure. The outlog file shows the particulars of the run. Calling PySEER with the -h arguement
   provides further information on all options. More info can also be found at https://pyseer.readthedocs.io/en/master/usage.html
   or https://pyseer.readthedocs.io/en/master/tutorial.html.

2. random_effects_lmm/: gwas analysis using a mixed linear model using a kinship matrix calculated from the SNPs. PySEER provides 
   a script for this and can be run as: similarity --vcf multiple_snp_alignment.vcf.gz samples.txt > gg.snps.txt.

3. elasticnet/: gwas analysis using logistic regression as well but with both Ridge and Lasso penalties. Details of options can be 
   obtained from the web-links in (1) above.
  
