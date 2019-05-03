f = open("table11.txt").readlines()
with open("rewriten_table_11.txt", "w") as outfile:
    for line in f[1:]:
        clean_line = line.split('\t')[2:]
        isocode = clean_line[1].split('-')
        print(isocode)
        changed_code = isocode[-2] + '_' + isocode[-1]
        clean_line[1] = changed_code

        string = str(clean_line[0]) + '\t' + str(clean_line[1]) + '\n'
        outfile.write(string)
        print(clean_line)
 

