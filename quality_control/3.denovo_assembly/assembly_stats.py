import os
import glob
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sys import argv

script, path_to_QUAST_executable = argv

# Define text handles

filepath           = "./"
QUAST              = path_to_QUAST_executable

# Grab files
files = glob.glob("./*/contigs.fasta")
files.sort()
unique_prefix_seqs = [contig.split('/')[1] for contig in files]
stats_data = []

for unique_prefix_seq in unique_prefix_seqs:

    if unique_prefix_seq:
 
        print("Running QUAST analysis of the contigs obtained from the de novo assembly of isolate ", unique_prefix_seq)
        output_base    = unique_prefix_seq 
        os.system("cd %s; %s -m 1000 -o viz_out contigs.fasta" % (output_base, QUAST) )

        stats_text_f   = unique_prefix_seq + "/viz_out/transposed_report.txt"
        stats_file     = open(stats_text_f)
        lines          = stats_file.readlines()
        contig_stats   = lines[3].strip().split()
        largest_contig = float(contig_stats[14])
        n50            = float(contig_stats[17])
        n75            = float(contig_stats[18])
        assembly_len   = float(contig_stats[8])
        num_of_contigs = float(contig_stats[13])

        stats_data.append([largest_contig,n50,n75,assembly_len,num_of_contigs])

np.savetxt("contigs_stats.txt",stats_data)

# Plot de novo assembly statistics

stats_array = np.array(stats_data)

plt.clf()
plt.subplots(311)
plt.plot(stats_array[:,4],stats_array[:,1]/1000.0)
plt.xlabel("Number of Contigs")
plt.ylabel("N50(Kbp)")

plt.subplots(312)
plt.plot(stats_array[:,3]/1000000.0,stats_array[:,1]/1000.0)
plt.xlabel("Assembly Length (Mbp)")
plt.ylabel("N50(Kbp)")

plt.subplots(313)
plt.plot(stats_array[:,4],stats_array[:,3]/1000000.0)
plt.xlabel("Number of Contigs")
plt.ylabel("Assembly Length (Mbp)")

plt.show()
