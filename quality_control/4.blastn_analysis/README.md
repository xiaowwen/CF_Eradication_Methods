The run_blast_on_contigs.py scripts blasts the denovo assemblies to determine if they are Pseudomonas Aureuginosa.
Blastn command: blastn -db nt -query %s -out %s -evalue 0.00001 -outfmt "7 qseqid sseqid pident length evalue sscinames"

Usage:

python run_blast_on_contigs.py path_to_denovo_assembly path_to_blastn_executable

Next the obtain_good_contigs_based_on_BLAST.py script parses the blast report to identify good contigs: 
1. Have at least one Pseudomonas taxonomic label 
2. Coverage more than 10 and sequence length more than 1000.

Usage:

python obtain_good_contigs_based_on_BLAST.py  path_to_denovo_assembly.

It assumes the blast output files are in the current directory
