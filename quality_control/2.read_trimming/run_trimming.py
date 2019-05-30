import os
import glob
from pathlib import Path
import utilities
from sys import argv

script, path_to_paired_end_fasta_files, path_to_Trimmomatic_executable = argv

# Define text handles

filepath           = path_to_paired_end_fasta_files
Trimmomatic        = path_to_Trimmomatic_executable
unique_prefix_seqs = utilities.isolate_folders(filepath)

all_strings = []

for unique_prefix_seq in unique_prefix_seqs:

    R1             = filepath + "/" + unique_prefix_seq + "_1.fq.gz"
    R2             = filepath + "/" + unique_prefix_seq + "_2.fq.gz"
    isolate_seq1   = Path(R1)
    isolate_seq2   = Path(R2)
    output_base    = unique_prefix_seq + ".fq.gz"

    if isolate_seq1.is_file() and isolate_seq2.is_file():
        
        output_base    = unique_prefix_seq + ".fq.gz" 
        outlog         = unique_prefix_seq + ".outlog"
        string = "java -jar %s PE -threads 40 %s %s -baseout %s CROP:150 SLIDINGWINDOW:4:5 ILLUMINACLIP:NexteraPE-PE.fa:2:30:10 MINLEN:100" % (Trimmomatic, isolate_seq1, isolate_seq2, output_base)
        all_strings.append(string)

output_slurm = "trimming_reads.sh"
with open(output_slurm, 'w') as outfile:
    for each_string in all_strings:
        outfile.write(each_string + '\n')
