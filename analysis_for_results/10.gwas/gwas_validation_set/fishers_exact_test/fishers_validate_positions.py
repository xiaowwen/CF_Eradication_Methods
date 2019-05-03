import glob
import pandas as pd
import numpy
from sys import argv
import scipy.stats as stats
import statsmodels.api as sm
from scipy.stats import fisher_exact

script, fasta, positions_file, phenotype_file, output_datafile = argv

# Create dictionary of fasta sequences, with header as key and sequence as value:
aligned_seqs_dict = {}
with open(fasta, 'r') as infile1:
    for line in infile1:
        if line.startswith(">"):
            iso_ndx = line.strip().split('>')[1] #.split('_')[0]
            aligned_seqs_dict[str(iso_ndx)] = list(next(infile1).strip())

# Create list of high quality positions:
positions_list = []
with open(positions_file, 'r') as infile2:
    for line in infile2:
        positions_list.append(line.strip()) #.split('-')[1])
outnames = pd.Series(positions_list)

# Convert reference list into a series and label positions with high quality positions list:
reference =  aligned_seqs_dict["REF"]
ref_series = pd.Series(reference, index=positions_list)
ref_df     = pd.DataFrame(reference, index=positions_list, columns = ['REF'])

# Turn sequence dictionary into dataframe, with positions as the column names:
df_filtered_hq_snp_seqs = pd.DataFrame.from_dict(aligned_seqs_dict, orient='index')
df_filtered_hq_snp_seqs.columns = positions_list
df_filtered_hq_snp_seqs.drop(["REF"])

df_filtered_hq_snp_seqs.to_csv(path_or_buf=output_datafile, sep='\t', index=True, header=True)

# Carry out Fishers Exact Test

validation_AET = pd.read_csv(filepath_or_buffer=phenotype_file, sep='\t', header=0, index_col=0) 
SNP_pos = ['930528', '708697', '1871531', '4463848', '928907', '5905798', '4617850', '795950', '5905798']

test_positions = df_filtered_hq_snp_seqs[SNP_pos]
val_test_data = validation_AET.merge(test_positions, left_index=True, right_index=True)

for SNP in SNP_pos:
    print('Reference: ', ref_df.loc[SNP])
    two_by_two_table = sm.stats.Table.from_data(val_test_data[['phenotypes', SNP]])
    print(two_by_two_table.table_orig)
    oddsratio, pvalue = fisher_exact(two_by_two_table.table_orig)
    print('Fisher exact test p-value: {:.4f}'.format(pvalue))
    print("===================================================================================")
