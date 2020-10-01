import numpy as np
import matplotlib.pyplot as plt
import sys


# функция считывания в матрицы
def to_matrix(filename):
    verge_list = []
    apex_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            # делаем из строки список
            line = line.split(' ')
            if 'v' in line:
                # буквы v и f нам ни к чему, поэтому срезаем их
                apex_list.append(line[1:3])
            if 'f' in line:
                verge_list.append(line[1:])
    verge_matrix = np.array(verge_list, dtype=np.int32)
    apex_matrix = np.array(apex_list, dtype=np.float64)
    return verge_matrix, apex_matrix


def draw_line(x1, y1, x2, y2, background):

    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx>0 else -1 if dx<0 else 0
    sign_y = 1 if dy>0 else -1 if dy<0 else 0

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el/2, 0

    background[-y - 1024, -x - 1024, :] = 255

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        background[-y - 1024, -x - 1024, :] = 255


def draw_teapot(apex_matrix, verge_matrix, background):
    for line in verge_matrix:
        x1 = apex_matrix[line[0] - 1][0]
        y1 = apex_matrix[line[0] - 1][1]
        x2 = apex_matrix[line[1] - 1][0]
        y2 = apex_matrix[line[1] - 1][1]
        draw_line(x1, y1, x2, y2, background)
        x1 = x2
        y1 = y2
        x2 = apex_matrix[line[2] - 1][0]
        y2 = apex_matrix[line[2] - 1][1]
        draw_line(x1, y1, x2, y2, background)
        x1 = x2
        y1 = y2
        x2 = apex_matrix[line[0] - 1][0]
        y2 = apex_matrix[line[0] - 1][1]
        draw_line(x1, y1, x2, y2, background)

    plt.figure()
    plt.imshow(background)
    plt.show()
    plt.imsave('the_utah_teapot.png', background)

def main():
    file_name = sys.argv[1]
    v_matrix, a_matrix = to_matrix(file_name)
    background = np.zeros((2048, 2048, 3), dtype=np.uint8)
    draw_teapot((a_matrix*270).astype(np.int32), v_matrix, background)


if __name__ == "__main__":
    main()
