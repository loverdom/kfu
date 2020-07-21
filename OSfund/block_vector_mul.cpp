#include <Windows.h>
#include <iostream>

//замещаем BUF_SIZE на 255 во всём коде
#define BUF_SIZE 255

using namespace std;
//размер матрицы и q - насколько частей делится вектор-результат
int n, m, q;
//матрица, вектор-множитель, вектор-результат
int** matrix, * vector, * result;

//функция потока
DWORD WINAPI threadfunc(LPVOID lpParam);
//мютексы
HANDLE* mutexArr;


int main() {
	srand(GetTickCount64());
	cout << "m: ";
	cin >> m;
	cout << "n: ";
	cin >> n;
	cout << "q (q <= 8): ";
	cin >> q;
	cout << "---MATRIX(m x n)---" << endl;

	matrix = new int* [m];
	for (int i = 0; i < m; i++)
		matrix[i] = new int[n];

	vector = new int[n];
	result = new int[m];

	//во избежании мусора, заполняем нулями
	for (int i = 0; i < m; i++)
		result[i] = 0;

	//printf для читабельного вывода матрицы
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			matrix[i][j] = rand() % 21 - 10;
			printf("%4d", matrix[i][j]);
		}
		cout << endl;
	}

	cout << "---VECTOR---" << endl;
	for (int i = 0; i < n; i++){
		vector[i] = rand() % 21 - 10;
		printf("%4d\n", vector[i]);
	}
	cout << "---PROCESS---" << endl;
	mutexArr = new HANDLE[q];


	for (int i = 0; i < q; i++)
		//параметры (дескриптор безопасности по-умолчанию, без первоначального владельца, без имени)
		mutexArr[i] = CreateMutex(NULL, FALSE, NULL);

	HANDLE* threadArr = new HANDLE[q * q];

	for (int i = 0; i < q * q; i++)
		threadArr[i] = CreateThread(NULL, 0, threadfunc, (LPVOID)i, 0, 0);

	WaitForMultipleObjects(q*q, threadArr, TRUE, INFINITE);
	
	//закрываем потоки и мютексы
	for (int i = 0; i < q * q; i++)
		CloseHandle(threadArr[i]);
	for (int i = 0; i < q; i++)
		CloseHandle(mutexArr[i]);

	cout << "---RESULT---" << endl;
	for (int i = 0; i < m; i++) {
		printf("%d ", result[i]);
	}

	//очистка памяти
	for (int i = 0; i < m; i++)
		delete[]matrix[i];

	delete[] matrix;
	delete[] threadArr;
	delete[] mutexArr;
	delete[] vector;
	delete[] result;
	return 0;
}

DWORD WINAPI threadfunc(LPVOID lpParam) {
	//буфер
	char message[BUF_SIZE];

	int ind = int(lpParam);
	//промежуточный вектор
	int* piece;
	
	//сохраняем кол-во записанных байтов
	int info;

	//размер блока
	int block_rows = m / q;
	int block_col = n / q;

	piece = new int[block_rows];

	//во избежании мусора, заполняем нулями
	for (int i = 0; i < m / q; i++)
		piece[i] = 0;

	// ind/q "координата" блока по верткали 
	// ind%q "координата" блока по горизонтали 
	int i_height = ind / q * block_rows;
	int j_width = ind % q * block_col;
	int end_height = i_height + block_rows;
	int end_width = j_width + block_col;

	//умножаем блок на соответсвующую часть вектора-множителя
	for (int i = i_height; i < end_height; i++)
		for (int j = j_width; j < end_width; j++)
			piece[i - i_height] += matrix[i][j] * vector[j];
	


	WaitForSingleObject(mutexArr[ind / q], INFINITE);


	for (int i = i_height; i < end_height; i++)
		result[i] += piece[i - i_height];
	ReleaseMutex(mutexArr[ind / q]);







	//sprintf - вывод не в поток, а в буфер
	//sprintf_s - возвращает кол-во записанных байтов
	
	//записываем в буфер
	info = sprintf_s(message, BUF_SIZE, "block: (%d, %d)\n", ind / q, ind % q);
	int t = 0;
	while (t < block_rows)
		//записываем в буфер 
		info += sprintf_s(message + info, BUF_SIZE - info, "%4d\n", piece[t++]);

	//выводим в консоль (формат: строка символов)
	printf_s("\n%s", message);



	delete[] piece;
	return 0;
}
