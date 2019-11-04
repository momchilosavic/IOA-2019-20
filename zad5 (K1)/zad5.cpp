// IOA zad3.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <stdio.h>
#include <time.h>
#include <vector>

#define N 29


static double timeCnt;
static long cntr;
static long min = LONG_MAX;
static long T[] = { 27257, 11737, 3417, 74732055, 7008769, 71198, 6970, 8602, 74787,
		3485, 97291, 61981162, 1938, 8551, 8051, 65105553, 8228, 10217603,
		23728483, 72114322, 4896, 85845, 6014, 84696329, 47142, 41039298, 2159,
		5235466, 82838 };
static long totalSum = 0;

void swap(long P[], int i, int j) {
	long tmp = P[i];
	P[i] = P[j];
	P[j] = tmp;
}

void comb(int n, int k){
	int i;
	int j = k;
	int* c = new int[k];
	for (i = 0; i < k; i++)
		c[i] = j--;

	while (true)
	{
		/*****/
		cntr++;
		long sumA = 0;
		long sumB = 0;
		for (i = k;i--;) {
			//printf("%d%c", c[i], i ? ' ': '\n');
			sumA += T[c[i]-1];
		}
		
		long nMin = abs(sumA - (totalSum - sumA));
		if (nMin == 0 || nMin < min) {
			min = nMin;
			printf("\nRazlika: %d", min);
			printf("\nSuma niza A: %d", sumA);
			printf("\nA: ");
			for (i = k; i--;) {
				printf("%d ", T[c[i]-1]);
			}
		}
		/*****/

		i = 0;
		if (c[i]++ < n) continue;

		for (; c[i] >= n - 1;)
			if (++i >= k)
				return;
		for (c[i]++; i; i--)
			c[i - 1] = c[i] + 1;
	}

	delete[] c;
}

int main()
{
	for (int i = 0; i < N;i++)
		totalSum += T[i];
	timeCnt = clock();
	cntr = 0;
	min = LONG_MAX;
	for(int i = 1; i <= 14; i++)
		comb(29, i);
	printf("\n\nItrations: %d", cntr);
	printf("\nTime: %.2fs\n", ((double)clock() - timeCnt)/CLOCKS_PER_SEC);
	return 0;
}