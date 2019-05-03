import glob

def isolate_folders(seq_fpath):
    # Grab sequence files
    try:
        files = glob.glob(seq_fpath+"/*P.fq.gz")
        if len(files) > 0:
            success = True
    except:
        pass

    if len(files) == 0:
        try:
            files = glob.glob(seq_fpath+"/*.fq.gz")
        except:
            files = glob.glob(seq_fpath+"/*.fq")
    files.sort()

    # Get file prefixes
    prefixes = []
    for fastq in files:
        fname = fastq.split('/')[-1]
        if fname.endswith('P.fq.gz'):
            prefix = fname[:-9]
        elif fname.endswith('_1.fq.gz') or fname.endswith('_2.fq.gz'):
            prefix = fname[:-8]
        elif fname.endswith('fq'):
            prefix = fname[:-3]
        else:
            print('Sequence files must be paired end reads with either [.fq.gz] or [.fq] suffixes')
        prefixes.append(prefix)
    unique_prefix_seqs = list(set(prefixes))
    return unique_prefix_seqs

