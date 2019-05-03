import os
import glob
from pathlib import Path
from sys import argv
import utilities

script, path_to_paired_end_fasta_files, path_to_Spades_executable = argv

# Define text handles

filepath           = path_to_paired_end_fasta_files
Spades             = path_to_Spades_executable 
unique_prefix_seqs = utilities.isolate_folders(filepath)

# Grab files
files = glob.glob(filepath + "/*P.fq.gz")
files.sort()
all_strings = []

for unique_prefix_seq in unique_prefix_seqs:

    R1             = filepath + unique_prefix_seq + "_1P.fq.gz"
    R2             = filepath + unique_prefix_seq + "_2P.fq.gz"
    isolate_seq1   = Path(R1)
    isolate_seq2   = Path(R2)

    if isolate_seq1.is_file() and isolate_seq2.is_file():
        print("Running de novo assembly for isolate sequences ", R1 , " and ", R2)
        output_base    = unique_prefix_seq 
        string = "%s -o %s -1 %s -2 %s --careful " % (Spades, output_base, isolate_seq1, isolate_seq2) 
        #os.system("%s -o %s -1 %s -2 %s --careful " % (Spades, output_base, isolate_seq1, isolate_seq2) )
        all_strings.append(string)

output_slurm = "spades_denovo_assembly.sh"
with open(output_slurm, 'w') as outfile:
    for each_string in all_strings:
        outfile.write(each_string + '\n')


