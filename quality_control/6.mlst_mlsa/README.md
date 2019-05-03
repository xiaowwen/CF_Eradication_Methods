The scripts in this folder are used for MLST and MLSA analysis.

1. The create_blastDB_from_contigs_mlst.py script takes a directory containing (denovo) contigs and creates a BLAST
   database. Next it runs blastn of the 7 genes against these databases, writing the output into the dictory containing
   the BLAST database.

Usage: python create_blastDB_from_contigs_mlst.py path_to_contigs_folder. The blastn executable should be in your path.

2. The get_mlst_best_matching_allele.py script, reads the outputs of blastn from above and calculates the sequence types.
   It requires the presence of the ST profiles data (mlst_profiles_csv) and additional info for the isolates here
   (isolate_background_data.csv). It outputs strain list output file that can be used by software like PHYLOViZ.

Usage: python get_mlst_best_matching_allele.py mlst_output_path/ mlst_profiles isolate_background_data.

3. The obtain_alleles_sequence_for_mlsa.py uses the strain information and seqeunces from the 7 housekeeping genes to
   write out a multiple alignment fasta file.

Usage: python obtain_alleles_sequence_for_mlsa.py path_to_allele_loci (acsA.fas etc) 
