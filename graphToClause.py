# from sympy import *
# import argparse

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
    clause2, numVar = to_cnf(clause2, numVar)

    writeSatInput(filename, clause, numVar)

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
    
    return ( outl, free_var_num + len(dnf_clauses))


def get_out(sat_out_file, num_vars):
    with open(sat_out_file,"r") as sat_out:
    issat = sat_out.readline()
    if issat != "SAT":
        print("Invalid output")
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
        
def writeSatInput(fileprefix, clause, numVar):
    pass



                


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Taking graph input')
    parser.add_argument('-f', dest='fileprefix', help='The file path', required = True, type=str)
    # parser.add_argument('-o', dest='output', help='Output Prefix', required=True, type=str)
    args = parser.parse_args()

    generate(args.fileprefix)

    # Output in x.satinput and x.satouput 


