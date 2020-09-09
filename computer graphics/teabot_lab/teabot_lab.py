#!/usr/bin/env python3
import numpy as np
import sys

#функция считывания в матрицы
def to_matrix(filename):
    verge_list = []
    apex_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            #делаем из строки список
            line = line.split(' ')
            if 'v' in line:
                #буквы v и f нам ни к чему, поэтому срезаем их
                apex_list.append(line[1:])
            if 'f' in line:
                verge_list.append(line[1:])
    verge_matrix = np.array(verge_list, dtype = np.int32)
    apex_matrix = np.array(apex_list, dtype = np.float64)
    return verge_matrix, apex_matrix

def tri_square(a, b, c):
    #площадь через определитель
    s = 0.5*np.abs((a[0] - c[0])*(b[1] - c[1]) - (b[0] - c[0])*(a[1] - c[1]))
    return s

def total_area(a_matrix, v_matrix):
    list_of_amounts = []
    for line in v_matrix:
        list_of_amounts.append(tri_square(a_matrix[line[0] - 1], a_matrix[line[1] - 1],\
                                          a_matrix[line[2] - 1]))
    total_area = np.sum(list_of_amounts)
    return total_area


def main():
    #sys.argv[0] имя нашего файла .py
    file_name = sys.argv[1]
    verge_matrix, apex_matrix = to_matrix(file_name)
    area = total_area(apex_matrix, verge_matrix)
    print("|" + 45*"-")
    print("|" + "First point of lab:")
    print("|" + "[+] Amount of apexes = {}".format(apex_matrix.shape[0]))
    print("|" + "[+] Amount of verges = {}".format(verge_matrix.shape[0]))
    print("|" + 45*"-")
    print("|" + "Second point of lab:")
    print("|" + "[+] Max of 'x' = {0} and min of 'x' = {1}".format(np.max(apex_matrix[:, 0]), \
                                                             np.min(apex_matrix[:, 0])))
    print("|" + "[+] Max of 'y' = {0} and min of 'y' = {1}".format(np.max(apex_matrix[:, 1]), \
                                                             np.min(apex_matrix[:, 1])))
    print("|" + "[+] Max of 'z' = {0} and min of 'z' = {1}".format(np.max(apex_matrix[:, 2]), \
                                                             np.min(apex_matrix[:, 2])))
    print("|" + 45*"-")
    print("|" + "Third point of lab:")
    print("|" + "[+] Total area of teapot: {}".format(area))
    print("|" + 45*"-")

if __name__ == "__main__":
    main()
