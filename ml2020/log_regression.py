import numpy as np
import matplotlib.pyplot as plt

#функция с выводом графиков при M равным 2, 8 , 100
def first_g(M):
    #матрица плана (матрица из базисных функций)
    design_matrix = np.zeros((N, M))
    
    #заполняем матрицу плана (полиномиальная регрессия)
    for i in range(M):
        design_matrix[:, i] = x**i
        
    #параметры модели
    w = np.linalg.inv(design_matrix.T@design_matrix)@design_matrix.T@t
    
    #линейная комбинация нелинейных базисных функций от входных переменных
    y = design_matrix @ w.T    
    
    #графическое окно
    figure1 = plt.figure()
    g1 = figure1.subplots()
    g1.scatter(x, t, c = 'r', s = 1/2)
    g1.scatter(x, z, c = 'b', s = 1/5)
    g1.scatter(x, y, c = 'k', s = 1/2)
    
    plt.show()
    




#размер обучающей выборки
N = 1000

#входные переменные
x = np.linspace(0, 1, N)

#то, что в целевой переменной нам подвластно
z = 20 * np.sin(2 * np.pi * 3 * x) + 100 * np.exp(x)

#то, что в целевой переменной нам неподвластно
error = 10 * np.random.randn(N)

#целевые переменные
t = z + error

#степени полинома (1, 2, 3, ...)   
deg = np.arange(1, 100)

#храним значения функции потери E(w)
e = []



first_g(2)
first_g(8)
first_g(100)


e = []
    
#степень полинома меняется от 1 до 100
for i in range (1,100):   
    #M меняется        
    design_matrix2 = np.zeros((N,i))        
    #заполняем в соотвествии с размером
    for j in range(i):
        design_matrix2[:,j] = x**j
        
    #переменная для временного хранения вычисленного значения функции потери
    temp=0        
    #параметры модели
    w2 = np.linalg.inv(design_matrix2.T@design_matrix2)@design_matrix2.T@t        
    #линейная комбинация нелинейных базисных функций от входных переменных
    y2 = design_matrix2 @ w2.T   
    #вычисление значений E(w)
    for n in range(N):
        temp += 1/2 * (y2[n]-t[n])**2
        
    #заносим вычиленное в список    
    e.append(temp)
     
#графическое окно
figure2 = plt.figure()
g2 = figure2.subplots()
g2.plot(deg, e)
plt.show()  
