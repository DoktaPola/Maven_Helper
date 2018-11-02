inFile = open('C:\\Users\\Полина\\Desktop\\hi.txt', 'r')
outFile = open('result.txt', 'w')
buffer = []
keepCurrentSet = True
for line in inFile:
    # buffer.append(line)
    if line.startswith("----"):
        # ---- starts a new data set
        if keepCurrentSet:
            outFile.write("".join(buffer))
        # now reset our state
        keepCurrentSet = True
        buffer = []
    elif line.startswith("extractme"):
        keepCurrentSet = False
inFile.close()
outFile.close()
