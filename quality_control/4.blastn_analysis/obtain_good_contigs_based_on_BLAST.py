import os
import glob
from pathlib import Path
from Bio import SeqIO
import numpy as np
from sys import argv

script, path_to_denovo_assembly = argv

# Grab files
blast_result_files = glob.glob("*/*_blastn_results.txt")
blast_result_files.sort()
assembly_path = path_to_denovo_assembly

##
##  Parse blast report to identify good contigs: 1. Have at least one Pseudomonas taxonomic label 
##  2. Coverage more than 10 and sequence length more than 1000.
##  Blastn command: blastn -db nt -query %s -out %s -evalue 0.00001 -outfmt "7 qseqid sseqid pident length evalue sscinames"
##

def parse_blastn_file(blast_output):

    blast_prefix = blast_output.split('/')[-1]
    contig_file_name = assembly_path + blast_prefix[:-19] + "/contigs.fasta"
    f = open(blast_output)
    lines = f.readlines()

    unique_contigs_list = []

    for line in lines:

       if line.startswith("NODE"):

           data = line.strip().split()
           contig_name = data[0]
           taxo_label = data[5]

           contig_info = contig_name.split('_') 
          
           contig_node    = contig_info[1]
           coverage = contig_info[5]
           contig_len = contig_info[3]

           if taxo_label == 'Pseudomonas':
           
               if (float(contig_len) > 1000.0) and (float(coverage) > 10.0):
                   good_contig = 1
                   color    = 'deepskyblue'
               else:
                   good_contig = 0
                   color       = 'red'
           else:
               good_contig = 0
               color       = 'red'

           all_names = [unique_contigs_list[i][0] for i in range(len(unique_contigs_list))]
           
           if contig_name in all_names:
               position = all_names.index(contig_name)
             
               if unique_contigs_list[position][4] == 0:
                   if good_contig == 1:
                       unique_contigs_list[position][4] = 1
           else:
               unique_contigs_list.append([contig_name, contig_node, coverage, contig_len, good_contig, color])

    return [contig_file_name, unique_contigs_list]

##
## Generate parsed blastn results. Use SeqIO (biopython) to write good contigs to a fasta file
##

for blast_result_file in blast_result_files:

    print(blast_result_file)
    contigs_file_name, parsed_list = parse_blastn_file(blast_result_file)
    full_denovo_contigs = list(SeqIO.parse(contigs_file_name, "fasta"))
    print(contigs_file_name)
    good_contigs_names = []
    for _contig in parsed_list:
       if _contig[4] == 1:
           good_contigs_names.append(_contig[0])

    good_full_contigs = []
    for full_denovo_contig in full_denovo_contigs:
        if full_denovo_contig.name in good_contigs_names:
            good_full_contigs.append(full_denovo_contig)
    
    output_contigs = blast_result_file[:-19] + "_out_contigs.fasta" 
    with open(output_contigs, 'w') as outfile1:
        SeqIO.write(good_full_contigs, outfile1, "fasta")

#outfile = open('parsed_blast_results.txt', 'w')
#for parsed_line in parsed_list:
#    wline = str(parsed_line[0]) + '\t' + str(parsed_line[1]) + '\t'+ str(parsed_line[2]) + '\t' + str(parsed_line[3]) + '\t'+ str(parsed_line[4]) + '\t' + str(parsed_line[5]) + '\n'
#    outfile.write(str(wline))
