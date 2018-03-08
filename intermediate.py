import fileHandler as handle
import general
import sys
human ="human.csv"
parasite='parasite.csv'
defaultRate='high'
rate ='high'
metric ='';
acceptedInput = ['low','intermediate','high']
metric =''
acceptedMetric=['correlation','euclidean','cosine']
if len(sys.argv) > 1:
    rate =sys[1]
    if rate not in acceptedInput:
        handle.showUsage()
    if len(sys.argv)  > 2:
        metric = sys.argv[2]
        if metric not in acceptedMetric:
            showUsage()
print("loading data...")
humanLabel,humanData = handle.read2Matrix(human)
parasiteLabel,parasiteData = handle.read2Matrix(parasite)
print('done loading data')
print("normalising data")
humanData = general.normaliseValue(humanData)
parasiteData = general.normaliseValue(parasiteData)
print("done normalising data")
print("building correlation distance model")
correlation = general.buildIntermediateRelationship(humanData,parasiteData,'correlation')
print("done building correlation distance model")
print("building euclidean distance model")
# euclidean = general.buildIntermediateRelationship(humanData,parasiteData,'euclidean')
# print("done building euclidean distance model")
filename='intermediate.csv'
print('estimating threshold')
# correlationThreshold=general.estimateThresholdByVariance(correlation,rate)
# euclideanThreshold = general.estimateThresholdByVariance(euclidean,rate)
print("done estimating threshold")
print("building gene expression relationship model")
print("estimating correlation relationship matrix")
# manually add the threshold value here
correlationThreshold = 0.1
correlationRelationshipMatrix = general.getRelationshipMatrix(correlationThreshold,correlation,humanLabel,parasiteLabel)
print("done estimating correlation relationship matrix")
print("estimating euclidean relationship matrix")
# euclideanRelationshipMatrix = general.getRelationshipMatrix(euclideanThreshold,euclidean)
print("done estimating euclidean relationship matrix")
print("estimating relationship intersect")
intersect = general.estimateIntersect(correlationRelationshipMatrix,euclideanRelationshipMatrix)
print("building graph structure")
node1,node2,edges = general.extractNodes(humanLabel,parasiteLabel,intersect,correlation)
print("done building graph structure")
print("displaying graph")
general.buildGraph(node1,node2,edges)
