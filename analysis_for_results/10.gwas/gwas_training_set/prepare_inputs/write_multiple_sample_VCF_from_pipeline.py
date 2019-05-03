import glob
import pandas as pd
import numpy
from sys import argv

script, fasta, positions_file, output_vcf = argv

# Create dictionary of fasta sequences, with header as key and sequence as value:
aligned_seqs_dict = {}

with open(fasta, 'r') as infile1:
    for line in infile1:
        if line.startswith(">"):
            aligned_seqs_dict[line.strip()] = list(next(infile1).strip())

# Create list of high quality positions:
positions_list = []
with open(positions_file, 'r') as infile2:
    for line in infile2:
        positions_list.append(line.strip()) #.split('-')[1])
outnames = pd.Series(positions_list)
reference = aligned_seqs_dict[">REF"] 

# Convert reference list into a series and label positions with high quality positions list:
ref_series = pd.Series(reference, index=positions_list)

# Turn sequence dictionary into dataframe, with positions as the column names:
df_filtered_hq_snp_seqs = pd.DataFrame.from_dict(aligned_seqs_dict, orient='index') 
df_filtered_hq_snp_seqs.columns = positions_list

filtered_hq_pos = df_filtered_hq_snp_seqs.columns
isolates        = df_filtered_hq_snp_seqs.index.values
multiple_vcf    = output_vcf
variant_strings = []

# Write header 
hstring1 = '##fileformat=VCFv4.2'
hstring2 = '##fileDate=20170502'
hstring3 = '##source=PLINKv1.90'
hstring4 = '##contig=<ID=NC_002516.2,length=6264404>'
hstring5 = '##INFO=<ID=PR,Number=0,Type=Flag,Description="Provisional reference allele, may not be based on real reference genome">'
hstring6 = '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">'
hstring7 = '#CHROM' + '\t' + 'POS' + '\t' + 'ID' + '\t' + 'REF' + '\t' + 'ALT' + '\t' + 'QUAL' + '\t' + 'FILTER' + '\t' + 'INFO' + '\t' + 'FORMAT'
hstrings = [hstring1,hstring2,hstring3,hstring4,hstring5,hstring6]

with open('header_multiple_vcf.txt', 'w') as hfile:
    for _string in hstrings:
        hfile.write(_string + '\n')
    for replicon in isolates:
        if replicon != '>REF':
            rep_name = replicon.split('>')[1]
            hstring7 = hstring7 + '\t' + rep_name
    hfile.write(hstring7 + '\n')

for filtered_hq in filtered_hq_pos:

    print("Analysis for position: ", filtered_hq)
    ref_at_pos            = ref_series.loc[filtered_hq]
    alt_at_pos            = df_filtered_hq_snp_seqs[filtered_hq].values.tolist()
    alt_at_pos            = list(set(alt_at_pos))

    if len(alt_at_pos) == 1:
        alt_at_pos = alt_at_pos[0]
    elif len(alt_at_pos) == 2:
        if ref_at_pos in alt_at_pos:
            alt_at_pos.pop(alt_at_pos.index(ref_at_pos))
    else:
        print("There cannot be more then one variant per position")
        alt_at_pos = ['.']

    string  =  ''
    for isolate in isolates:

        alt_seqs_for_isolate = df_filtered_hq_snp_seqs.loc[isolate,filtered_hq]

        if alt_seqs_for_isolate == ref_at_pos:
            string = string + '0/0'  + '\t'
        else:
            if alt_seqs_for_isolate != '.':
                string = string + '1/1' + '\t'
            else:
                string = string + './.' + '\t'

    variant = 'NC_002516.2' + '\t' + filtered_hq + '\t' + '.' + '\t' + ref_at_pos + '\t' + alt_at_pos[0] + '\t' + '.' + '\t'  + '.' + '\t' + 'PR' +  '\t' + 'GT' + '\t' + string
    variant_strings.append(variant)

with open(multiple_vcf, 'w') as outfile:

    #Write Header
    hstring7 = '#CHROM' + '\t' + 'POS' + '\t' + 'ID' + '\t' + 'REF' + '\t' + 'ALT' + '\t' + 'QUAL' + '\t' + 'FILTER' + '\t' + 'INFO' + '\t' + 'FORMAT'
    for _string in hstrings:
        outfile.write(_string + '\n')
    for replicon in isolates:
        if replicon != '>REF':
            rep_name = replicon.split('>')[1]
            hstring7 = hstring7 + '\t' + rep_name
    outfile.write(hstring7 + '\n')

    # Write Variants
    for variant_string in variant_strings:
        outfile.write(variant_string + '\n')
