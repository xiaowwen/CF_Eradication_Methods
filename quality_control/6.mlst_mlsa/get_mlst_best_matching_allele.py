import os
import glob
from pathlib import Path
import pandas as pd
from sys import argv
import seaborn as sns
from pprint import pprint

script, mlst_top_folder, mlst_profiles_csv, isolate_background_data = argv

# List of output files from the blastn database search for each loci

loci = ['acsA.out', 'aroE.out', 'guaA.out', 'mutL.out', 'nuoD.out', 'ppsA.out', 'trpE.out']

# Read database if sequence types, circle though each datapoint in mlst_dict and get ST
# ST database can be downloaded via: wget http://rest.pubmlst.org/db/pubmlst_paeruginosa_seqdef/schemes/1/profiles_csv

STs = pd.read_csv(mlst_profiles_csv, delimiter='\t', index_col=None)

# Denovo assembled contigs after alignment to good contigs
blastn_dbs = os.getcwd()  + '/' + mlst_top_folder  + '/' + '*/*.nsq'
files = glob.glob(blastn_dbs)
prefixes = [ line.split('/')[-1].split('.')[0] for line in files]
unique_prefix_seqs = list(set(prefixes))

mlst_dict = {}
ST_dict   = {}
novel_ST_counts = int(1)
novel_ST_dict = {}

for unique_prefix_seq in unique_prefix_seqs:

    list_of_best_fit_alleles = []

    for locus in loci:

        locus_file = mlst_top_folder + '/' + unique_prefix_seq + '/' + locus
        locus_lines = open(locus_file).readlines()

        allele_indices = [i for i, allele in enumerate(locus_lines) if allele.startswith('Query=')]
        
        data_for_this_locus = {}

        for j in range(len(allele_indices)-1):

            # The data we need is largely contained in the 'Identities= ...' line
            locus_slice = locus_lines[allele_indices[j]:allele_indices[j+1]]
            allele_name = locus_slice[0].strip().split()[1]
            locus_slice_idx = [i for i, allele in enumerate(locus_slice) if allele.strip().startswith('Identities')]

            # Sometimes no hits are found
            if len(locus_slice_idx) > 0:
                data  = locus_slice[locus_slice_idx[0]]
                gaps = data.strip().split('Gaps')[1].split()[1].split('/')[0]
                HSP_L_allele_L = data.strip().split('Gaps')[0].split()[2]
                hsp_l,allele_l = HSP_L_allele_L.split('/')
                perc_identity = 100.0*(float(hsp_l)/float(allele_l))
                data_for_this_locus[(allele_name, HSP_L_allele_L, gaps)] = perc_identity

            else:
                # What happens when there are no hits??
                data_for_this_locus[(allele_name, 0, 0)] = 0

        # Get the best match for all hits for a particular locus. If no hits were found, add a placeholder record.
        if len(data_for_this_locus.values()) > 0:
            max_perc_identity = max(data_for_this_locus.values())
            info_ = list(data_for_this_locus.keys())[list(data_for_this_locus.values()).index(max_perc_identity)]
            list_of_best_fit_alleles.append([info_[0], info_[1], info_[2] ,max_perc_identity])
        else:
            info_ = (allele_name, '0/N', 'N')
            list_of_best_fit_alleles.append([info_[0], info_[1], info_[2] ,0])


    # Add the best hit data to the dictionary and extract the allele values 
    unique_prefix_seq = unique_prefix_seq.split('_')[0]

    mlst_dict[unique_prefix_seq] = list_of_best_fit_alleles

    acs = int(list_of_best_fit_alleles[0][0].split('_')[1])
    aro = int(list_of_best_fit_alleles[1][0].split('_')[1])
    gua = int(list_of_best_fit_alleles[2][0].split('_')[1])
    mut = int(list_of_best_fit_alleles[3][0].split('_')[1])
    nuo = int(list_of_best_fit_alleles[4][0].split('_')[1])
    pps = int(list_of_best_fit_alleles[5][0].split('_')[1])
    trp = int(list_of_best_fit_alleles[6][0].split('_')[1])

    # Check against the ST database to assign sequence types
    expression = "acsA==%s & aroE==%s &  guaA==%s & mutL==%s & nuoD==%s & ppsA==%s & trpE==%s" % (acs,aro,gua,mut,nuo,pps,trp)
    ST_df = STs.query(expression)

    if len(ST_df) == 1:
        sequence_type = ST_df['ST'].values[0]
        ST_dict[unique_prefix_seq]  = [sequence_type, acs, aro, gua, mut, nuo, pps, trp]
    else:
        if len(novel_ST_dict) == 0:
            ST_dict[unique_prefix_seq]  = ['Novel_1', acs, aro, gua, mut, nuo, pps, trp]
            novel_ST_name = 'Novel_1'
            novel_ST_dict[(acs, aro, gua, mut, nuo, pps, trp)] = novel_ST_name

        else:
            if (acs, aro, gua, mut, nuo, pps, trp) in novel_ST_dict.keys():
                prev_found_novel_ST =  novel_ST_dict[(acs, aro, gua, mut, nuo, pps, trp)] 
                ST_dict[unique_prefix_seq]  = [prev_found_novel_ST, acs, aro, gua, mut, nuo, pps, trp]

            else:
                novel_ST_counts = novel_ST_counts + 1
                new_nodel_ST_name = 'Novel_' + str(novel_ST_counts)
                ST_dict[unique_prefix_seq]  = [new_nodel_ST_name, acs, aro, gua, mut, nuo, pps, trp]
                novel_ST_dict[(acs, aro, gua, mut, nuo, pps, trp)] = new_nodel_ST_name

ST_dict_df = pd.DataFrame.from_dict(ST_dict, orient='index', columns=['ST', 'acsA', 'aroE', 'guaA', 'mutL', 'nuoD', 'ppsA', 'trpE'])
isolate_info_df = pd.read_csv(filepath_or_buffer=isolate_background_data, sep='\t', header=0, index_col=1)
isolate_info_df.index = isolate_info_df.index.map(str)

isolate_ID = [isolate_id.split('_')[0] for isolate_id in ST_dict_df.index.values]
isolates_df = pd.DataFrame(isolate_ID, columns=['isolate'], index=ST_dict_df.index)
ST_dict_df_isolate = isolates_df.merge(ST_dict_df, left_index=True, right_index=True)

number_of_STs = ST_dict_df.ST.value_counts()
ST_types = list(set(ST_dict_df_isolate['ST'].values))

ST_isolates = {}
for ST_type in ST_types:

    ST_type_by_isolate = ST_dict_df_isolate.loc[ST_dict_df_isolate['ST'] == ST_type]
    isolates_per_ST = ST_type_by_isolate['isolate'].values 

# Merge in other isolate information e.g. patient_num, infection_num

full_isolate_info_df = ST_dict_df_isolate.merge(isolate_info_df, left_index=True, right_index=True) 

# Write file for PHYLOViZ analysis using geoBURST algorithm

PHYLOViZ_data = full_isolate_info_df[['ST', 'acsA', 'aroE', 'guaA', 'mutL', 'nuoD', 'ppsA', 'trpE']]
aux_data_for_colors = full_isolate_info_df[['isolate','eradication_status']]
PHYLOViZ_data.to_csv(path_or_buf='PHYLOViZ_data.csv', sep='\t', index=True, header=True)

# Write iTOL supplimentary data  files

ST_colors = {}
STs = list(set(PHYLOViZ_data.ST.values))
palette = sns.color_palette('colorblind', len(STs)).as_hex()

for j in range(len(STs)):
    ST_colors[ STs[j] ] = palette[j]

ST_colors_by_Isolate = {}

for isol_ID in PHYLOViZ_data.index:
    strain = PHYLOViZ_data.loc[isol_ID, 'ST']
    ST_colors_by_Isolate[isol_ID] = ST_colors[strain]      

#print(ST_colors)
pprint(ST_colors_by_Isolate)

print(len(ST_colors_by_Isolate.keys()))


