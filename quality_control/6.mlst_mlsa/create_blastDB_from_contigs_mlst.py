import os
import glob
from pathlib import Path
from sys import argv

script, path_to_denovo_contigs, path_to_locus_alleles = argv

# Denovo assembled contigs after alignment to good contigs
assembly_path = path_to_denovo_contigs 
files = glob.glob(path_to_denovo_contigs + "*.fa")

prefixes = [ line.split('/')[-1].split('.')[0] for line in files]
unique_prefix_seqs = list(set(prefixes))

for unique_prefix_seq in unique_prefix_seqs:

    contigs_fasta       = assembly_path + unique_prefix_seq + ".fa"
    formatted_results   = unique_prefix_seq + "_blastn_results.txt"

    if Path(contigs_fasta).is_file(): 
        os.system('mkdir %s' % unique_prefix_seq)
        print("Creating BLAST database for contig:  ", unique_prefix_seq)

        acs_allele = path_to_locus_alleles + "/acsA.fas"
        aro_allele = path_to_locus_alleles + "/aroE.fas"
        gua_allele = path_to_locus_alleles + "/guaA.fas"
        mut_allele = path_to_locus_alleles + "/mutL.fas"
        nuo_allele = path_to_locus_alleles + "/nuoD.fas"
        pps_allele = path_to_locus_alleles + "/ppsA.fas"
        trp_allele = path_to_locus_alleles + "/trpE.fas"

        os.system('cd %s; makeblastdb -in %s -dbtype "nucl" -out %s' % (unique_prefix_seq, contigs_fasta, unique_prefix_seq) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out acsA.out' % (unique_prefix_seq, unique_prefix_seq, acs_allele) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out aroE.out' % (unique_prefix_seq, unique_prefix_seq, aro_allele) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out guaA.out' % (unique_prefix_seq, unique_prefix_seq, gua_allele) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out mutL.out' % (unique_prefix_seq, unique_prefix_seq, mut_allele) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out nuoD.out' % (unique_prefix_seq, unique_prefix_seq, nuo_allele) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out ppsA.out' % (unique_prefix_seq, unique_prefix_seq, pps_allele) )
        os.system('cd %s; blastn -db %s -query %s -evalue 0.00001 -out trpE.out' % (unique_prefix_seq, unique_prefix_seq, trp_allele) )

