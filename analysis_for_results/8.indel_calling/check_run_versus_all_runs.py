import utilities
import os

sequences = '/scratch/d/dguttman/emmanuel/reproduce_analysis/5.align_to_good_contigs_Reference_Mapping/sequence_reads_after_align_to_good_contigs/combined_set/'
unique_prefix_seqs = utilities.isolate_folders(sequences)

all_filtered_vcfs = []

for unique_prefix_seq in unique_prefix_seqs:
    filtered_vcf = unique_prefix_seq + "_gatk_bwa_filtered.vcf"
    all_filtered_vcfs.append(filtered_vcf)

f = open('/scratch/d/dguttman/emmanuel/reproduce_analysis/9.indel_calling/analysis/alignments/err').readlines()

all_completed_vcfs = [ line.split()[-1].split('/')[-1] for line in f]

uncompleted = list(set(all_filtered_vcfs) - set(all_completed_vcfs))
uncompleted_dirs = [uncomplete.split('_')[0] for uncomplete in uncompleted]

path_to_alignments = '/scratch/d/dguttman/emmanuel/reproduce_analysis/9.indel_calling/analysis/alignments/'

with open("parallel_slurm_uncompleted.sh", "w") as outfile:

    for uncompleted_dir in uncompleted_dirs:

        run_dir = path_to_alignments + uncompleted_dir + '/'
        runfile = ' && ./new_' + uncompleted_dir + '_get_indels.sh'
        program_calls_file = uncompleted_dir + '_get_indels.sh'
        new_sh_file = 'new_' + uncompleted_dir + '_get_indels.sh'
        string = '\t' + 'cd ' + uncompleted_dir + runfile# + '\n'
        print(string)
        outfile.write(string + '\n')

        os.system('cd %s; tail -n16 %s > %s' % (run_dir, program_calls_file, new_sh_file) )

