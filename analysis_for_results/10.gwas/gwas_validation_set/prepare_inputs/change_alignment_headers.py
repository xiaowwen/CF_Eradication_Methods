import glob
import json

f = open('filtered_val_snp_alignment.fa').readlines()
fsm_names = open('new_fsm_file_list.txt').readlines()
fsm_names = [fsm_name.strip().split()[0] for fsm_name in fsm_names]

align_dict = {}

for j in range(len(f)):
    line = f[j].strip()
    if line.startswith('>pao1'):
        sequence = f[j+1].strip()
        header   = line.split('>pao1')[1]
        #align_dict[header] = sequence
        
        for each_name in fsm_names:
            name_list = each_name.split('_')
            isolate   = name_list[0] + name_list[1]

            if header == isolate:
                isolate_header = '>' + each_name

        align_dict[isolate_header] = sequence

    if line.startswith('>REF'):
        isolate_header = '>REF'
        align_dict[isolate_header] = sequence = f[j+1].strip()

with open('new_filtered_val_snp_alignment.fa', 'w') as outfile:
    for head,seq in align_dict.items():
        outfile.write(head + '\n')
        outfile.write(seq  + '\n')
