# _*_coding:utf-8_*_
from scipy import stats
from numpy import *

def Gaus_dis(y,mui,sigma):
    return stats.norm.pdf(y,mui,sigma)

def Gaus_EM(data,sig,mu,alp):
    sigma = sig
    mui = mu
    alph = alp
    
    num = len(data)
    max_iter = 1
    for i in range(max_iter):
        gama=zeros((num,2))
        for j in range(num):

##########  E   ############         
            temp2=[]
            for k1 in range(2):   #对每一个分模型循环
                temp1 = alph[k1]*Gaus_dis(sigma[k1],mui[k1],data[j]) 
                #print temp1
                temp2.append(temp1)

            temp_sum = temp2               #保存模型概率分布值
            print temp_sum
            
            for k2 in range(2):
                gama[j][k2] = temp_sum[k2]/sum(temp_sum)    #计算每一个分模型对观测数据的响度
            #print array(gama[:,0])

########  M     ##########
        for k3 in range(2):
            gama_mat=mat(gama[:,k3])
            data_mat=mat(data)
            data_mui=[0,0,0,0,0]

            for k4 in range(num):
                data_mui[k4] = data[k4] - mui[k3]
            data_mui_mat = mat(data_mui)

            mui[k3] = sum(gama_mat*data_mat.T)/sum(gama_mat)
            sigma[k3] = sum(gama_mat*data_mui_mat.T)/sum(gama_mat)
            alph[k3] = sum(gama_mat)/num
            
    return mui,sigma,alph

data = [0.5,0.88,1.2,0.5,0.4]

print Gaus_EM(data,[0.5,0.5],[0.5,0.2],[0.5,0.3])



    

