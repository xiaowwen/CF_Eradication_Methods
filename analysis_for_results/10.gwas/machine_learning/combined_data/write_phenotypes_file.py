import glob

t_list = open('combined_fsm_file_list.txt').readlines()
training_list = [training_isolate.strip().split('\t')[0] for training_isolate in t_list]
print(training_list)

fsm_list      = []

phenotype_file = 'new_combined_resistances.pheno'

f = open('total_phenotype_input.csv').readlines()
isolates = [iso.strip().split()[0] for iso in f]
phenos = [phe.strip().split()[1] for phe in f]
print(phenos)

with open(phenotype_file, 'w') as pheno_out:

    for isolate,pheno in zip(isolates,phenos):
        
        for item in training_list:
            item_prefix = item.split('_')[0]
            if isolate == item_prefix:
                pheno_prefix_name = item
                pheno_val = pheno

        pheno_out.write(pheno_prefix_name + '\t' + str(pheno_val) + '\n')


fsm_file_name = 'new_fsm_file_list.txt'
with open(fsm_file_name, 'w') as fsm_list_out:

    for isolate in isolates:
        for item in training_list:
            item_prefix = item.split('_')[0]
            if isolate == item_prefix:
                contig_prefix_name = item
                contig_name        = item + '.fa'

        fsm_list_out.write(contig_prefix_name + '\t' + contig_name + '\n')

    

