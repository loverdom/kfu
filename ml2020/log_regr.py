import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits


#функция стандартизации
def standartization(x):
    mu_t=[]
    sigma_t=[]
    for i in range(D):
        mu_t.append(np.mean(x[:, i]))
    for i in range(D):
        sigma_t.append(np.sqrt(np.mean((x[:, i]- mu_t[i])**2))) 
    mu = np.array(mu_t)
    sigma = np.array(sigma_t) 
    for i in range(D):
        if sigma[i] != 0:
            x[:, i]=(x[:, i]-mu[i])/sigma[i]       
    return x

#функция перемешивания
def shuffle(x, t):
    ind = np.arange(N)
    np.random.shuffle(ind)
    ind_train = ind[:np.int32(0.8*len(ind))]
    ind_valid = ind[np.int32(0.8*len(ind)):]
    x_train = x[ind_train, :]
    x_valid = x[ind_valid, :]
    t_train = t[ind_train]
    t_valid = t[ind_valid]
    return x_train, x_valid, t_train, t_valid
    
#функция инициализации W
#первым столбцом будет вектор bias
def init_W(sigma):
    b = init_b(sigma)
    W =  sigma*np.random.rand(K, D)
    for i in range(K):    
        W[:, 0] = b[i]
    return W    

def init_b(sigma):
    return sigma*np.random.rand(K)
    
#предсталвение в one-hot-encoding
def onehot(t):
    n = np.int32(len(t))
    T = np.zeros((n, K))
    for i in range(n):
        T[i][t[i]] = 1
    return T           

#функция softmax с решением overflow
def softmax(u):
    u -= np.max(u)
    s = np.sum(np.exp(u))
    return np.exp(u)/s

#инициализирую матрицу с выходами softmax, здесь смещаю матрицу Х добавление 
#столбца единичек    
def Y(W, X):
    n = np.int32(len(X))
    X_temp = np.ones((n, D+1))
    Y = np.zeros((n, K))
    for i in range(1, D+1):
        X_temp[:, i] = X[:, i-1]
    for j in range(n):
        Y[j, :] = softmax(W@X[j, :])        
    return Y   
            
#матрица частных произвдных
def nabla_E(Y, X, T):
    return (Y - T).T@X

#целевая функция
def E(Y, T):
    y = np.log(Y.T)
    n = np.int32(len(T))
    E = 0
    for i in range(n):
        E += T[i, :] @ y[:, i]
    return -E    

#точность
def accuracy(Y, T):
    n = np.int32(len(Y))
    count = 0
    for i in range(n):
        if np.argmax(Y[i, :]) == np.argmax(T[i, :]):
            count += 1
    return count/n        

#основная ф-ия град-го спуска
def grad(X_train, T_Train, X_valid, T_valid):
    
    sigma = 5*10**(-1)
    gamma = 5*10**(-4)
    #случайная инициализация W 
    W = init_W(sigma)   
    #начальные значения точностей на valid для входа в цикл
    acc_v_step = 1
    acc_v = 0
    Y_train = None
    Y_valid = None
    #списки ошибок и точностей на выборках
    acc_v_list = []
    acc_t_list = []
    E_v_list = []
    E_t_list = []    
    q = 0
    #пока точность на valid растёт
    while acc_v < acc_v_step:
        #считаем итерцаию
        q += 1               
        #инициализировали начальные Y на обеих выборках        
        Y_train = Y(W, X_train)
        Y_valid = Y(W, X_valid)
        #посчитали точности на выборках и записали их
        acc_t = accuracy(Y_train, T_train)
        acc_t_list.append(acc_t)        
        acc_v = accuracy(Y_valid, T_valid)
        acc_v_list.append(acc_v)
        #посчитали ошибки на выборках и записали их
        E_v = E(Y_valid, T_valid)
        E_t = E(Y_train, T_train)
        E_v_list.append(E_v)
        E_t_list.append(E_t)
        #выводим чётные итерации
        if q%2 == 0:    
            print('---------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print('Итераця ({}), точность на valid-set = {}, точность на train-set = {}, ошибка на train-set = {}, ошибка на valid-set = {}'.format(q, acc_v, acc_t, E_t, E_v))        
        #делаем проверочный шаг
        W_temp = W - gamma * nabla_E(Y_train, X_train, T_train)        
        #считаем, увеличиться ли точность на train, если мы шаг сделаем
        acc_t_step = accuracy(Y(W_temp, X_train), T_train)        
        #если да, перезаписываем W
        if acc_t_step > acc_t:
            W = W_temp
        #считаем следущую точность на valid
        acc_v_step = accuracy(Y(W, X_valid), T_valid)
    #берем конечную точность
    accuracy_ret = acc_v_list[-1]    
    #возвращаем списки и конечную точность на валидационной
    return E_t_list, acc_t_list, E_v_list, acc_v_list, accuracy_ret            
        
N = 1797
K = 10
D = 64
digits = load_digits()
T = onehot(digits.target)
X = standartization(digits.data)
X_train, X_valid, T_train, T_valid = shuffle(X, T)

et, at, ev, av, acc_print = grad(X_train, T_train, X_valid, T_valid)

print('----------------------------------------------------------------')
print('Final accuracy on valid: {}'.format(acc_print))






x_et = np.arange(np.int32(len(et)))
x_at = np.arange(np.int32(len(at)))
x_av = np.arange(np.int32(len(av)))
x_ev = np.arange(np.int32(len(ev)))


fig1, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize=(8, 4))
fig2, (ax3, ax4) = plt.subplots(nrows = 1, ncols = 2, figsize=(8, 4))


ax1.set_title('Ошибка на train set')
ax1.plot(x_et, et)

ax2.set_title('Точность на train set')
ax2.plot(x_at, at)

ax3.set_title('Ошибка на valid set')
ax3.plot(x_ev, ev)

ax4.set_title('Точность на valid set')
ax4.plot(x_av, av)


plt.show()
