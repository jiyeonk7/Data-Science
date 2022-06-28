import sys
import math

def prepdata(f1, f2):
    train = dict()
    test = list()
    
    with open(f1, 'r') as f1:
        trdata = f1.read().split('\n')
        trdata = trdata[:-1]
        for line in trdata:
            record = line.split('\t')
            userid = record[0]
            item = record[1]
            rating = record[2]
            train.setdefault(userid, {})
            train[userid][item] = int(rating)
        
    with open(f2, 'r') as f2:
        tedata = f2.read().split('\n')
        tedata = tedata[:-1]
        for line in tedata:
            trecord = line.split('\t')
            tuserid = trecord[0]
            titem = trecord[1]
            trating = trecord[2]
            ttimestamp = trecord[3]
            test.append((tuserid, titem, trating, ttimestamp))
    
    return train, test


def cf(train, test):
    users = list()
    rec = set()
    rate = list()
    
    for record in test:
        testuser = record[0]
        testitem = record[1]
        
        if testuser not in rec:
            cset = recommendation(train, testuser)
        
        rec.add(testuser)
        
        for item in cset:
            if item[1] == testitem:
                rate.append(item[0])
                
        if len(rate) == 0:
            rate = [5]
        
        record = [testuser, testitem, rate[0]]
        users.append(record)
    return users



def recommendation(train, testuser):
    itemcoefficient = dict()
    rating = dict()
    
    for trainuser in train:
        if trainuser != testuser:
            coefficient = pearson(train, testuser, trainuser)
            if coefficient > 0:
                for item in train[trainuser]:
                    if item not in train[testuser] or train[testuser][item] == 0:
                        itemcoefficient.setdefault(item, 0)
                        itemcoefficient[item] = itemcoefficient[item] + coefficient
                        rating.setdefault(item, 0)
                        rating[item] = rating[item] + train[trainuser][item]*coefficient
    cset = [(total/itemcoefficient[item], item) for item, total in rating.items()]
    return cset


def pearson(train, testuser, trainuser):
    common = dict()
    for item in train[testuser]:
        if item in train[trainuser]:
            common[item] = 1
    
    count = len(common)
    if count != 0:
        testsum = 0
        trainsum = 0
        testsum1 = 0
        trainsum1 = 0
        productsum = 0
        
        for item in common:
            testsum = testsum + train[testuser][item]
        for item in common:
            trainsum = trainsum + train[trainuser][item]
            
        for item in common:
            testsum1 = testsum1 + train[testuser][item]*train[testuser][item]
        for item in common:
            trainsum1 = trainsum1 + train[trainuser][item]*train[trainuser][item]
            
        for item in common:
            productsum = productsum + train[testuser][item]*train[trainuser][item]
            
        x = productsum - (testsum*trainsum/count)
        y = math.sqrt((testsum1 - (testsum*testsum)/count)*(trainsum1 - (trainsum*trainsum)/count))
        
        if y == 0:
            return 0
        
        return (x/y)
    
    else:
        return 0


def writeoutput(fname, data):
    ofname = fname + '_prediction.txt'
    with open(ofname, 'w') as output:
        for i in range(len(data)):
            line = ''
            for j in range(len(data[0])):
                line = line + '%s\t' % (data[i][j])
            line = line[:-1]
            line = line + '\n'
            
            output.write(line)



if __name__ == "__main__":
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    
    train, test = prepdata(trainfile, testfile)
    recommended = cf(train, test)
    writeoutput(trainfile, recommended)
    