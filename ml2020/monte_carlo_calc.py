import numpy as np
import matplotlib.pyplot as plt

#количество точек
print('Введите количество точек: ')
S=int(input())

#шаг
step = S/500
if step < 1:
    step=1

#генерируем точки внутри квадрата 1х1 ((x,y))
shevchuk = np.random.rand(S, 2)

#массив с количеством точек для вычисления
ddt = np.arange(10,S,int(step))

#список вычисленных значений из выборки
zemfira = []

#переменная для временного хранения вычисленных значений
monetochka = 0

#списки с координатами точек внутри окружности
X_red = []
Y_red = []

#списки с координатами точек вне окружности
X_blue = []
Y_blue = []

figure=plt.figure()        

#вычисление Пи методом Монте-Карло
def montecarlo(s):
    temp = 0
    for i in range(0, s):
        if ((shevchuk[i][0] - 0.5)**2 + (shevchuk[i][1] - 0.5)**2) < 0.25:
            temp = temp+1

    return 4*temp / s 

print('Абсолютная погрешность: ')
print(str((np.abs(montecarlo(S)-np.pi)/np.pi)*100) + ' %')

#график зависимости
for i in range(0, ddt.size):
    monetochka = montecarlo(ddt[i])
    zemfira.append(monetochka)

g1 = figure.add_subplot(1, 2, 2)
g1.plot(ddt,zemfira)

#красный круг в синем квадрате
for i in range(S):
    if ((shevchuk[i][0] - 0.5)**2 + (shevchuk[i][1] - 0.5)**2) < 0.25:
        X_red.append(shevchuk[i][0])
        Y_red.append(shevchuk[i][1])
    else:
        X_blue.append(shevchuk[i][0])
        Y_blue.append(shevchuk[i][1])

g2 = figure.add_subplot(1, 2, 1)        
g2.scatter(X_red, Y_red, c='r', s=1)
g2.scatter(X_blue, Y_blue, c='b', s=1)
red = plt.Circle((0.5, 0.5), 0.5, fill=False)
blue = plt.Polygon([(0, 0), (0, 1), (1, 1), (1, 0)], fill=False)

          
plt.show()
