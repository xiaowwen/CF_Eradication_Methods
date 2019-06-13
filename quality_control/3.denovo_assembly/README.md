This script creates submission file to run SPADEs denovo assembly for a set of
trimmed paired end reads (assummed to end with _1P.fq.gz and _1U.fq.gz).

Run:

python run_denovo_assembly.py  path_to_paired_end_fasta_files path_to_Spades_executable

The assembly_stats.py script obtains some statistics for the assmblies. It assumes the folders with 
all the assembly files are located in the current directory. The requires the presence of the QUAST
program to run.

python assembly_stats.py path_to_QUAST_executable
