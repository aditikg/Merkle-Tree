import hashlib
import sys

class MerkleTree:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = getHashValue(value)
    
def MerkleTreeBuild(leafNodes,fl):
    nodes = []
    for i in leafNodes:
        nodes.append(MerkleTree(i))

    while len(nodes)!=1:
        randomV = []
        for i in range(0,len(nodes),2):
            node1 = nodes[i]
            if i+1 < len(nodes):
                node2 = nodes[i+1]
            else:
                randomV.append(nodes[i])
                break
            fl.write("\nLeft node: "+ node1.value + " | Hash : " + node1.hashValue +" \n")
            fl.write("\nRight child: "+ node2.value + " | Hash : " + node2.hashValue +" \n")
            concatenatedHashval = node1.hashValue + node2.hashValue
            parent = MerkleTree(concatenatedHashval)
            parent.left = node1
            parent.right = node2
            fl.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " | Hash : " + parent.hashValue +" \n")
            randomV.append(parent)
        nodes = randomV 
    return nodes[0]

def getHashValue(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def combining(value1,value2):
    combinedValue = value1+value2
    return combinedValue


def checkConsistency(leaves1,leaves2):
    i=0
    while i < len(leaves1):
        if leaves1[i]!=leaves2[i]:
            break
        i+=1
    if i < len(leaves1):
        return []
    fl = open("merkle.tree", "w")
    fl.write("\nMerkle Tree 1 \n")
    r1 = MerkleTreeBuild(leaves1,fl)
    fl.write("\n\n")
    fl.write("\nMerkle Tree 2 \n")
    r2 = MerkleTreeBuild(leaves2,fl)
    fl.close()
    op = []
    op.append(r1.hashValue)
    with open("merkle.tree") as fl:
        data = fl.readlines()
    
    tree2Index = 0
    for i in range(len(data)):
        if data[i].startswith("\nMerkle Tree 2"):
            tree2Index = i
    parentLines = []
    leftChildLines = []
    rightChildLines = []
    for i in range(tree2Index,len(data)):
        if data[i].startswith("Parent("):
            parentLines.append(data[i])
    
    for i in range(tree2Index,len(data)):
        if data[i].startswith("Left"):
            leftChildLines.append(data[i])

    for i in range(tree2Index,len(data)):
        if data[i].startswith("Right"):
            rightChildLines.append(data[i])  
    op = []
    flag = False
    for i in range(len(parentLines)):
        if r1.hashValue in parentLines[i]:
            flag = True
            break
    if flag:
        values = []    
        combinedHash = ''
        leftc = r1.value
        while combinedHash != r2.hashValue:
            for i in range(len(leftChildLines)):
                if leftc in leftChildLines[i].split(" ")[-6]:
                    rightc = rightChildLines[i].split(" ")[-6]
                    values.append(getHashValue(rightc))
                    break
            combinedValue = combining(getHashValue(leftc),getHashValue(rightc))
            combinedHash = getHashValue(combinedValue)
            leftc = combinedValue
            
        op.append(r1.hashValue)
        op+=values
        op.append(r2.hashValue)
                
    else:
        root1LeftChildValue = data[tree2Index-5].split(" ")[-6]
        root1RightChildValue = data[tree2Index-4].split(" ")[-6]
        root1RightChildSiblingValue = leaves2[leaves2.index(root1RightChildValue)+1]
        values = []
        values.append(getHashValue(root1LeftChildValue))
        values.append(getHashValue(root1RightChildValue))
        values.append(getHashValue(root1RightChildSiblingValue))
        root1RightChildCombinedValue = combining(getHashValue(root1RightChildValue),getHashValue(root1RightChildSiblingValue))        
        combinedHash = ''
        leftc = root1LeftChildValue
        rightc = root1RightChildCombinedValue
        while combinedHash != r2.hashValue:
            combinedValue = combining(getHashValue(leftc),getHashValue(rightc))
            combinedHash = getHashValue(combinedValue)
            leftc = combinedValue
            for i in range(len(leftChildLines)):
                if leftc in leftChildLines[i].split(" ")[-6]:
                    rightc = rightChildLines[i].split(" ")[-6]
                    values.append(getHashValue(rightc))
                    break
            
        op.append(r1.hashValue)
        op+=values
        op.append(r2.hashValue)
                
    return op

inputString1 = sys.argv[1]
inputString2 = sys.argv[2]
leavesString1 = inputString1[1:len(inputString1)-1]
leaves1 = leavesString1.split(",")
leavesString2 = inputString2[1:len(inputString2)-1]
leaves2 = leavesString2.split(",")

op = checkConsistency(leaves1,leaves2)
if len(op) > 0:
    print("yes",op)
else:
    print("no")