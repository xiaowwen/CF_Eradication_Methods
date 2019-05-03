import pandas as pd
import numpy as np
from Bio.SeqIO.FastaIO import SimpleFastaParser
from sys import argv

script, path_to_allele_loci = argv

# Read sequences of the MLST alleles into a dictionary for easy lookup later

path_to_loci = path_to_allele_loci 
loci_fasta = ['acsA.fas', 'aroE.fas', 'guaA.fas', 'mutL.fas', 'nuoD.fas', 'ppsA.fas', 'trpE.fas']

def read_all_loci_sequences(loci_fastas):

    loci_sequences_dict = {}
    for each_locus in loci_fastas:

        path_locus_file = path_to_loci + '/' + each_locus
        with open(path_locus_file, 'r') as infile:
            for title, seq in SimpleFastaParser(infile):
                title = title #.lower()
                loci_sequences_dict[title] = seq
    return loci_sequences_dict

myseq_dict = read_all_loci_sequences(loci_fasta)

# Read the MLST data for the isolates under consideration, and write the corresponding
# sequences to file for further processing.

mlst_STs = pd.read_csv('PHYLOViZ_data.csv', delimiter='\t', header=0, index_col=0)
mlst_STs_values = mlst_STs.values.tolist()
isolates_indices = mlst_STs.index.tolist()

output_seq_dict = {}
for value, isolate_  in zip(mlst_STs_values, isolates_indices):

    allele_names = ['acsA_' + str(value[1]), 'aroE_' + str(value[2]), 'guaA_' + str(value[3]), 'mutL_' + str(value[4]), 'nuoD_' + str(value[5]), 'ppsA_' + str(value[6]), 'trpE_' + str(value[7])]
    isolate_name = '>' + str(isolate_)
    allele_seq_isolate = ''
    for allele_name in allele_names:
        allele_seq_isolate = ''.join(myseq_dict[allele_name]) 
    output_seq_dict[isolate_name] = allele_seq_isolate

# Finally write all sequences to file
with open('MLSA_sequences.fasta', 'w') as outfile:
    for key_value in output_seq_dict.keys():
        outfile.write(key_value + '\n')
        outfile.write(output_seq_dict[key_value] + '\n')


