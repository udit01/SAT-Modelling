# from sympy import *
# import argparse
import sys


# Variable numbering in minsat starts with 1
# i, j is node, sub-graph number
def get1Dindex(i, j, k):
    return (i*k + j)

# Variable numbering in minsat starts with 1
def get2Dindex(idx, k):
    # can treat it as var starting from 0
    # idx = idx - 1
    i = idx // k
    j = idx - i*k
    return i,j

def getInput(fileprefix, mode=0):

    # Construct graph from INPUT
    edgelist = []
    # fileprefix = "test"
    with open(fileprefix+".graph","r") as infile:
        first = infile.readline()
        pars = first.split(" ")
        n = int(pars[0])
        edges = int(pars[1])
        K = int(pars[2])
        
        if (mode == 1):
            return n, K
        
        edgeMatrix = [[False for x in range(n)] for y in range(n)] 

        for i in range(edges):
            line = infile.readline()
            spl = line.split(" ")
            n1 = int(spl[0])
            n2 = int(spl[1])
            n1 -= 1
            n2 -= 1
            edgelist.append([n1,n2])

            # print(n1, n2)
            edgeMatrix[n1][n2] = True
            edgeMatrix[n2][n1] = True

    return edgelist, edgeMatrix, n, K, edges


def generate(fileprefix):

    edgeList, edgeMatrix, n, K, edges = getInput(fileprefix)
    # A clause is a list of (list of tuples)
    # Tuples of (Bool, number) where 
    numVar = n*K + 1
    
    
    clause1 = [] 
    
    # variableMatrix[n][K] represents whether node n is present in k'th graph
    # variableMatrix = [[False for i in range(n)] for j in range(K)]


    for i in range(n):
        l = []
        for j in range(K):
            l.append((True, get1Dindex(i,j,K)))
        # element wise append 
        clause1.append(l)
    
    # print("Printing clause1 ------- " , clause1)
    
    # # DNF TYPE , or of 2 and's (x1^x2) V (x3^x4) V ...
    # clause2 = []
    # # AN EDGE MUST 
    # # print("EDGE MATRIX", edgeMatrix)
    # for i in range(n):
    #     for j in range(i+1, n):
    #         if (edgeMatrix[i][j]):
    #             l = []
    #             for t in range(K):
    #                 l.append( [(True, get1Dindex(i, t, K)), (True, get1Dindex(j, t, K))] )
    #             clause2.extend(l)

    # # numVar is the index of next free variable
    # # print('Printing edge matrix', edgeMatrix)
    # # print("Printing clause 2  ------- " , clause2)
    # clause2, numVar = to_cnf(clause2, numVar)
    # # print("Printing clause 2 ---- " , clause2)


    clause3 = []
    # i and j are nodes and t is subgraph
    for i in range(n):
        for j in range(i+1,n):
            l = []
            if(not edgeMatrix[i][j]):
                for t in range(K):
                    l.append([(False, get1Dindex(i, t, K)), (False, get1Dindex(j, t, K) )])
            # concat l with clause3
            clause3.extend(l)
    

    # print("Printing clause3 ------- " , clause3)
    # DNF TYPE , or of 2 and's (x1^x2) V (x3^x4) V ...
    clause4 = []
    # NO SUBGRAPH IS SUBGRAPH OF ANOTHER
    # i and j are subgraphs
    for i in range(K):
        for j in range(K):
            if i == j:
                continue
            l = []
            for node in range(n):
                # print("PRINTING SG1, SG2, NODE ", i, j, node)
                l.append([(True, get1Dindex(node, i, K)), (False, get1Dindex(node, j, K))])
            # concat l with clause4
            l, numVar = to_cnf(l, numVar)
            clause4.extend(l)

    # print("Printing clause4 ------ " , clause4)

    # numVar is the index of next free variable
    # clause4, numVar = to_cnf(clause4, numVar)
    # print("Printing clause4 ------ " , clause4)


    # Clause 5, we thought it was included in previous constraints ?
    clause5 = []
    # ALL EDGES MUST BE INCLUDED
    for i in range(n):
        for j in range(i+1,n):
            l = []
            if(edgeMatrix[i][j]):
                # print("PRINTING i, j in clause 5 --- ", i, j)
                for t in range(K):
                    # OR of pairwise and
                    l.append( [(True, get1Dindex(i, t, K)), (True, get1Dindex(j, t, K))] )
                l, numVar = to_cnf(l,numVar)
            clause5.extend(l)

    
    clause6 = []
    # NO SUBGRAPH IS EMPTY
    for i in range(K):
        l = []
        for j in range(n):
            l.append((True, get1Dindex(j, i, K)))
        clause6.append(l)
    # print("Printing clause 5 ----- ", clause5)

    # clause = clause1 + clause2 + clause3 + clause4 + clause5 + clause6
    clause = clause1 + clause3 + clause4 + clause5 + clause6
    
    # print("Num Var ---- ",numVar)

    writeSatInput(fileprefix, clause, numVar)

def writeSatInput(fileprefix, clause, numVar):
    # 1 to numVar all are varialbes
    writeString = ""
    string1 = "p cnf %d %d\n" %(numVar, len(clause))
    # outfile.write(string1)
    writeString += string1
    for exp in clause:
        st = ""
        for term in exp:
            if (not term[0]):
                st += "-" 
            # To make the variables 1 indexed
            st += str(term[1]+1) + " "
        st += "0\n"
        writeString += st
        # outfile.write(st)
    with open(fileprefix+".satinput","w") as outfile:
        outfile.write(writeString)
        outfile.close()


def to_cnf(dnf_clause, free_var_num):

    if (dnf_clause == []):
        return [], free_var_num

    outl = []
    num_ands = len(dnf_clause)
    tmpl = []
    for i in range(num_ands):
        tmpl.append((True, free_var_num+i))
    outl.append(tmpl)

    
    for i in range(num_ands):
        for var in dnf_clause[i]:
            outl.append([(False, free_var_num + i),var])
    
    return outl, (free_var_num + num_ands)


def get_out(fileprefix, num_vars):
    with open(fileprefix+".satoutput","r") as sat_out:
        issat = sat_out.readline()
        if issat != "SAT\n":
            print("0")
            exit(-1)
        sol  = sat_out.readline()
        assign = sol.split(" ")
        assign = assign[:-1] # check that this removes 0 only
        assignments = []
        for i in range(num_vars):
            if assign[i][0]=="-":
                assignments.append(False)
            else:
                assignments.append(True)   
    
    return assignments
        


# UDIT: I have tested this function (for sample case),
# this is running as expected [assignments, i&j order etc]  
def out(fileprefix):
    
    n, K = getInput(fileprefix, mode=1)
    
    # print(edgeList, n, K)

    assignments = get_out(fileprefix, n*K)
    # print("Assignments are ----",assignments)
    variableMatrix = [[False for i in range(K)] for j in range(n)]
    for t in range(len(assignments)):
        i, j = get2Dindex(t, K)
        variableMatrix[i][j] = assignments[t]

    # print("Variable matrix is ---",variableMatrix)
    
    writeString = ""

    for t in range(K):
        count = 0
        for i in range(n):
            if(variableMatrix[i][t]):
                count+=1
        # print("#%d %d\n"%(t+1, count), end="")
        writeString += "#%d %d\n" % (t+1, count)
        for i in range(n):
            if(variableMatrix[i][t]):
                count -= 1
                writeString += str(i+1) 
                # print(i+1, end="")
                if(count > 0):
                    # print(" ", end="")
                    writeString += " "
        writeString += "\n"
    
    with open(fileprefix+".subgraphs","w") as outfile:
        outfile.write(writeString)
        outfile.close()
    


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


