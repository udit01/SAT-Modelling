# from sympy import *
# import argparse
import sys


# Variable numbering in minsat starts with 1
# i, j is node, sub-graph number
def get1Dindex(i, j, k):
    return (i*k + j + 1)

# Variable numbering in minsat starts with 1
def get2Dindex(idx, k):
    # can treat it as var starting from 0
    # idx = idx - 1
    i = idx // k
    j = idx - i*k
    return i,j

def getInput(fileprefix):

    # Construct graph from INPUT
    edgelist = []
    # fileprefix = "test"
    with open(fileprefix+".graph","r") as infile:
        first = infile.readline()
        pars = first.split(" ")
        n = int(pars[0])
        edgeMatrix = [[False for x in range(n)] for y in range(n)] 
        edges = int(pars[1])
        K = int(pars[2])

        for i in range(edges):
            line = infile.readline()
            spl = line.split(" ")
            n1 = int(spl[0])
            n2 = int(spl[2])
            edgelist.append([n1,n2])

            edgeMatrix[n1][n2] = True
            edgeMatrix[n2][n1] = True

    return edgelist, edgeMatrix, n, K, edges


def generate(fileprefix):

    edgeList, edgeMatrix, n, K, edges = getInput(fileprefix)
    # A clause is a list of (list of tuples)
    # Tuples of (Bool, number) where 
    clause1 = [] 
    
    # variableMatrix[n][K] represents whether node n is present in k'th graph
    # variableMatrix = [[False for i in range(n)] for j in range(K)]

    for i in range(n):
        l = []
        for j in range(K):
            l.append((True, get1Dindex(i,j,K)))
        # element wise append 
        clause1.append(l)
    
    
    # DNF TYPE , or of 2 and's (x1^x2) V (x3^x4) V ...
    clause2 = []

    for i in range(n):
        if j in range(n):
            if i == j:
                continue
            if (edgeMatrix[i][j]):
                l = []
                for t in range(K):
                    l.append( [(True, get1Dindex(i, t, K)), [True, get1Dindex(j, t, K)]] )
                clause2 = clause2 + l

    # numVar is the index of next free variable
    numVar = n*K + 1
    clause2, numVar = to_cnf(clause2, numVar)


    clause3 = []
    # i and j are nodes and t is subgraph
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if(not edgeMatrix[i][j]):
                l = []
                for t in range(K):
                    l.append([(False, get1Dindex(i, t, K)), (False, get1Dindex(j, t, K) )])
                # concat l with clause3
                clause3 = clause3 + l
    

    # DNF TYPE , or of 2 and's (x1^x2) V (x3^x4) V ...
    clause4 = []

    # i and j are subgraphs
    for i in range(K):
        for j in range(K):
            if i == j:
                continue
            l = []
            for node in range(n):
                l.append([(True, get1Dindex(node, i, K)), (False, get1Dindex(node, j, K))])
            # concat l with clause4
            clause4 = clause4 + l


    # numVar is the index of next free variable
    clause4, numVar = to_cnf(clause4, numVar)
    clause = clause1 + clause2 + clause3 + clause4
    writeSatInput(fileprefix, clause, numVar-1)

def writeSatInput(fileprefix, clause, numVar):
    # 1 to numVar all are varialbes
    with open(fileprefix+".satinput","w") as outfile:
        
        string1 = "p cnf %d %d\n" %(numVar, len(clause))
        outfile.write(string1, end="")

        for exp in clause:
            st = ""
            for term in exp:
                if (not term[0]):
                    st += "-" 
                st += str(term[1]) + " "
            
            st += "0\n"
            outfile.write(st, end="")

        outfile.close()


def to_cnf(dnf_clause, free_var_num):
    outl = []
    num_ands = len(dnf_clause)
    tmpl = []
    for i in range(num_ands):
        tmpl.append((True, free_var_num+i))
    outl.append(tmpl)

    for i in len(dnf_clause):
        for var in dnf_clause[i]:
            outl.append([(False, free_var_num + i),var])
    
    return ( outl, free_var_num + len(dnf_clause))


def get_out(fileprefix, num_vars):
    with open(fileprefix+".satoutput","r") as sat_out:
        issat = sat_out.readline()
        if issat != "SAT":
            print("0")
            exit(-1)
        sol  = sat_out.read_line()
        assign = sol.split(" ")
        assign = assign[:-1] # check that this removes 0 only
        assignments = []
        for i in range(num_vars):
            if assign[i][0]=="-":
                assignments.append(False)
            else:
                assignments.append(True)   
    
    return assignments
        

def out(fileprefix):

    edgeList, edgeMatrix, n, K, edges = getInput(fileprefix)
    assignments = get_out(fileprefix, n*K)

    variableMatrix = [[False for i in range(K)] for j in range(n)]

    for t in range(len(assignments)):
        i, j = get2Dindex(t, K)
        variableMatrix[i][j] = assignments[t]

    for t in range(K):
        count = 0
        for i in range(n):
            if(variableMatrix[i][t]):
                count+=1
        print("#%d %d\n"%(t+1, count), end="")
        for i in range(n):
            if(variableMatrix[i][t]):
                count -= 1
                print(i, end="")
                if(count > 0):
                    print(" ", end="")
        print()


if __name__ == "__main__":


    # parser = argparse.ArgumentParser(description='Taking graph input')
    # parser.add_argument('-f', dest='fileprefix', help='The file path', required = True, type=str)
    # parser.add_argument('-o', dest='output', help='Output Prefix', required=True, type=str)
    # args = parser.parse_args()

    fileprefix = sys.argv[1]
    mode = int(sys.argv[2])
    
    if mode == 0:
        generate(fileprefix)
    else:
        out(fileprefix)
    
    # Output in x.satinput and x.satouput 


