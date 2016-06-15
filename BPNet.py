#_*_coding:utf-8_*_
import random
import numpy as np
import math

random.seed(0)

def rand(a, b):  
    return (b-a)*random.random() + a 

def sigmoid(x):
    return math.tanh(x) 

def dsigmoid(y):
    return 1.0 - y**2 

def makeMatrix(I, J, fill=0.0):
    m = []  
    for i in range(I):  
        m.append([fill]*J)  
    return m

class BPNet(object):
    def __init__(self,ni,nh,no):
        self.ni = ni+1
        self.nh = nh+1
        self.no = no

        # activation for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        # 生成权重矩阵，每一个输入层节点和隐藏层节点都连接
        # 每一个隐藏层节点和输出层节点连接
        self.wi = makeMatrix(self.ni,self.nh-1) 
        print self.wi
        self.wo = makeMatrix(self.nh,self.no)
        print self.wo
        # 生成权重，在-0.2-0.2之间
        for i in range(self.ni):
            for j in range(self.nh-1):
                self.wi[i][j] = rand(-0.2,0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0,2.0)
        print self.wi
        print self.wo


        self.ci = makeMatrix(self.ni, self.nh)  
        self.co = makeMatrix(self.nh, self.no)

    def update(self,inputs):
        if len(inputs)!=self.ni-1:
            raise ValueError('wrong number of input')
        # input activations 
        # 输入激励函数
        for i in range(self.ni-1):
            self.ai[i] = inputs[i]

        # hidden activations
        # 隐藏层激励函数
        for j in range(self.nh-1):
            sum = 0.0
            for i in range(self.ni):
                sum +=self.ai[i]*self.wi[i][j]
            self.ah[j] = sigmoid(sum)
        
        # output activations
        # 输出激励函数
        for k in range(self.no):
            sum = 0.0
            for i in range(self.nh):
                sum += self.ah[i]*self.wo[i][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]

    def backPropagate(self,targets,N):
        if len(targets) != self.no:
            raise ValueError('wrong number of values')

        # calculate error terms for output
        # 计算输出层的误差项
        output_delta = [0.0]*self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_delta[k] = dsigmoid(self.ao[k])*error

        # calculate error terms for hidden
        # 计算隐藏层的误差项
        hidden_delta = [0.0]*self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_delta[k]*self.wo[j][k]
            hidden_delta[j] = dsigmoid(self.ah[j])*error
            
        # update output weights
        # 更新输出层的权重参数
        for j in range(self.nh):
            for k in range(self.no):
                change = output_delta[k]*self.ah[j]
                if (j==self.nh-1):        #更新偏置
                    self.wo[j][k] += output_delta[k]
                else:
                    self.wo[j][k] += N*change 
        #print self.wo

        # update input weights
        # 更新输入项的权重参数
        for i in range(self.ni):
            for j in range(self.nh-1):
                change = hidden_delta[j]*self.ai[i]
                if (i==self.ni-1):        #更新偏置
                    self.wi[i][j] += hidden_delta[j]
                else:
                    self.wi[i][j] += N*change 
        #print self.wi

        # calculate wrror
        # 计算E(W)
        error = 0
        for k in range(len(targets)):
            error += 0.5*(targets[k]-self.ao[k])*2
        return error

    def test(self,patterns):
        for p in patterns:
            print (p[0],'->',self.update(p[0]))

    def weights(self):
        print ('Input weights:')
        for i in range(self.wi[i]):
            print (self.wi[i])
        print ('Output weights')
        for j in range(self.nh):
            print (self.wo[j])

    def train(self,patterns,iteration=1000,N=0.5):
        # N: learning rate    
        for i in range(iteration):  
            error = 0.0  
            for p in patterns:  
                inputs = p[0]  
                targets = p[1]  
                self.update(inputs)  
                error = error + self.backPropagate(targets, N)  
            if i % 100 == 0:  
                print('error %-.5f' % error)
def demo():  
    # Teach network XOR function  
    pat = [  
        [[0,0,0], [0]],  
        [[0,1,0], [1]],  
        [[1,0,0], [0]],  
        [[1,1,1], [1]]  
    ]  
    dat = [[[0,1,1],[123]]]
    # create a network with two input, two hidden, and one output nodes  
    n = BPNet(3, 2, 1)  
    # train it with some patterns  
    n.train(pat)  
    # test it  
    n.test(pat)
    n.test(dat)




if __name__ == '__main__':
    demo()

