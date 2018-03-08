from scipy import spatial as sc
from scipy import ndimage
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import numpy as np
from functools import reduce
import sys
# the function for calculating the intermediate result between the  label using correlation distance
def buildIntermediateRelationship(human,parasite,distance='correlation'):
    result=[]
    total = len(human)
    count=0
    for x  in human:
        temp=[]
        yCount=0
        yTotal = len(parasite)
        for y in parasite:
            if distance=='correlation':
                temp.append(sc.distance.correlation(x,y))
            if distance=='euclidean':
                temp.append(sc.distance.euclidean(x,y))
            if distance=='cosine':
                temp.append(sc.distance.cosine(x,y))
        count+=1;
        # if count==50:
        #     break
        print(str(count)+' of '+str(total))
        result.append(temp)
    return normaliseValue(result)


# function to load the computeed value for csv output as intermediate file
def buildCsvFormat(filename,data,humanLabel,parasiteLabel):
    with open(filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        first = [''] + parasiteLabel
        spamwriter.writerow(first)
        counter=0;
        for dt in data:
            temp = [humanLabel[counter]] + dt
            spamwriter.writerow(temp)
            counter+=1

# the function for generate the graph
def extractNodes(parasiteLabel, humanLabel,relationshipMatrix,weights):
    #extract all genes
    node1 =[humanLabel[i] for i in range(len(relationshipMatrix))
        if len(relationshipMatrix[i]) > 0] #make sure the list is not empty befor adding it as human genome node
    tempArr = [];
    for i in range(len(relationshipMatrix)):
        tempArr+=relationshipMatrix[i]
    subParasite= list(set(tempArr))
    subParasite =[parasiteLabel[i] for i in subParasite];
    edges =[(humanLabel[x],parasiteLabel[y],{'weight':weights[x][y]}) for x in range(len(relationshipMatrix)) for y in relationshipMatrix[x]
        if len(relationshipMatrix[x]) > 0]
    return node1,subParasite,edges

def buildGraph(humanNode, parasiteNode,edges):
    graph =nx.Graph();
    graph.add_nodes_from(humanNode,bipartite=0)
    graph.add_nodes_from(parasiteNode,bipartite=1)
    graph.add_edges_from(edges);
    l= set(n for n,d in graph.nodes(data=True) if d['bipartite']==0)
    r = set(graph) - l
    pos = {}
    pos.update((node, (1, index)) for index, node in enumerate(l))
    pos.update((node, (2, index)) for index, node in enumerate(r))
    nx.draw(graph,pos=pos,with_labels=True)
    plt.show()

def getRelationshipMatrix(threshold,intermediate,humanLabel,parasiteLabel):
    # let all the information necessary for estimating the result be added here
    relationshipMatrix=[]
    for i in range(len(intermediate)):
        temp =[]
        for j in range(len(intermediate[i])):
            if intermediate[i][j] < threshold:
                # append a dictionary here to better perform the estimation
                if realValue:
                    temp.append((intermediate[i][j]))
                else:
                    temp.append(j)
        if realValue:
            relationshipMatrix = relationshipMatrix+temp
        else:
            relationshipMatrix.append(temp)
    return relationshipMatrix

def estimateThreshold(data,value):
    """this is the section to calculate the automatic threshold  for clustering the raltionship"""
    # get the threshold that has the minimum standard deviation
    # let hight be 5 percent and let medium be 10 percent and low be 15 percent
    std =[]
    totalLength = len(data)
    expectedcount =0
    if value=='low':
        expectedcount=totalLength*0.003
    elif value=='intermediate':
        expectedcount=totalLength*0.001
    elif value=='high' or value not in ['low','intermediate','high']:
        expectedcount=totalLength * 0.001

    mValue=0.5
    step =0.005
    minValue =sys.float_info.max
    result = 0.3 #ensure the threshold cannot be less than half
    prev = totalLength
    while mValue > step:
        temp = getRelationshipMatrix(mValue,data)
        count = getDerivedCount(temp)
        mValue=mValue-step
        if count < expectedcount:
            return mValue
    return 0.1;

def getDerivedCount(data):
    result=0
    for value in data:
        if len(value) > 0:
            result=result+1
    return result;

def estimateThresholdByVariance(data,value):
    """this is the section to calculate the automatic threshold  for clustering the raltionship"""
    # get the threshold that has the minimum standard deviation
    std =[]
    mValue=0.3
    minValue =sys.float_info.max
    prevVariance =sys.float_info.max
    step =0.05
    result = 0.3 #ensure the threshold cannot be less than half
    while mValue > step:
        print("testing threshold using "+str(mValue))
        temp = getRelationshipMatrix(mValue,data,True)
        dt = np.array(temp)
        minVar = ndimage.variance(dt)
        std.append(abs(prevVariance-minVar))
        mValue=mValue-step
        prevVariance=minVar
    tempResult = sorted(std)
    rTemp=std.index(tempResult[0])
    result-=(rTemp+1)*step
    return 0.05
    print(result)
    exit()
    return result;

def normaliseValue(matrix):
    '''let the value be between zero and one by getting the maximaum'''
    maxValue = getMaximum(matrix)
    minValue = getMinimum(matrix)
    result = []
    for val  in matrix:
        result.append([normalise(x,minValue,maxValue) for x in val])
    return result

def normalise(x,min, max):
    """function that min max normalisation for the value to be calculated"""
    val = (x-min)/(max-min)
    return val

def estimateIntersect(correlation,euclidean):
    """this method helps to estimate the intersection for the three distance metric value"""
    check = len(correlation)==len(euclidean)
    if not check:
        print("error calcualting intersection")
    intersect = []
    for i in range(len(correlation)):
        intersect.append(getIntersection(correlation[i],euclidean[i]))
    return intersect;

def getIntersection(first,second):
    result = reduce(np.intersect1d,(first,second))
    # convert number array to list
    result = result.tolist()
    return result
def getMinimum(value):
    result = []
    for val in value:
        result.append(min(val))
    return min(result)

def getMaximum(value):
    result = []
    for val in value:
        result.append(max(val))
    return max(result)

# function to estimate the nearest neighbor algorithm
def estimateKnn(associationResult,scoreLabels):
    # make the return value from this file be a tupple
    # that also contains the label and the score for the values
    result =[]
    for x in associationResult:
        for y in x:
            score = estimateDistanceScore(x,y)
            resut


    
