# _*_coding:utf-8_*_
# 统计学方法中关于抛硬币的ＥＭ算法
from numpy import *

data =array([1,1,0,1,0,0,1,0,1,1,0,1,1,1,0,0,1,1])

def EM(data,parm):
    pai = parm[0]
    p = parm[1]
    q = parm[2]
    num = len(data)
    mui = zeros((num,1))
    for i in range(50):       #最大迭代次数
        for j in range(num):
            temp1 = pai*(p**data[j])*((1-p)**(1-data[j]))      #E步:计算给定参数下概率的条件分布 
            temp2 = (1-pai)*(q**data[j])*((1-q)**(1-data[j]))
            mui[j] = temp1/float(temp1+temp2)
        pai = sum(mui)/num                                     #M步:最大化Q函数
        p = sum(mui.T*data)/sum(mui)
        q = sum((1-mui.T)*data)/sum(1-mui)
    return pai,p,q

print EM(data,[0.4,0.6,0.7])



