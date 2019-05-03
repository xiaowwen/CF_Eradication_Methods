This script takes as input trimmed reads (paired end fastas) and corresponding contigs generated from
denovo assembly and carries out alignment to output paired end fastas that are contained in good contigs.
Good contigs that are 1. Have at least one Pseudomonas taxonomic label 2. At least 10X Coverage  and 
sequence length more than 1000.

Usage:
python align_to_good_contigs.py path_to_trimmed_reads/ path_to_good_contigs/

Requirements:

# Software paths
samtools             = full_path_to_samtools_executeable e.g. "/full/path/to/samtools-1.8/samtools"
bwa                  = full_path_to_bwa_executeable 
picard               = full_path_to_picard_executeable 
bcftools             = full_path_to_bcftools_executeable

This should be provided by editing those sections in the script. 



