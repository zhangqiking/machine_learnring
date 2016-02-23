# _*_coding:utf-8_*_

from numpy import *
FLAG = True                                                   #定义全局变量
def LoadData(path):                                           #数据预处理，将特征向量储存在列表中                                            
    datamat=[] ; datalabel=[]
    fr=open(path)
    for line in fr.readlines():
        lineArr=line.strip().split()
        datamat.append([int(lineArr[0]),int(lineArr[1])])
        datalabel.append(int(lineArr[2]))
    return datamat,datalabel

def retu(dataMatrix,labelMat,w0,w1,b,m,eta):            #用于跳出if和for循环的return函数（多层循环的跳出问题）
    global FLAG
    for i in range(m):
            x0=dataMatrix[i][0]
            x1=dataMatrix[i][1]
            y =labelMat[i]
            temp=labelMat[i]*(w0*x0+w1*x1+b)
            if temp<=0:            #判断是否有误分类
                w0=w0+eta*y*x0
                w1=w1+eta*y*x1
                b=b+eta*y
                FLAG = True
                print FLAG
                return w0,w1,b
    FLAG = False
    return w0,w1,b

                

def perceptron(datamat,datalabel,init_coef,eta):    #感知机主函数函数
    global FLAG
    dataMatrix=array(datamat)
    labelMat=array(datalabel)
    w_0=init_coef[0]
    w_1=init_coef[1]
    b_0 =init_coef[2]
    m,n=shape(dataMatrix)
    while FLAG:
        w0,w1,b = retu(dataMatrix,labelMat,w_0,w_1,b_0,m,eta)
        w_0=w0
        w_1=w1
        b_0=b
    return w0,w1,b

datam,labelm=LoadData('C:\\Users\\UESTC\\Desktop\\per_data.txt') 
print perceptron(datam,labelm,[1,1,0],1)


        
       




