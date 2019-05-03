import os
import glob
from pathlib import Path
import math
from sys import argv

script, path_to_denovo_assembly, path_to_blastn_executable = argv

# Define text handles

filepath           = path_to_denovo_assembly
blastn             = path_to_blastn_executable

prefix_seqs        = glob.glob(filepath + '*/contigs.fasta')
unique_prefix_seqs = [prefix.split('/')[-2] for prefix in prefix_seqs]
all_strings        = []

for unique_prefix_seq in unique_prefix_seqs:

    os.system('mkdir %s' % unique_prefix_seq)
    contigs_fasta       = filepath + unique_prefix_seq + "/contigs.fasta"
    formatted_results   = unique_prefix_seq + "/" + unique_prefix_seq + "_blastn_results.txt"

    if contigs_fasta:
        string = '%s -db nt -query %s -out %s -evalue 0.00001 -outfmt "7 qseqid sseqid pident length evalue sscinames" -num_threads 20' % (blastn, contigs_fasta,formatted_results) 
        all_strings.append(string)

output_slurm = "blastn_on_contigs.sh"
with open(output_slurm, 'w') as outfile:
    for each_string in all_strings:
        outfile.write(each_string + '\n')

