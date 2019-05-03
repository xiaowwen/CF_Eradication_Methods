import os
import glob
from pathlib import Path
import utilities
from sys import argv

script, path_to_trimmed_reads, path_to_good_contigs = argv

# Gather required files
filepath             = path_to_trimmed_reads 
blastn_analysis_path = path_to_good_contigs 
unique_prefix_seqs   = utilities.isolate_folders(filepath)
all_strings          = []

# Software paths
samtools             = full_path_to_samtools_executeable #"/home/d/dguttman/diazcaba/Software/samtools-1.8/samtools"
bwa                  = full_path_to_bwa_executeable #"/home/d/dguttman/diazcaba/Software/bwa-0.7.17/bwa"
picard               = full_path_to_picard_executeable #"/home/d/dguttman/diazcaba/Software/picard.jar"
bcftools             = full_path_to_bcftools_executeable #"/home/d/dguttman/diazcaba/Software/bcftools-1.8/bcftools"

for unique_prefix_seq in unique_prefix_seqs:

    R1             = filepath + '/' + unique_prefix_seq + "_1P.fq.gz"
    R2             = filepath + '/' + unique_prefix_seq + "_2P.fq.gz"
    isolate_seq1   = Path(R1)
    isolate_seq2   = Path(R2)

    contigs_fasta       = blastn_analysis_path + unique_prefix_seq + "_out_contigs.fasta"
    contigs_fasta_      = unique_prefix_seq + "_out_contigs.fasta"
    contigs_fasta_star  = unique_prefix_seq + "_out_contigs.fasta.*"
    aligned_results     = unique_prefix_seq + "_aligned_sorted.bam"
    aligned_veiw1       = unique_prefix_seq + "_F12.sam"
    aligned_veiw2       = unique_prefix_seq + "_f8F4.sam"
    aligned_veiw3       = unique_prefix_seq + "_f4F8.sam"
    merged_views        = unique_prefix_seq + "_merged.bam"
    merged_sorted       = unique_prefix_seq + "_merged_sorted.bam"
    merged_R1           = unique_prefix_seq + "_merged.R1.fq.gz"
    merged_R2           = unique_prefix_seq + "_merged.R2.fq.gz"

    if isolate_seq1.is_file() and isolate_seq2.is_file():

        os.system("mkdir %s; cd %s; cp %s ." % (unique_prefix_seq, unique_prefix_seq, contigs_fasta))
        string1 = "%s index %s; %s faidx %s" % (bwa, contigs_fasta_, samtools, contigs_fasta_)
        string2 = "%s mem -t 20 %s %s %s  | %s sort -o %s --threads 20" % (bwa, contigs_fasta_, isolate_seq1, isolate_seq2, samtools, aligned_results)
        string3 = "%s view --threads 20 -h %s -F 12 > %s " % (samtools, aligned_results, aligned_veiw1)
        string4 = "%s view --threads 20 -h %s -f 8 -F 4 > %s" % (samtools, aligned_results, aligned_veiw2)
        string5 = "%s view --threads 20 -h %s -f 4 -F 8 >  %s" % (samtools, aligned_results, aligned_veiw3)
        string6 = "%s merge --threads 20 %s %s %s %s" % (samtools, merged_views, aligned_veiw1, aligned_veiw2, aligned_veiw3)
        string7 = "%s sort --threads 20 %s -o %s" % (samtools, merged_views, merged_sorted)
        string8 = "java -jar %s SamToFastq INPUT=%s  FASTQ=%s SECOND_END_FASTQ=%s" % (picard, merged_sorted, merged_R1, merged_R2)
        string9 = "rm %s %s %s %s %s %s %s %s" % (aligned_results, aligned_veiw1, aligned_veiw2, aligned_veiw3, merged_views, merged_sorted, contigs_fasta_, contigs_fasta_star)

    all_strings = [string1,string2,string3,string4,string5,string6,string7,string8,string9]

    output_slurm = unique_prefix_seq + '_slurm.sh'

    with open(output_slurm, 'w') as outfile:

        outfile.write('\n')
        for each_string in all_strings:
            outfile.write(each_string + '\n')

    os.system("mv %s %s" %(output_slurm, unique_prefix_seq) )
