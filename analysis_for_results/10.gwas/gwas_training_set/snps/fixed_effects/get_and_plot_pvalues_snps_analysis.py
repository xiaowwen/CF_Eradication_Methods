import numpy as np
import pandas as pd
from sys import argv
import math
from pprint import pprint
import matplotlib.pyplot as plt
from scipy.stats import chi2

script, snp_gwas_input = argv

snps_gwas_out = open(snp_gwas_input)

input_snps = pd.read_csv(filepath_or_buffer=snp_gwas_input, sep='\t', header=0, index_col=0)

snp_details = input_snps.index.values.tolist()

snp_pos     = [ int(snp_detail.split('_')[2]) for snp_detail in snp_details ]
chromosome  = [ snp_detail.split('_')[0] + '_' + snp_detail.split('_')[1] for snp_detail in snp_details ]

print(snp_pos)

base_pvalue = input_snps['filter-pvalue'].values
pvalue      = -1.0*np.log10(input_snps['lrt-pvalue'].values) 

print(len(pvalue))

# Plot Manhattan plot
#plt.plot(snp_pos, pvalue)
#plt.show()

ouput_list = []

for i in range(len(snp_pos)):

    ouput_list.append([chromosome[i], '.', snp_pos[i], pvalue[i], pvalue[i], 0])

header = ['#CHR', 'SNP', 'BP', 'minLOG10(P)', 'log10(p)', 'r^2']
output_df = pd.DataFrame(ouput_list, columns=header)
output_df.to_csv(path_or_buf='snps_gwas_out.plot', header=True, index=False, sep='\t')

pvalue_gt_3 = np.where(pvalue > 3)
df_pvalue_gt_3 = output_df.loc[pvalue_gt_3]
log10Pval = df_pvalue_gt_3['log10(p)'].values
_chrom_pos = df_pvalue_gt_3['BP'].values
chrom_pos = [int(each_pos) for each_pos in _chrom_pos]

# Plot Manhattan plot
plt.plot(snp_pos, pvalue, 'k.', ms=4)
plt.axhline(y=-1.0*math.log10(0.05/len(pvalue)), linewidth=1, color='r')
#plt.xticks([1E06, 2E06, 3E06, 4E06, 5E06, 6E06],size='10', rotation='horizontal')
plt.xticks([1E06, 2E06, 3E06, 4E06, 5E06, 6E06], ('1e+6', '2e+6', '3e+6', '4e+6', '5e+6', '6e+6'), size='10', rotation='horizontal')
plt.ylabel('-log10(p)', size='14')
plt.xlabel('Chromosome Position', size='14')
plt.savefig('training_snps_fixed_PCAs.png')

# Plot variant h squared
#plt.clf()
#variant_h2 = input_snps['variant_h2'].values
#print(variant_h2)
#plt.plot(chromosome, variant_h2, 'k.', ms=4)
#plt.plot(variant_h2, 'k.', ms=0.1)
#plt.show()


# Calculate genomic inflation factors

chisq = chi2.pdf((1-base_pvalue), df=1)
#print( np.median(chisq)  )
#print(base_pvalue)
gwas_lambda = np.median(chisq)/(chi2.pdf(0.5, df=1))
print("Genomic Inflation Factor (lambda): ", gwas_lambda)

np.savetxt('base_pvalue.txt', base_pvalue, fmt='%1.16f')
