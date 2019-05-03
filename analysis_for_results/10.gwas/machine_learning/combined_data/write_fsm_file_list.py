import glob

training_list = open('combined_list.txt').readlines()
fsm_file_name = 'combined_fsm_file_list.txt'
fsm_list      = []

phenotypes    = open('total_phenotype_input.csv').readlines()
phenotype_file = 'combined_resistances.pheno'

with open(fsm_file_name, 'w') as fsm_out:
    for training_isolate in training_list:
        line_for_file = training_isolate.strip()
        fsm_list.append(line_for_file)
        denovo_fasta  = line_for_file + '.fa'
        fsm_out.write(line_for_file + '\t' + denovo_fasta + '\n')

with open(phenotype_file, 'w') as pheno_out:
    for phenotype in phenotypes:
        data         = phenotype.strip().split()
        pheno_prefix = data[0]
        pheno_val    = data[1]

        for item in fsm_list:
            if item.startswith(pheno_prefix):
                pheno_prefix_name = item

        pheno_out.write(pheno_prefix_name + '\t' + str(pheno_val) + '\n')



