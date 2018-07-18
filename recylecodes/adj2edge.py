
unweighted=True
csv = open("./data/usSuprimeADJ.txt")
# columns = csv.readline().strip().split(',')[1:]
columns = [i for i in range(1,10)]
row=0
# print columns
for line in csv:
    #column += 1
    tokens = [ int(x) for x in line.strip().split() ]
    # row = tokens[0]
    row = row + 1
    for column, cell in zip(columns, tokens[0:]):
        if unweighted:
            if column > row and cell != 0:
                if cell > 0:
                   print '{},{},{}'.format(row, column, 1)
                   #print type(cell)
                else:
                    print '{},{},{}'.format(row, column, -1)
                    #print 'bye'
        else:
            if column > row and cell != 0:
                print '{},{},{}'.format(row, column, cell)
