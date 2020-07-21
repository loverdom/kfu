import numpy as np
import matplotlib.pyplot as plt



N = 1000

mu_0 = 180
mu_1 = 193

sigma_0 = 6
sigma_1 = 7

soccer = sigma_0*np.random.randn(N) + mu_0
basketball = sigma_1*np.random.randn(N) + mu_1

soccer_mark = np.zeros(N)
basketball_mark = np.ones(N)

maximum = 0
recall_list = []
alpha_list = []
t_best = 0


def TP(basketball_mark):
    return (np.sum(basketball_mark))

def TN(soccer_mark):
    return (N - np.sum(soccer_mark))

def FP(soccer_mark):
    return np.sum(soccer_mark)

def FN(basketball_mark):
    return (N - np.sum(basketball_mark))

def Accuracy(TP, TN):
    return ((TP + TN)/(2*N))
    
def Precision(TP, FP):
    if TP + FP == 0:
        return 1
    else:
        return (TP/(TP + FP))

def Recall(TP, FN):
    if TP + FN == 0:
        return 1
    else:
        return (TP/(TP + FN))   
    
def F1(Precision, Recall):
    if Precision == 0 and Recall == 0:
        return None
    else:
        return (2*(Precision*Recall)/(Precision+Recall))
    
def alpha(FP, TN):
    if FP + TN == 0:
        return 0
    else:
        return (FP/(FP + TN))

    
def beta(FN, TP):
    return (FN/(FN + TP))
    


def classfication(T):
    for i in range(0, N):
        if basketball[i] > T:
            basketball_mark[i] = 1
        if soccer[i] < T:
            soccer_mark[i] = 0
        if basketball[i] < T:
            basketball_mark[i] = 0
        if soccer[i] > T:
            soccer_mark[i] = 1                 


def print_metrics(t_best):
    classfication(t_best)
    tp = TP(basketball_mark)
    tn = TN(soccer_mark)
    fp = FP(soccer_mark)
    fn = FN(basketball_mark)
    print("---t---")
    print(t_best)
    print("---true positive---")
    print(tp)
    print("---false positive---")
    print(fp)
    print("---true negative---")
    print(tn)
    print("---false negative---")
    print(fn)
    print("---accuracy---")
    print(maximum)
    print("---Precision---")
    print(Precision(tn, fp))
    print("---Recall---")
    print(Recall(tp, fn))
    print("---F1 score---")
    print(F1(Precision(tp, fp), Recall(tp, fn)))
    print("---alpha---")
    print(alpha(fp, tn))
    print("---beta---")
    print(beta(fn, tp))
    print("---area under curve---")
    print(AUC(recall_list, alpha_list))
 
    
def AUC(recall_list, alpha_list):
    auc = 0
    for i in range(1, 300):
        auc += 0.5*(recall_list[i]+recall_list[i-1])*np.abs(alpha_list[i]-alpha_list[i-1])
    return auc

for i in range(300):
    classfication(i)
    acc = Accuracy(TP(basketball_mark), TN(soccer_mark))
    if maximum < acc:
        maximum = acc
        t_best = i
    recall_list.append(Recall(TP(basketball_mark), FN(basketball_mark)))
    alpha_list.append(alpha(FP(soccer_mark), TN(soccer_mark)))          
        
        
print_metrics(t_best)      
x = np.linspace(0,1)
y = x
figure = plt.figure()
g = figure.subplots()
g.plot(alpha_list, recall_list, 'y')
g.plot(x, y, '--')
plt.show()

