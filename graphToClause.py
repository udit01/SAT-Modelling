from sympy import *
import argparse


# Variable numbering in minsat starts with 1
# i, j is node, sub-graph number
def get1Dindex(i, j, k):
    return (i*k + j + 1)

# Variable numbering in minsat starts with 1
def get2Dindex(idx, k):
    idx = idx - 1
    i = idx // k
    j = idx - i*k
    return i,j

def generate(fileprefix):
    
    # Construct graph from INPUT

    adj = [[]] 
    # adj list representation 0th element is dummy and nodes indexed from 1
    edgelist = []
    # fileprefix = "test"
    with open(fileprefix+".graph","r") as infile:
        first = infile.readline()
        pars = first.split(" ")
        n = int(pars[0])
        edges = int(pars[1])
        K = int(pars[2])

        for i in range(edges):
            adj.append([])
        for i in range(edges):
            line = infile.readline()
            spl = line.split(" ")
            n1 = int(spl[0])
            n2 = int(spl[2])
            edgelist.append([n1,n2])
    #         edgelist.append([n2,n1])
            adj[n1].append(n2)
            adj[n2].append(n1)
    
    # A clause is a list of (list of tuples)
    # Tuples of (Bool, number) where 
    clause1 = [] 
    
    # variableMatrix[n][K] represents whether node n is present in k'th graph
    # variableMatrix = [[False for i in range(n)] for j in range(K)]

    for i in range(n):
        l = []

        for j in range(K):
            l.append((True, get1Dindex(i,j,K)))
        
        clause1.append(l)
    
    clause2 = []

    for i in range(n):
        for j in range(n):
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Taking graph input')
    parser.add_argument('-f', dest='fileprefix', help='The file path', required = True, type=str)
    # parser.add_argument('-o', dest='output', help='Output Prefix', required=True, type=str)
    args = parser.parse_args()

    generate(args.fileprefix)

    # Output in x.satinput and x.satouput 


