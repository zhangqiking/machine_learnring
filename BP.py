import numpy as np

def sigmoid(x,deriv=False):
    if (deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

# input dataset
x= np.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1]])
#output dataset
y= np.array([[0,0,1,1]]).T

np.random.seed(1)
syn0= 2*np.random.random((3,1))-1
print syn0
for iter in xrange(10000):
    # forward propagation
    l0 = x
    l1 = sigmoid(np.dot(l0,syn0))
 
    # how much did we miss?
    l1_error = y - l1
 
    # multiply how much we missed by the 
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * sigmoid(l1,True)
 
    # update weights
    syn0 += np.dot(l0.T,l1_delta)
print "Output After Training:"
print l1
