import numpy as np
import matplotlib.pyplot as plt

#матрица плана
def calc_design_matrix(x, basic):
    design_matrix = np.ones((len(x), len(basic)+1))
    for i in range(0, len(basic)):
        design_matrix[:, i + 1] = basic[i](x)
    return design_matrix    


#вычисление параметров
def calc_w(x, t, lam_cur, basic):
    design_matrix = calc_design_matrix(x, basic)
    I = np.eye((len(basic) + 1))
    w =  np.linalg.inv(design_matrix.T@design_matrix + lam_cur*I)@design_matrix.T@t
    return w
                         
                         
#ошибка
def calc_E(x, t, w, basic):
    design_matrix = calc_design_matrix(x, basic)
    y = design_matrix@w.T   
    E = np.sum((y-t)**2)*1/2
    return E



N = 1000
x = np.linspace(0, 1, N)
z = 20 * np.sin(2 * np.pi * 3 * x) + 100 * np.exp(x)
error = 10 * np.random.randn(N)
t = z + error

#делим индексы и устраиваем мешанину 
ind = np.arange(N)
np.random.shuffle(ind)
ind_train = ind[:np.int32(0.8*len(ind))]
ind_valid = ind[np.int32(0.8*len(ind)):np.int32(0.9*len(ind))]
ind_test = ind[np.int32(0.9*len(ind)):]

#датасет
x_train = x[ind_train]
x_valid = x[ind_valid]
x_test = x[ind_test]
t_train = t[ind_train]
t_valid = t[ind_valid]
t_test = t[ind_test]


#число раундов в цикле 
rounds = 3000

#начальное минимальное значение функции потери
E_min = 10**10

#массив базисных функций
basic_func = np.array([np.sin, np.cos, np.exp, np.sqrt, lambda x: x**2, lambda x: x**3, lambda x: x**4,lambda x: x**5,lambda x: x**6,lambda x: x**7,lambda x: x**8,lambda x: x**9,lambda x: x**10,lambda x: x**11,lambda x: x**12,lambda x: x**13,lambda x: x**14,lambda x: x**15,lambda x: x**16,lambda x: x**17,lambda x: x**18,lambda x: x**19])

#коэффциенты регулиризации 
lam = np.array([10**-11, 10**-10, 10**-7, 10**-5,10**-4, 10**-3, 10**-2, 10**-1, 0.5, 1, 5, 10, 50, 10**2, 500, 10**3, 1500, 10**4])

#лучшие значения
lam_best = 0
w_best = 0
basic_func_best = 0
#цикл 
for i in range(rounds):
    basic_func_cur = np.random.choice(basic_func, np.random.randint(len(basic_func)), replace = False)
    lam_cur = np.random.choice(lam)
    design_matrx_cur = calc_design_matrix(x_train, basic_func_cur)
    #вычисляем параметры на обучающей выборке
    w_cur = calc_w(x_train, t_train, lam_cur, basic_func_cur)
    #вычисляем ошибку на валидационной выборке
    E_cur = calc_E(x_valid, t_valid, w_cur, basic_func_cur)
    #флаг для сохранения нового минимального значения ошибки 
    save = E_cur < E_min
    #отметим текущие значения, как лучшие
    if(save):
        E_min = E_cur
        lam_best = lam_cur
        w_best = w_cur
        basic_func_best = basic_func_cur
#ошибка на тестовой выборке
E_best = calc_E(x_test, t_test, w_best, basic_func_best)
print('------ошибка-----')
print(E_best)
print('-------базисные функции--')
print(basic_func_best)
print('------коэффициент регулиризации-------')
print(lam_best)
print('------------------')
#далее находим у(x,w)
design_matrix_on_whole_x = calc_design_matrix(x, basic_func_best)
y = design_matrix_on_whole_x @ w_best.T

figure = plt.figure()
g = figure.subplots()
#график z(x) в виде непрерывной прямой чёрного цвета
g.plot(x, z, 'k')
#график t(x) в виде красных точек
g.scatter(x, t, c = 'r', s = 1)
#график y(x) в виде непрерывной прямой синего цвета
g.plot(x, y, 'b')
plt.show()
