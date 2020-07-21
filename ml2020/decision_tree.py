import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import numpy as np

#функция вывода гистограмм
def g(for_ax1, for_ax2, for_ax3, for_ax4):   
    fig1, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize=(8, 4))
    fig2, (ax3, ax4) = plt.subplots(nrows = 1, ncols = 2, figsize=(8, 4))


    ax1.set_title('Correct on train set')
    ax1.hist(for_ax1, color = 'y')

    ax2.set_title('Incorrect on train set')
    ax2.hist(for_ax2, color = 'k')

    ax3.set_title('Correct on test set')
    ax3.hist(for_ax3, color = 'k')

    ax4.set_title('Incorrect test set')
    ax4.hist(for_ax4, color = 'y')
    plt.show()

#функция перемешивания и деления датасета
def shuffle(x, t):
    ind = np.arange(np.int64(len(x)))
    np.random.shuffle(ind)
    ind_train = ind[:np.int64(0.8*len(ind))]
    ind_test = ind[np.int64(0.8*len(ind)):]
    x_train = x[ind_train, :]
    x_test = x[ind_test, :]
    t_train = t[ind_train]
    t_test = t[ind_test]
    return x_train, x_test, t_train, t_test

#критерии остановки
def stop(x, t, depth, limit_of_depth, data_amount, entropy_border):
    entr = entropy(t)
    if np.int64(len(x)) >= data_amount\
        and depth != limit_of_depth and entr >= entropy_border:
        return 0
    else:
        return True

#считаем энтропию
def entropy(t):
    H = 0.0
    Ni = t.shape[0]
    Nik = np.unique(t, return_counts=True)[1]
    for k in Nik:
        H += k / Ni * np.log2(k / Ni)
    return -H

#функция деления
def split_data(x, tetta):
    left_ind = []
    right_ind = []
    for i in range(np.int64(len(x))):
        if x[i, tetta[0]] < tetta[1]:
            left_ind.append(i)
        else:
            right_ind.append(i)
    return left_ind, right_ind

#вычисляем information gain
def ig(x, t, left_ind, right_ind):
    parent_entropy = entropy(t)
    left_entropy = entropy(t[left_ind])
    right_entropy = entropy(t[right_ind])
    ig = parent_entropy - ((np.int64(len(x[left_ind])) / np.int64(len(x))) \
                             * left_entropy) - ((np.int64(len(x[right_ind])) / np.int64(len(x)))\
                                               * right_entropy)
    
    return ig

#вычисляем параматеры тетта (пси и тау)
def tetta(x, t):
    best_IG = 0
    psi = 0
    best_tau = 0

    left_ind = []
    right_ind = []

    for bruteforce_x in range(x.shape[1]):
        for bruteforce_tau in range(17):
            for j in range(np.int64(len(x))):
                if x[j, bruteforce_x] < bruteforce_tau:
                    left_ind.append(j)
                else:
                    right_ind.append(j)
            IG = ig(x, t,  left_ind, right_ind)
            right_ind.clear()
            left_ind.clear()
            if IG > best_IG:
                best_IG = IG
                psi = bruteforce_x
                best_tau = bruteforce_tau
    return psi, best_tau

#создаём терминальный узел
def terminal_node(t):
    Ni = t.shape[0]
    assure_vector= np.ones(10)
    for i in range(10):
        assure_vector[i] = np.int64(len(t[t == i])) / Ni

    return {'is_terminal': True, 'assure': assure_vector}

#создаем разделяющий узел
def split_node(tetta):
    node = {}
    node['psi'] = tetta[0]
    node['tau'] = tetta[1]
    node['left'] = None
    node['right'] = None
    node['is_terminal'] = False
    return node

#создаём дерево
def tree(x, t, depth, limit_of_depth, data_amount, entropy_border):
    if not stop(x, t, depth, limit_of_depth, data_amount, entropy_border):
        tetta_arr = tetta(x, t)
        left, right = split_data(x, tetta_arr)
        node = split_node(tetta_arr)
        depth += 1
        node['left'] = tree(x[left], t[left], \
            depth, limit_of_depth, data_amount, entropy_border)

        node['right'] = tree(x[right], t[right], depth, \
            limit_of_depth, data_amount, entropy_border)
    else:
        node = terminal_node(t)
    return node

#считаем метрики
def metrics(x, t, node):
    confusion_matrix = np.zeros((10, 10))
    matrix = np.zeros((x.shape[0], 10))

    for i in range(x.shape[0]):
        matrix[i] = np.array(solve(x[i], node))
    for j in range(matrix.shape[0]):
        confusion_matrix[t[j]][np.argmax(matrix[j])] += 1
    
    correct = []
    incorrect = []
    for i in range(x.shape[0]):
        if t[i] == np.argmax(matrix[i]):
            correct.append(np.amax(matrix[i]))
        else:
            incorrect.append(np.amax(matrix[i]))
    count = 0  
    for i in range(confusion_matrix.shape[0]):
        count += confusion_matrix[i][i]
    
    accuracy = count / matrix.shape[0]    
        
    return confusion_matrix, correct, incorrect, accuracy

#дерево решений
def solve(Si, node):
    if not node['is_terminal']:
        if Si[node['psi']] < node['tau']:
            return solve(Si, node['left'])
        else:
            return solve(Si, node['right'])
    else:
        return node['assure']


digits = load_digits()

x_train, x_test, t_train, t_test = shuffle(digits.data, digits.target)
depth = 0
limit_of_depth = 35
data_amount = 35
entropy_border = 0.1

tree = tree(x_train, t_train, depth, limit_of_depth, data_amount, \
                                                            entropy_border)

confusion_matrix_train, for_ax1, for_ax2, accuracy_train \
                                = metrics(x_train, t_train, tree)
confusion_matrix_test, for_ax3, for_ax4, accuracy_test =\
                                     metrics(x_test, t_test, tree)

print("-----TRAIN-----")
print("------Confusion matrix for train set------")
print(confusion_matrix_train)
print("------accuracy on train set------")
print(accuracy_train)
print("-----TEST-----")
print("------Confusion matrix for test set------")
print(confusion_matrix_test)
print("------accuracy on test set------")
print(accuracy_test)
print("-----GRAPHICS-----")
g(for_ax1, for_ax2, for_ax3, for_ax4)
print("-----THE END-----")
