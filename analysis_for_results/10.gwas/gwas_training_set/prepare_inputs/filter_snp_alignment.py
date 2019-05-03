from sys import argv
import pandas

# Originally written by Conrad, used here with some adaptations

script, fasta, positions_file, output_fasta, output_positions = argv

# Create dictionary of fasta sequences, with header as key and sequence as value:
infile_dict = {}
with open(fasta, 'r') as infile1:
    for line in infile1:
        if line.startswith(">"):
            infile_dict[line.strip()] = list(next(infile1).strip())

# Create list of high quality positions:
positions_list = []

with open(positions_file, 'r') as infile2:
    for line in infile2:
        positions_list.append(line.strip().split('-')[1])

outnames = pandas.Series(positions_list)

reference = infile_dict[">REF"]

# Convert reference list into a series and label positions with high quality positions list:
ref_series = pandas.Series(reference, index=positions_list)
ref_df     = pandas.DataFrame(reference, index=positions_list, columns = ['REF'])

# Delete reference sequence from infile_dict:
del infile_dict[">REF"]

# Turn sequence dictionary into dataframe, with positions as the column names:
df1 = pandas.DataFrame.from_dict(infile_dict, orient='index')
df1.columns = positions_list

print("Original number of df columns: ", len(df1.columns))

# 1. Get and drop columns with N:
#####################################################################################

def get_n_columns(column_vector):
    key_set = set(column_vector)
    if 'N' in key_set:
        outcome = "drop"
    else:
        outcome = "keep"
    return outcome

# Drop columns and pass to a copy(out1) of original dataframe to help with
# getting list of dropped columns below
out1 = df1.apply(get_n_columns, axis=0)
out1.rename(index=outnames, inplace=True)

# Get the list of columns and THEN actually apply the regular Pandas drop() function
# to drop them in the original dataframe. This is done for other dropping functions
# as well so as to have just one copy of the original dataframe.
to_drop_N_colnames = []
for i, j in out1.iteritems():
    if j == 'drop':
        to_drop_N_colnames.append(i)

df1.drop(to_drop_N_colnames, axis=1, inplace=True)
print("New df length after removing columns with N: ", len(df1.columns))

# Update the positions as well by only including those that are not in the 
# to_drop_N_colnames from above. 
positions_list2 = [i for i in positions_list if i not in to_drop_N_colnames]
outnames2 = pandas.Series(positions_list2)

# 2. Get and drop identical columns:
#####################################################################################

def get_identical_columns(column_vector):
    key_set = set(column_vector)
    if len(key_set) == 1:
        outcome = 'drop'
    else:
        outcome = 'keep'
    return outcome

out2 = df1.apply(get_identical_columns, axis=0)
out2.rename(index=outnames2, inplace=True)

to_drop_identical_cols = []
for i, j in out2.iteritems():
    if j == 'drop':
        to_drop_identical_cols.append(i)

df1.drop(to_drop_identical_cols, axis=1, inplace=True)
print("New df length after removing identical columns: ", len(df1.columns))

positions_list3 = [i for i in positions_list2 if i not in to_drop_identical_cols]
outnames3 = pandas.Series(positions_list3)

# 3. Get and drop multiallelic columns:
#####################################################################################

def get_multiallelic_columns(column_vector):
    key_set = set(column_vector)
    if len(key_set) > 2:
        outcome = 'drop'
    else:
        outcome = 'keep'
    return outcome

out3 = df1.apply(get_multiallelic_columns, axis=0)
out3.rename(index=outnames3, inplace=True)

to_drop_multiallelics = []
for i,j in out3.iteritems():
    if j == 'drop':
        to_drop_multiallelics.append(i)

df1.drop(to_drop_multiallelics, axis=1, inplace=True)
print("New df length after removing multiallelic columns: ", len(df1.columns))

positions_list4 = [i for i in positions_list3 if i not in to_drop_multiallelics]
outnames4 = pandas.Series(positions_list4)

# 4. Get and drop singleton columns:
#####################################################################################

def get_singleton_columns(column_vector):
    key_set = set(column_vector)
    if len(key_set) == 2:
        counts = list(column_vector.value_counts())
        if 1 in counts:
            outcome = "drop"
        else:
            outcome = "keep"
    else:
        print("Something isn't right")
    return outcome

out4 = df1.apply(get_singleton_columns, axis=0)
out4.rename(index=outnames4, inplace=True)

to_drop_singletons = []
for i, j in out4.iteritems():
    if j == 'drop':
        to_drop_singletons.append(i)

df1.drop(to_drop_singletons, axis=1, inplace=True)
print("New df length after removing singletons: ", len(df1.columns))
positions_list5 = [i for i in positions_list4 if i not in to_drop_singletons]
outnames5 = pandas.Series(positions_list5)

# 5. Remove allese with MAF < 0.05
#####################################################################################

def get_low_maf_columns(column_vector):
    threshold = 0.05
    key_set = set(column_vector)
    value_counts = list(column_vector.value_counts())
    sum_counts = float(sum(value_counts))
    value_freqs = [float(i)/sum_counts for i in value_counts]
    if all(value_freq > threshold for value_freq in value_freqs) == True:
        outcome = "keep"
    elif all(value_freq > threshold for value_freq in value_freqs) == False:
       outcome = "drop"
    return outcome

out5 = df1.apply(get_low_maf_columns, axis=0)
out5.rename(index=outnames5, inplace=True)

to_drop_low_maf = []
for i, j in out5.iteritems():
    if j == 'drop':
        to_drop_low_maf.append(i)

df1.drop(to_drop_low_maf, axis=1, inplace=True)
print("New df length after removing low MAF alleles: ", len(df1.columns))

#df1.to_csv(path_or_buf="/home/enaziga/work/reproduce_analysis/10.pyseer_analysis/snps_analysis/biallelic_snps_matrix.txt", sep='\t')

positions_list6 = [i for i in positions_list5 if i not in to_drop_low_maf]
outnames6 = pandas.Series(positions_list6)

# 6. Remove uniquely segregating variants
#####################################################################################

def get_unique_seg(variants_df):
    print(variants_df)
    inputcol = list(variants_df.columns)
    colstring_dict = {}
    colstring_set = set()
    for i in inputcol:
        # print type(i)
        col = list(variants_df[i])
        colstring = ''.join(col)
        if colstring not in colstring_set:
            colstring_set.add(colstring)
            colstring_dict[colstring] = [i]
        else:
            colstring_dict[colstring].append(i)

    #print(colstring_dict)
    print("Number of uniquely segregating variants: ", len(colstring_dict))
    to_drop = []
    for key in colstring_dict:
        key_value = colstring_dict[key]
        if len(key_value) > 1:
            key_value_minus_first = key_value[1:]
            for i in key_value_minus_first:
                to_drop.append(i)
        else:
            pass

    print("Number of identically-segregating variants to remove: ", len(to_drop))
    return to_drop

to_drop_seg_sites = get_unique_seg(df1)

df1.drop(to_drop_seg_sites, axis=1, inplace=True)
print("New df length after removing identically segregating sites: ", len(df1.columns))

positions_list7 = [i for i in positions_list6 if i not in to_drop_seg_sites]
outnames7 = pandas.Series(positions_list7)

# Get reference sequence where all dropped columns above has been removed and write that to a file

string_pos = [str(pos7) for pos7 in positions_list7]
ref_with_dropped_columns = ref_df.loc[string_pos]
ref_seq_with_dropped_cols = ref_with_dropped_columns['REF'].values.tolist()
with open('reference_filtered.fa', 'w') as outfile:
    ref_string2 = ''
    for each_REF in ref_seq_with_dropped_cols:
        ref_string2 += each_REF
    outfile.write('>REF \n')
    outfile.write(ref_string2 + '\n')

# Convert dataframe and reference sequence (a series) to a dictionary and list, respectively (for easier writing to file):
df1_dict = df1.transpose().to_dict(orient='list')

# Write isolate sequences to file:
with open(output_fasta, 'w') as outfile:
    for key in df1_dict:
        outfile.write(key + '\n' + ''.join(df1_dict[key]) + '\n')
    ref_string3 = ''
    for each_REF in ref_seq_with_dropped_cols:
        ref_string3 += each_REF
    outfile.write('>REF \n')
    outfile.write(ref_string3 + '\n')

# Write positions to new list:
with open(output_positions, 'w') as outfile2:
    for position in positions_list7:
        outfile2.write(str(position) + '\n')

