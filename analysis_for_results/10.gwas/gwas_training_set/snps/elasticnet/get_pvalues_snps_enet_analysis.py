import numpy as np
import pandas as pd
from sys import argv
import math
from pprint import pprint

script, snp_gwas_input = argv

snps_gwas_out = open(snp_gwas_input)
input_snps = pd.read_csv(filepath_or_buffer=snp_gwas_input, sep='\t', header=0, index_col=0)
snp_details = input_snps.index.values.tolist()

snp_pos     = [ snp_detail.split('_')[2] for snp_detail in snp_details ]
chromosome  = [ snp_detail.split('_')[0] + '_' + snp_detail.split('_')[1] for snp_detail in snp_details ]

#pvalue      = -1.0*np.log10(input_snps['lrt-pvalue'].values) 
pvalue      = -1.0*np.log10(input_snps['filter-pvalue'].values)

ouput_list = []

for i in range(len(snp_pos)):
    ouput_list.append([chromosome[i], '.', snp_pos[i], pvalue[i], pvalue[i], 0])

header = ['#CHR', 'SNP', 'BP', 'minLOG10(P)', 'log10(p)', 'r^2']
output_df = pd.DataFrame(ouput_list, columns=header)
output_df.to_csv(path_or_buf='snps_gwas_out.plot', header=True, index=False, sep='\t')

threshhold = -1.0*math.log10(0.05/36956.0) 
pvalue_gt_10 = np.where(pvalue > threshhold)
