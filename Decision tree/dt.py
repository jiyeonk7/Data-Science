import pandas as pd
import math
from sys import argv


def makeDB(file):
    dataSet = list()
    with open(file, "r") as f:
        datum = f.read().splitlines()
        for data in datum:
            attribute = data.split('\t')
            dataSet.append(attribute)
    dataSet = pd.DataFrame(dataSet)
    attributes = dataSet.iloc[0]
    dataSet = dataSet[1:]
    dataSet.columns = attributes

    return dataSet


class Dtree():
    def __init__(self, dataSet, node_type = 'attributeNode'):
        self.node_type = node_type
        self.dataSet = dataSet
        self.labelProb = self.dataSet.iloc[:,-1].value_counts().idxmax()
        
        if node_type == 'attributeNode':
            self.buildTree()
        elif node_type == 'leafNode':
            self.labelProb = self.dataSet.iloc[:,-1].value_counts().idxmax()
    
    def buildTree(self):
        self.bestAttrib = selectAttrib(self.dataSet)
        self.classify(self.dataSet[self.bestAttrib])
    
    def checkNext(self, dataSet):
        labelProb = dataSet.iloc[:,-1].unique()
        if len(labelProb) == 1:
            self.noCreateNext = True
        elif len(dataSet.columns) <= 2:
            self.noCreateNext = True
        else:
            self.noCreateNext = False
        return self.noCreateNext 
    
    def classify(self, column):
        labels = column.unique()
        self.children = dict()
        
        for label in labels:
            Pdataset = self.dataSet.loc[self.dataSet[self.bestAttrib] == label]
            if self.checkNext(Pdataset):
                self.children[label] = Dtree(Pdataset, node_type = 'leafNode')
            else:
                self.children[label] = Dtree(Pdataset.drop(self.bestAttrib, 1))
    
    def testData(self, series):
        if self.leaf():
            return self.labelProb
        else:
            label = series[self.bestAttrib]
            try:
                child = self.children[label]
            except:
                return self.labelProb
            return child.testData(series)
    
    def leaf(self):
        return self.node_type == 'leafNode'


def calEntropy(values):
    total = values.sum()
    entropy = 0
    for value in values:
        if value:
            entropy = -((value/total)*math.log(value/total)/math.log(2)) + entropy
        else:
            return 0
    return entropy

def calGainRatio(trainDB):
    total = trainDB.values.sum()
    gain = 0
    for row in trainDB.values:
        gain = (row.sum()/total)*calEntropy(row) + gain
    
    splitInfo = 0
    for row in trainDB.values:
        splitInfo = -((row.sum()/total)*math.log(row.sum()/total)/math.log(2)) + splitInfo
    
    gainRatio = gain / splitInfo
    return gainRatio

def selectAttrib(dataSet):
    attributes = dict()
    targetClass = dataSet[dataSet.columns[-1]]
    for column in dataSet.columns[:-1]:
        attribute = dataSet[column]
        DB = pd.crosstab(attribute, targetClass)
        attributes[column] = calGainRatio(DB)
    return min(attributes.keys(), key=(lambda x: attributes[x]))


def writeOutput(line, file):
    with open(file, 'a') as f:
        new = ''
        for word in line:
            new = new + (word + '\t')
        f.write(new[:-1] + '\n')
        
    

if __name__ == '__main__':
    trainFile = argv[1]
    testFile = argv[2]
    outputFile = argv[3]
    
    trainSet = makeDB(trainFile)
    
    tree = Dtree(trainSet)
    
    attribute = trainSet.columns
    attribute = list(attribute)
    writeOutput(attribute, outputFile)
    
    testSet = makeDB(testFile)
    for _,row in testSet.iterrows():
        line = row.values
        clabel = tree.testData(row)
        line = list(line)
        line.append(clabel)
        writeOutput(line, outputFile)
    
    
    