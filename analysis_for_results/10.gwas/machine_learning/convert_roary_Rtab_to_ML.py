import numpy as np
import pandas as pd

input_genes = pd.read_csv(filepath_or_buffer='gene_presence_absence.training.Rtab', sep='\t', header=0, index_col=0)
genes       = input_genes.transpose()
phenotypes  = pd.read_csv(filepath_or_buffer='resistances.pheno', sep='\t', header=0, index_col=0)

print(phenotypes)
print(genes)

isolates    = genes.index
gene_names  = genes.columns

# Get and drop identical columns:
def get_identical_columns(column_vector):
    key_set = set(column_vector)
    if len(key_set) == 1:
        outcome = 'drop'
    else:
        outcome = 'keep'
    return outcome

genes_drop_or_not = genes.apply(get_identical_columns, axis=0)

to_drop_identical_cols = []
for i, j in genes_drop_or_not.iteritems():
    if j == 'drop':
        to_drop_identical_cols.append(i)

genes.drop(to_drop_identical_cols, axis=1, inplace=True)
print("Number of identical columns to remove: ", len(to_drop_identical_cols))
print("Number of identically distributed variants to remove: ", len(to_drop_identical_cols)/2)
print("Genes df shape: ", genes.shape)

merged_df = genes.merge(phenotypes, left_index=True, right_index=True)

print(merged_df)

merged_df.to_csv(path_or_buf="ml_train_input.csv", index=False, header=False, sep='\t')
merged_df.to_csv(path_or_buf="ml_train_input.txt", index=True, header=True, sep='\t')


