import os
import glob
from pathlib import Path
import utilities
from sys import argv

script, path_to_paired_end_fasta_files, path_to_kraken_executable = argv

# Define text handles

filepath = path_to_paired_end_fasta_files 
kraken   = path_to_kraken_executable 
unique_prefix_seqs = utilities.isolate_folders(filepath)
print(unique_prefix_seqs)

all_strings = []

for unique_prefix_seq in unique_prefix_seqs:

    R1             = filepath + "/" + unique_prefix_seq + "_1P.fq.gz"
    R2             = filepath + "/" + unique_prefix_seq + "_2P.fq.gz"
    isolate_seq1   = Path(R1)
    isolate_seq2   = Path(R2)

    print(isolate_seq1,isolate_seq2)
    if isolate_seq1.is_file() and isolate_seq2.is_file():
        
        isolate_report = "reports/" + unique_prefix_seq + ".report"
        outlog         = "outlogs/" + unique_prefix_seq + ".outlog"

        string = "%s --db minikraken2_v2_8GB --threads 40 --paired --output %s --gzip-compressed --report %s --report-zero-counts %s %s" % (kraken, outlog, isolate_report, isolate_seq1, isolate_seq2)
        all_strings.append(string)

output_slurm = "run_check_contamination.sh"
with open(output_slurm, 'w') as outfile:
    for each_string in all_strings:
        outfile.write(each_string + '\n')

#os.system("mkdir reports; mv *.report reports")
#os.system("mkdir logfiles; mv .outlog logfiles")
