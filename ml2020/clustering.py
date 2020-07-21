from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

#считаем расстояния
def d(x, y):
    return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

#считаем ошибку
def E_calc(centroid, i):
    Ej = 0
    sArr = np.zeros((i, 2))
    amount = np.zeros(i)
    for j in range(N):
        dArr = np.zeros(i)
        for t in range(i):
            dArr[t] = d(centroid[t], X[j])
        index = np.argmin(dArr)
        sArr[index] += X[j]
        amount[index] +=1
        Ej += dArr[index]**2 
    return Ej, sArr, amount 

#правило локтя
def D_calc(E):
    D = np.zeros(K-1)
    D[0] = 1
    for i in range(1,K-1):
        D[i] = np.float64(abs(E[i]-E[i+1]) / abs(E[i-1]-E[i]))
    return D    

def kmeans(X):
    centroids = np.zeros((K, K, 2))
    E = np.zeros(K)
    ind = np.random.randint(0, N, K)
    centroid = X[ind]
    for k in range(1,K+1):
        prev = np.zeros((k, 2))
        stop = False
        Ej = 0    
        while(stop != True):

            Ej, sArr, amount = E_calc(centroid, k)
            for i in range(k):
                prev[i] = centroid[i]
                if (amount[i] != 0):
                    centroid[i] = sArr[i]/amount[i]
                if (prev[i, 0] == centroid[i,0] and prev[i, 1] == \
                                                                centroid[i, 1]):
                    stop=True
                
        E[k-1] = Ej
        for j in range(k):
            for q in range(2):
                centroids[k-1, j, q] = centroid[j, q]
    

    return E, centroids

#сколько цветов надо
def colors(X, dArr, centroids):
    cArr = np.linspace(0, K - 1, K)
    num = np.argmin(dArr)
    cList = []
    for i in range(N):
        r = np.zeros((num+1))
        for j in range(num+1):
            r[j] = d(centroids[num, j], X[i])
        cList.append(cArr[np.argmin(r)])    
    return cList, num   

#рисуем графики
def g(dArr, E, centroids):
    colArr, num = colors(X, dArr, centroids)
    figure, ax = plt.subplots(nrows = 3, ncols = 1, figsize = (8, 16))
    ax1, ax2, ax3 = ax.flatten()
    xArr = np.arange(1, K+1)
    ax1.plot(xArr, E)
    ax1.set_ylabel('E(k)')
    xArr = np.arange(1, K)
    ax2.plot(xArr, dArr)
    ax2.set_ylabel('D(k)')
    ax2.grid(True)
    ax3.scatter(X[:, 0], X[:, 1], c = colArr, s = 3)
    
    ax3.scatter(centroids[num, : num + 1, 0],centroids[num, : num + 1, 1], 100,\
                                                        c = 'r', marker = '*')

    plt.show
    


centers = [[-1, -1], [0, 1], [1, -1]]
N = 3000
K = 10

X, _ = make_blobs(n_samples=N, centers=centers, cluster_std = 0.5)
E, centroids = kmeans(X)            
dArr = D_calc(E)
g(dArr, E, centroids)
