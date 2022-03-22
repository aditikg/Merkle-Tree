import hashlib,sys
    
class MerkleTree:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashedV = hashlib.sha256(value.encode('utf-8')).hexdigest()
    
def buildingTree(leaf,fl):
    nodes = []
    for i in leaf:
        nodes.append(MerkleTree(i))

    while len(nodes)!=1:
        ran = []    #Temprory Variable (random)
        for i in range(0,len(nodes),2):
            node1 = nodes[i]
            if i+1 < len(nodes):
                node2 = nodes[i+1]
            else:
                ran.append(nodes[i])
                break
            fl.write("Left child : "+ node1.value + " -> Hashed Value: " + node1.hashedV +" \n")
            fl.write("Right child : "+ node2.value + " -> Hashed Value: " + node2.hashedV +" \n")
            CHash = node1.hashedV + node2.hashedV     # Concatenated Hash
            parent = MerkleTree(CHash)
            parent.left = node1
            parent.right = node2
            fl.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " -> Hashed Value : " + parent.hashedV +" \n")
            ran.append(parent)
        nodes = ran 
    return nodes[0]

inpS = sys.argv[1]
leafString = inpS[1:len(inpS)-1]
leaf = leafString.split(",")
fl = open("merkle.tree", "w")
root = buildingTree(leaf,fl)
fl.close()