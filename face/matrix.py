#!/bin/python

from numpy import *
datas = []

def load_data(path):
    f = open(path)
    data = []
    for line in f.readlines():
        arr = []
        lines = line.strip().split("\t")
        for x in lines:
            if x != "-":
                arr.append(float(x))
            else:
                arr.append(float(0))
        #print arr
        data.append(arr)
    # print data
    return data

def gradAscent(data, K):
    dataMat = mat(data)
    print dataMat
    m, n = shape(dataMat)
    # print m,n
    p = mat(random.random((m, K)))
    # print p
    q = mat(random.random((K, n)))
    # print q

    alpha = 0.0002
    beta = 0.02
    maxCycles = 10000

    for step in xrange(maxCycles):
        for i in xrange(m):
            for j in xrange(n):
                if dataMat[i,j] > 0:
                    #print dataMat[i,j]
                    error = dataMat[i,j]
                    for k in xrange(K):
                        error = error - p[i,k]*q[k,j]
                    for k in xrange(K):
                        p[i,k] = p[i,k] + alpha * (2 * error * q[k,j] - beta * p[i,k])
                        q[k,j] = q[k,j] + alpha * (2 * error * p[i,k] - beta * q[k,j])

        loss = 0.0
        for i in xrange(m):
            for j in xrange(n):
                if dataMat[i,j] > 0:
                    error = 0.0
                    for k in xrange(K):
                        error = error + p[i,k]*q[k,j]
                    loss = (dataMat[i,j] - error) * (dataMat[i,j] - error)
                    for k in xrange(K):
                        loss = loss + beta * (p[i,k] * p[i,k] + q[k,j] * q[k,j]) / 2



        if loss < 0.001:
            break
        #print step
        if step % 1000 == 0:
            print loss
        global datas
        datas.append(loss)


    return p, q


if __name__ == "__main__":
    dataMatrix = load_data("./data")

    p, q = gradAscent(dataMatrix, 5)
    '''
    p = mat(ones((4,10)))
    print p
    q = mat(ones((10,5)))
    '''
    result = p * q
    print p
    print q

    print result


    from pylab import *
    from numpy import *
    #
    # data = []
    #
    # f = open("result")
    # for line in f.readlines():
    #     lines = line.strip()
    #     data.append(lines)
    # print data
    n = len(datas)
    x = range(n)

    plot(x, datas, color='r', linewidth=3)
    plt.title('Convergence curve')
    plt.xlabel('generation')
    plt.ylabel('loss')
    show()