import sys
import math

clusternum = list()

def readinput(file):
    D = list()
    
    with open(file, 'r') as d:
        dataset = d.read().split('\n')
        for item in dataset:
            item = item.split('\t')
            if len(item) != 3:
                continue
            else:
                D.append(item)
        return D
    
    
def cluster(D, id, label, eps, minpts):
    global clusternum
    
    neighbors = findN(D, id, eps)
    
    if len(neighbors) >= minpts:
        clusternum[id] = label
        
        for neighbor in neighbors:
            clusternum[neighbor] = label
        
        while len(neighbors) > 0:
            neighbor = neighbors[0]
            Nchild = findN(D, neighbor, eps)
            if len(Nchild) >= minpts:
                for i in range(len(Nchild)):
                    k = Nchild[i]
                    if clusternum[k] == None or clusternum[k] == -1:
                        neighbors.append(k)
                        clusternum[k] = label
            neighbors = neighbors[1:]
        return True
    
    else:
        clusternum[id] = -1
        return False

    
def findN(D, id, eps):
    Nlist = list()
    oricordinate = D[id][1:]
    
    for neighbor in range(len(D)):
        ncord = D[neighbor][1:]
        if Ncheck(oricordinate, ncord, eps):
            Nlist.append(neighbor)
    
    return Nlist


def Ncheck(ori, neighbor, eps):
    ori_x = float(ori[0])
    ori_y = float(ori[1])
    nei_x = float(neighbor[0])
    nei_y = float(neighbor[1])
    
    distance = math.sqrt(math.pow(ori_x - nei_x, 2) + math.pow(ori_y - nei_y, 2))
    
    return (distance < eps)


def controlcnum(cnum):
    ccount = len(str(clusternum))
    print(ccount)
    
    if ccount > cnum:
        for k in range(len(clusternum)):
            if clusternum[k] >= cnum:
                clusternum[k] = cnum - 1


def write(inputfile):
    inputname = inputfile.replace('.txt', '')
    for label in range(len(set(clusternum))-1):
        fname = inputname + '_cluster_' + str(label) + '.txt'
        IDlist = [i for i, j in enumerate(clusternum) if j == label]
        
        temp = ''
        for id in IDlist:
            temp += str(id) + '\n'
        with open(fname, 'w') as o:
            o.write(temp)

        
        
if __name__ == '__main__':
    inputfile = sys.argv[1]
    cnum = int(sys.argv[2])
    eps = int(sys.argv[3])
    minpts = int(sys.argv[4])
    
    dataset = readinput(inputfile)
    
    clabel= 0
    
    clusternum = [None]*len(dataset)
    
    for id in range(len(dataset)):
        if clusternum[id] == None:
            if cluster(dataset, id, clabel, eps, minpts):
                clabel = clabel + 1
    
    controlcnum(cnum)
    write(inputfile)
 