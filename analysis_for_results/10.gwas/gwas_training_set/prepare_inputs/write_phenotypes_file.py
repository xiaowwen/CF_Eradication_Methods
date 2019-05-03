import glob

t_list = open('validation_filelist.txt').readlines()
training_list = [training_isolate.strip().split('\t')[0] for training_isolate in t_list]

fsm_list      = []

phenotype_file = 'NEW.pheno'

f = open('validation.pheno').readlines()
isolates = [iso.strip().split()[0] for iso in f]
phenos = [phe.strip().split()[2] for phe in f]

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

