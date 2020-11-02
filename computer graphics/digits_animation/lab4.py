import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg.exe'

def draw_line(x1, y1, x2, y2):
    #проекция на ось икс
    dx = x2 - x1
    #проекция на ось игрек
    dy = y2 - y1

    #функция sign(x)
    #Определяем, в какую сторону нужно будет сдвигаться.
    #Если dx < 0, т.е. отрезок идёт справа налево по иксу,
    #то sign_x будет равен -1. Аналогично с sign_y
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    #далее мы будем сравнивать: "if dx < dy", поэтому берём модуль
    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    #Если dx > dy, то значит отрезок "вытянут" вдоль оси икс,
    #т.е. он скорее длинный, чем высокий.
    #Значит в цикле нужно будет идти по икс (errlen = dx;),
    #значит "протягивать" прямую по иксу надо в соответствии с тем,
    #слева направо и справа налево она идёт (pdx = sign_x;), при этом по y сдвиг такой отсутствует.
    if dx > dy:
        pdx, pdy = sign_x, 0
        errst, errlen = dy, dx
    #случай, когда прямая скорее "высокая", чем длинная, т.е. вытянута по оси y
    #тогда в цикле будем двигаться по y (errlen=dy)
    else:
        pdx, pdy = 0, sign_y
        errst, errlen = dx, dy

    x, y = x1, y1

    #t - итерационная переменная
    error, t = errlen/2, 1

    img[y, x, 0] = 255

    while t < errlen:
        error -= errst
        if error < 0:
            error += errlen
            #сдвинуть прямую (сместить вверх или вниз, если цикл проходит по иксам)
            x += sign_x
            #или сместить влево-вправо, если цикл проходит по y
            y += sign_y
        else:
            #продолжить тянуть прямую дальше, т.е. сдвинуть влево или вправо
            x += pdx
            #если цикл идёт по иксу; сдвинуть вверх или вниз, если по y
            y += pdy
        t += 1
        #красим
        img[y, x, 0] = 255

def work(p):
    t_arr = np.linspace(0, 1, 21)
    for i in range(len(p)):
        for t in t_arr:
            c = p[i]*(1 - t) + p[(i + 1) % len(p)]*t
            d_c = digit_coords(c)
            d_c[:, 0] += delta_x
            d_c[:, 1] += delta_y
            draw_digit((d_c).astype(np.int32))         

def digit_coords(p_arr):
    #вычисляем координаты кривых
    x = []
    t_arr =  np.linspace(0, 1, 101)
    for i in range(0, len(p_arr) - 3, 4):
        for t in t_arr:
            x.append(((1-t)**3) * p_arr[i] + 3*((1-t)**2)*t*p_arr[i + 1] + 3*(1-t)*(t**2)*p_arr[i + 2] + (t**3)*p_arr[i + 3])
    matrix = np.array(x)
    return matrix

def read(file_name):
    with open(file_name, 'r') as f:
        digits = json.load(f)
    return digits    

def ctrl_coords(dict, num):
    #считываем сегменты цифры
    points = []
    for i in range(4):
        for j in range(4):
            points.append(dict['digit_{}'.format(num)]['segment_{}'.format(i)][j])
    return np.array(points)

def draw_digit(coords):
    #идем по матрице
    for i in range(len(coords) - 1):
        draw_line(coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1])
    frame = plt.imshow(img)
    img[:,:,:] = 0
    frames.append([frame])

if __name__ == '__main__':
    #читаем json
    digits = read('digits.json')
    #размер полотна
    size = 1000
    center = size // 2
    figure = plt.figure()
    #полотно
    img = np.zeros((size, size, 3), np.uint8)
    frames = []
    #вот здесь у меня матрица с контрольными точками
    points = []
    for i in range(10):
        points.append(ctrl_coords(digits, i))
    #здесь я центрировал и вычислил координаты кривых
    points = np.array(points)
    x_center, y_center = np.mean(np.mean(points, axis=1), axis=0)
    delta_x = center - x_center
    delta_y = center - y_center
    
    work(points)

    #gif animation creation
    ani = animation.ArtistAnimation(figure, frames, interval=40, blit=True, repeat_delay=0)
    writer = PillowWriter(fps=24)
    ani.save("digits.gif", writer=writer)
    print('[+] Saving in gif format completed!')
    plt.show()
