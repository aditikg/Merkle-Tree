import sys
def parseFile():
    fl = open("merkle.tree","r")
    treeA ={}
    for line in fl:
        lineArray = line.split(" ")
        if lineArray[0] == 'Parent(concatenation':
            treeA[lineArray[6]] = lineArray[10]
        else:
            treeA[lineArray[3]] = lineArray[7]
    return treeA

def checkInclusion(inpS,treeA):
    res = []
    for key,value in treeA.items():
        if inpS in key:
            res.append(value)
            inpS = value
    return res

inpS = sys.argv[1]
treeA = parseFile()
res = checkInclusion(inpS,treeA)
if(len(res)> 0):
    print("yes",res)
else:
    print("no")