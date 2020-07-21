#include <iostream>
#include <Windows.h>

using namespace std;

int* A;
int k;
int n;
DWORD WINAPI doubling(LPVOID lpParam);

int main()
{
    srand(GetTickCount64());
    cin >> n;
    A = new int[n];
    cout << "----ARRAY----" << endl;
    for (int i = 0; i < n; i++) {
        //от -10 до 10 генерируем числа
        A[i] = rand() % 21 - 10;
        cout << A[i] << ' ';
    }
    cout << endl;

    //размер сумиируемого массива сначала равен длине исходного массива
    k = n;
    

    cout << "----PROCESS----" << endl;
    //складываем, пока не дойдём до суммы элементов с индексами 0 и 1
    while (k > 1) {
        //выделяем память под необходимое количество потоков
        HANDLE* threadArr = new HANDLE[k / 2 ];
        //создаём потоки и передаём аргументом 
        for (int i = 0; i < k / 2; i++) {
            threadArr[i] = CreateThread(NULL, 0, doubling, (LPVOID)i, 0, NULL);
        }
        //ждем завершения работы потоков
        WaitForMultipleObjects(k / 2, threadArr, TRUE, INFINITE);
        
        //в случае, когда подмассив будет иметь нечётное кол-во элементов
        //if (k % 2 != 0 && k != 1)
        //    A[0] += A[k - 1];
        
        //закрываем потоки
        for (int i = 0; i < k / 2; i++)CloseHandle(threadArr[i]);
        
        //каждый шаг сокращаем число слагаемых вдвое (для нечётного кол-ва левый подмассив будет больше и элемент "без пары" будет суммироваться)
        k = k - k / 2;
        
        //выводим для демонстрации
        cout << "k:" << k << endl;
        for (int i = 0; i < n; i++)
            cout << A[i] << " ";
        cout << endl << endl;;
        

        //очищаем память, после работы с массивом потоков
        delete[]threadArr;
    }
    //выводим результат
    cout << "----RESULT----" << endl;
    cout <<A[0];
    //очищаем память, после работы с массивом чисел
    delete[] A;
}

DWORD WINAPI doubling(LPVOID lpParam)
{
    int ind = (int)lpParam;         
    //от конца суммируемого массива идём к границе левого подмассива и потом идём к "паре" того элемента, индекс которого мы передали потоку
    A[ind] += A[k - k/2 + ind];
    return 0;
}
