
#include <iostream>
#include "windows.h"
#include <algorithm>
#include <ctime>


using namespace std;

int n, m;
DWORD WINAPI thread(LPVOID lpParam);
int *A, *B, *C;

int main()
{	
	HANDLE* ThreadArr;
	srand(time(NULL));
	cout << "Enter size of the polynom A (n value): ";
	cin >> n;
	A = new int[n + 1];
	for (int i = 0; i < n + 1; i++) {
		 A[i] = 1 + rand()%10;
	}
	cout << "Enter size of polynom B (m value): ";
	cin >> m;
	B = new int[m + 1];
	for (int i = 0; i < m + 1; i++) {
		B[i] = 1 + rand() % 10;
	}
	

	C = new int[m + n + 1];
	ThreadArr = new HANDLE[m + n + 1];

	for (int i = 0; i < n + m + 1; i++) C[i] = 0;
	cout << "A: ";
	for (int i = 0; i < n + 1; i++) {
		cout << A[i] << " ";
	}
	cout << endl;
	cout << "B: ";
	for (int i = 0; i < m + 1; i++) {
		cout<<B[i]<< " ";
	}
	cout << endl;
	for (int i = 0; i < n + m + 1; i++) {
		ThreadArr[i] = CreateThread(NULL, 0, thread, (LPVOID)i, 0, NULL);
	}
		
	WaitForMultipleObjects(n+m+1, ThreadArr, TRUE, INFINITE);
	for (int i = 0; i < n + m + 1; i++)CloseHandle(ThreadArr[i]);
	cout << "C: ";
	for (int i = 0; i < n + m + 1; i++) {
		cout << C[i] << "*x^" << i <<" ";
	}
	
	
	delete[] ThreadArr;
	delete[] A;
	delete[] B;
	delete[] C;

	return 0;
}


DWORD WINAPI thread(LPVOID lpParam)
{
	int k = (int)lpParam;
	for (int i = max(0, k - m); i <= min(n, k); i++) {
		C[k] += A[i] * B[k - i];
	}
	return 0;
}
