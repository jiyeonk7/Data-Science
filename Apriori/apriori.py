from sys import argv
from itertools import combinations
from collections import defaultdict

transDB = list()


#make a databaste of transactions from the input.txt
def makeDB(files):
    with open(files, "r") as f:
    	transactions = f.read().splitlines()
    	transID = 0
    	for transaction in transactions:
            itemID = transaction.split('\t')				
            transDB.append(itemID)
            transID = transID + 1


#checks whether the candidate pattern's support is larger
#than the minimum support given by the user initially
def checkSupp(keys, minS, FP):
    freqP = dict()
    for key, value in keys.items():
	if((int(value)) > (int(minS)-1)):
	    freqP[key] = value
	    item = list()
	    item.append(key)
	    item.append(value)
	    FP.append(item)
	else:
	    continue
	    
    return freqP


#joins k-frequent pattern set to make (k+1)-candidate set
def selfjoin(setLen, prevFP):
    i = 0
    prev = list()

    for keys in prevFP.keys():
	if setLen == 2:
	    if keys not in prev:
  	        prev.append(keys)
	    else:
		continue
	else:
	    for key in keys:
	        if key not in prev:
		    prev.append(key)
	        else:
		    continue

    Clist = list(combinations(prev, setLen))
    return Clist


#counts the support of each candidate in the candidate set
def countSupp(candSet, setLen):
    itemID = list()
    candlist = dict()

    i = 0
    for i in range(len(transDB)):
	itemID = transDB[i]
	for itemList in candSet:
	    cnt = 0
	    for item in itemList:
		if item in itemID:
		    cnt = cnt + 1
	        else:
		    continue
	    if cnt == (len(itemList)):
		if itemList not in candlist.keys():
		    candlist[itemList] = 1
		else:
		    candlist[itemList] = candlist[itemList] + 1
    return candlist


#with the (k+1)-candidate set generated with selfjoin function,
#check whether all subsets of the pattern are frequent patterns
def prune(candidateSet, previousList, length):
    allposs = list()
    existingSet = list()
    prunedSet = list()
    prev = list()
    for key in previousList.keys():
	prev.append(key)
    
    for itemlist in candidateSet:
	k = length-1
	allposs = list(combinations(itemlist, k))
	
	i = 0
	for i in range(len(allposs)):
	    if allposs[i] in prev:
		if itemlist not in prunedSet:
		    prunedSet.append(itemlist)
		else:
		    continue
    return prunedSet


#after mining the frequent pattern set with apriori algorithm,
#calculate the support and confidence of the pattern with its subsets
#and print the results to output.txt
def calSuppConf(FPList, previous, output):
    for pattern in FPList.keys():
	if len(pattern) == 2:
	    itemset = pattern[0]
	    assoitemset = pattern[1]
	    supp = (float(FPList[pattern])/float(len(transDB)))*100

	    i = 0
	    for i in range(len(previous)):
		if itemset == previous[i][0]:
		    cnt_i = previous[i][1]
		else:
		    continue
		
		j = 0
		for j in range(len(previous)):
		    if assoitemset == previous[j][0]:
			cnt_a = previous[j][1]
		    else:
		        continue
	    
		    conf_i = (float(FPList[pattern])/float(cnt_i))*100 
		    conf_a = (float(FPList[pattern])/float(cnt_a))*100
		    
		    writeOutput(itemset, assoitemset, supp, conf_i, output)
		    writeOutput(assoitemset, itemset, supp, conf_a, output)
		    
	else:
	    r = 0
	    combi = list()
	    for r in range(len(pattern)-1):
		poss = list(combinations(pattern, r+1))
		combi = combi + poss
	    k = 0
	    for k in range(len(combi)):
		itemset = combi[k]
		assoitemset = list(set(pattern) - set(combi[k]))
		supp = (float(FPList[pattern])/float(len(transDB)))*100
		
		l = 0
	    	for l in range(len(previous)):
		    if len(itemset) == 1:
			if itemset[0] == previous[l][0]:
			    cnt = previous[l][1]
		        else:
			    continue
		    else:
	  	        if itemset == previous[l][0]:
			    cnt = previous[l][1]
		        else:
			    continue
		    
		    conf = (float(FPList[pattern])/float(cnt))*100
		    writeOutput(itemset, assoitemset, supp, conf, output)



#prints the itemset, associative itemset, support, and confidence into the file
#that the user mentioned intially
def writeOutput(iset, aset, supp, conf, fname):
    line = "{"+str(iset)+"}" + '\t' + "{"+str(aset)+"}" + '\t' + "{"+str('%.2f' %round(supp, 2))+"}" + '\t' + "{"+str('%2.f' %round(conf, 2))+"}" + '\n'
    
    with open(fname, 'a') as f:
	f.write(line)
	
	    

if __name__ == '__main__' :
    minSuppPer = argv[1]
    inputFile = argv[2]
    outputFile = argv[3]

    makeDB(inputFile)

    minSupp = ((int(minSuppPer))*(len(transDB)))/100

    freqPatterns = list()
    candidates = dict()  
    previousFP = list()

    i = 0
    for i in range(len(transDB)):
	j = 0
	transLen = len(transDB[i])
	for j in range(transLen):
	    if transDB[i][j] not in candidates.keys():
		candidates[transDB[i][j]] = 1
	    else:
		candidates[transDB[i][j]] = candidates[transDB[i][j]] + 1
    
    previousFP = checkSupp(candidates, minSupp, freqPatterns)
    firstFreqSet = previousFP
    
    k = 2
    t = len(candidates)
    while t != 0:
	plist = list()
        clist = dict()  
	if k == 2:
            candidate = selfjoin(k, previousFP)
	    clist = countSupp(candidate, k)
	    previousFP = checkSupp(clist, minSupp, freqPatterns)
	    k = k + 1
	    t = len(candidate)
	    
	else:
	    candidate = selfjoin(k, previousFP)
	    plist = prune(candidate, previousFP, k)
	    if len(plist) == 0:
	        break
	    
	    clist = countSupp(plist, k)
	    previousFP = checkSupp(clist, minSupp, freqPatterns)
	    k = k + 1
	    t = len(candidate)

        calSuppConf(previousFP, freqPatterns, outputFile)

    #prints the frequent pattern sets in the given database
    print("final: ", freqPatterns)

