import os
import glob
from pathlib import Path
import utilities
import math
from sys import argv

script, path_to_good_contigs, path_to_prokka_executeable = argv

prokka_exe = path_to_prokka_executeable 
assembly_path  = path_to_good_contigs 

files = glob.glob(assembly_path + "/" + "*.fa")
prefixes = [ line.split('/')[-1].split('.')[0] for line in files]
unique_prefix_seqs = list(set(prefixes))

for unique_prefix_seq in unique_prefix_seqs:

    good_contigs   = unique_prefix_seq + '.fa'
    contigs_fasta  = assembly_path + "/" + good_contigs # unique_prefix_seq + "/contigs.fasta"

    if Path(contigs_fasta).is_file():
        os.system("%s --cpus 8 --genus Pseudomonas --species aeruginos --kingdom Bacteria --gcode 11 --mincontiglen 200 --proteins GCF_000006765.1_ASM676v1_genomic.gbff --usegenus --rfam --prefix %s %s" % (prokka_exe, unique_prefix_seq, contigs_fasta) )
