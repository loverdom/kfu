#include <iostream>
#include <Windows.h>

using namespace std;

DWORD WINAPI threadfunc(LPVOID lpParam);

int* a;

//структура хранящая индексы передаваемых в ф-ию потока элементов последовательности
struct mydata {
	int first_index, second_index;
};

int main()
{
	srand(GetTickCount64());
	cout << "n = ";
	int n;
	cin >> n;
	a = new int[n];
	cout << "-----Source sequence-----\n";
	for (int i = 0; i < n; i++) {
		a[i] = rand() % 101;
		cout << a[i] << " ";
	}
	cout << endl;

	cout << "-----Process-----\n";
	
	//массив для потоков
	HANDLE* threadarr = new HANDLE[n / 2];
	//массив для устройств
	mydata* temp = new mydata[n / 2];
	
	for (int phase = 1; phase < n; phase += phase) {
		//фаза 1-1 на выходе даёт сортированную 
		//последовательность длины 2
		int out_seq_len = phase + phase;
		//ведём счётчик устройств
		int count = 0;
		//далее цикл идёт по длине устройств
		for (int len = phase; len > 0; len = len / 2) {
			//step - расстояние до следующего устройства
			int step = len + len;
			//идём по устройствам
			for (int first_input = len % phase; first_input + len < n; first_input = first_input + step) {
				// шаги(смещения) внутри одного шага
				for (int bias = 0; bias < len; bias++) {
					//проверяем на сравнимость
					//&& first_input + bias + len < n условие позволяет работать с n если оно не степень двойки
					if ((first_input + bias) / out_seq_len == (first_input + bias + len) / out_seq_len && first_input + bias + len < n) {
						temp[count].first_index = first_input + bias;
						temp[count].second_index = temp[count].first_index + len;
						//передаём указатель на начало массива + номер в массиве   
						threadarr[count] = CreateThread(0, 0, threadfunc, (LPVOID)(temp + count), 0, 0);
						count++;
					}
				}
				
			}
			//ожидаем завершение всех потоков
			WaitForMultipleObjects(count, threadarr, TRUE, INFINITE);
			for (int i = 0; i < count; i++) CloseHandle(threadarr[i]);
			//устройства одной длины закончились => обнуляем счётчик
			count = 0;
				
		}
	}
	

	cout << "-----Sorted sequnce-----\n";
	for (int i = 0; i < n; i++) cout << a[i] << " ";
	
	delete[]a;
	delete[]temp;
	delete[]threadarr;

}


DWORD WINAPI threadfunc(LPVOID lpParam) {
	
	mydata* post = (mydata*)lpParam;
	printf("%2d(wire%2d) and %2d(wire%2d)\n", a[post->first_index], post->first_index, a[post->second_index], post->second_index);
	if (a[post->first_index] > a[post->second_index])
		swap(a[post->first_index], a[post->second_index]);
	return 0;
}
