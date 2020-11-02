import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg.exe'


# функция считывания в матрицы
def to_matrix(filename):
    f_list = []
    v_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            # делаем из строки список
            line = line.split(' ')
            if 'v' in line:
                # буквы v и f нам ни к чему, поэтому срезаем их
                v_list.append(line[1:3])
            if 'f' in line:
                f_list.append(line[1:])
    f_matrix = np.array(f_list, dtype=np.int32)
    v_matrix = np.array(v_list, dtype=np.float64)
    return f_matrix, v_matrix

def bres(x1, y1, x2, y2, col):
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
    error, t = errlen/2, 0


    img[y, x, :] = col


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
        img[y, x, :] = col


def draw_triangle(a, b, c, col = 0):
    bres(a[0], a[1], b[0], b[1], col)
    bres(b[0], b[1], c[0], c[1], col)
    bres(c[0], c[1], a[0], a[1], col)


def draw_teapot(v_matrix, f_matrix, col = 0):
    for line in f_matrix:
        draw_triangle(v_matrix[line[0] - 1], v_matrix[line[1] - 1], v_matrix[line[2] - 1], col)

def shiftMatr(vec):
    mtr = np.array([[1, 0, vec[0]], [0, 1, vec[1]], [0, 0, 1]])
    return mtr

def rotMatr(ang):
    mtr = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    return mtr

def to_proj_coords(x):
    _, c = x.shape
    x = np.concatenate([x, np.ones((1, c))], axis = 0)
    return x

def to_cart_coords(x):
    x = x[:-1] / x[-1]
    return x

def diagMatr(coef):
    mtr = np.array([[coef, 0, 0],[0, coef, 0], [0, 0, 1]])
    return mtr    

def to_pos_and_inc(v_matrix):
    #смещаем иксы и их отображения в положительный квадрант
    x_min_abs = np.fabs(v_matrix[:, 0].min())    
    v_matrix[:, 0] += x_min_abs
    v_matrix[:, 1] *= -1
    y_min_abs = np.fabs(v_matrix[:, 1].min())
    v_matrix[:, 1] += y_min_abs
    
    #увеличиваем размер чайника и приводим координаты в целочисленному типу
    v_matrix = (v_matrix * 150).astype(np.int32)
    return v_matrix

if __name__ == "__main__":
    start_time = time.time()
    file_name = "teapot.obj"
    f_matrix, v_matrix = to_matrix(file_name)
    v_matrix = to_pos_and_inc(v_matrix)
    
    #кол-во кадров
    frames_count = 100
    #граница смены
    zone = frames_count 
    #список с раскадровкой
    frames = []
    #для смены цвета
    red_to_green = np.array(np.linspace(255, 0, zone, dtype=np.int32))
    green_to_red = np.array(np.linspace(0, 255, zone, dtype=np.int32))    
    color = np.array(np.concatenate((np.concatenate((red_to_green, green_to_red)).reshape(-1, 1), np.concatenate((green_to_red, red_to_green)).reshape(-1, 1), np.zeros(2*frames_count).reshape(-1, 1)), axis=1))
   
    #координаты центра чайника
    x_center, y_center = np.mean(v_matrix, axis=0, dtype=np.int32)

    from_big_to_norm = np.linspace(2, 1, zone)
    from_norm_to_big = np.linspace(1, 2, zone)

    #коэффициенты для А
    coef = np.concatenate((from_norm_to_big, from_big_to_norm))

    #создаем холст
    #img = np.zeros((np.max(v_matrix[:, 1]) + 1, np.max(v_matrix[:, 0]) + 1, 3), np.uint8)
    #img[:, :, :] = 0
    #figure1 = plt.figure()
    #draw_teapot(v_matrix, f_matrix, 255)
    
    #красным обозначим центр чайника
    #img[y_center - 10:y_center + 10,x_center - 10:x_center + 10] = [255, 0, 0]
    #plt.imshow(img)
    #plt.show()

    #размер для кадров
    frame_body = 2500
    frame_body_center = frame_body // 2
    #величина смещения к центру 
    x_to_frame_center = frame_body_center - x_center
    y_to_frame_center = frame_body_center - y_center

    v_matrix[:, 0] += x_to_frame_center
    v_matrix[:, 1] += y_to_frame_center
    
    center = np.array([frame_body_center, frame_body_center])

    #матрица возврата в центр
    T = shiftMatr(-center)

    #приводим к матрицу координат виду:
    # / x1 x2 ... xn \                
    # \ y1 y2 ... yn /
    X = v_matrix.T

    #переходим к проективным координатам
    X_proj = to_proj_coords(X)

    figure = plt.figure()
    for i in range(2*frames_count):
        ang = i * 4 * np.pi / frames_count
        A = diagMatr(coef[i])
        R = rotMatr(ang)
        img = np.zeros((frame_body, frame_body, 3), dtype=np.uint8)

        X_proj_new = np.linalg.inv(T) @ A @ R @ T @ X_proj

        X_new = to_cart_coords(X_proj_new)
        X_new = np.int32(np.round(X_new.T))
        draw_teapot(X_new, f_matrix, color[i])

        frame = plt.imshow(img)
        frames.append([frame])

    print('[+] frames creation finished!')
    print('[|] Saving in gif format started')     
    #gif animation creation
    ani = animation.ArtistAnimation(figure, frames, interval=40, blit=True, repeat_delay=0)
    writer = PillowWriter(fps=24)
    ani.save("teapot.gif", writer=writer)
    print('[+] Saving in gif format completed!')
    print("Runtime:")    
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()


    
