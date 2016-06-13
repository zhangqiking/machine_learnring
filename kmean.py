from sklearn.cluster import KMeans
import numpy as np

def loadData(path):
    datamat = []
    labelmat = []
    fr = open(path)
    for line in fr.readlines():
        temp = []
        l=line.strip().split(',')
        for i in range(4):
            try:
                temp.append(float(l[i]))
            except:
                print 'ValueError'
                
        datamat.append(temp)
        labelmat.append(float(l[-1]))
    return datamat,labelmat

data,label = loadData('C:\\Users\\Qi\\Desktop\\iris.csv')
clf = KMeans(n_clusters=3)
s = clf.fit(data)
for i in range(1,30,1):
    clf = KMeans(n_clusters=i)
    s = clf.fit(data)
    print i , clf.inertia_
