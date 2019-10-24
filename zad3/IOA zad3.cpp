// IOA zad3.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <iomanip>
#include <algorithm>
#include <time.h>

#define N 12

static double minP = DBL_MAX;
static int minR[N];
static double x[N][2];
static double cost[N][N];
static long timeCnt = 0;



double pd(int* r, double c[N][N]) {
	double sum = 0;
	for (int i = 1; i < N; i++) 
		sum += c[r[i-1]-1][r[i]-1];
	return sum;
}


void init() {
	x[0][0] = 62.00;
	x[0][1] = 58.40;
	x[1][0] = 57.50;
	x[1][1] = 56.00;
	x[2][0] = 51.70;
	x[2][1] = 56.00;
	x[3][0] = 67.90;
	x[3][1] = 19.60;
	x[4][0] = 57.70;
	x[4][1] = 42.10;
	x[5][0] = 54.20;
	x[5][1] = 29.10;
	x[6][0] = 46.00;
	x[6][1] = 45.10;
	x[7][0] = 34.70;
	x[7][1] = 45.10;
	x[8][0] = 45.70;
	x[8][1] = 25.10;
	x[9][0] = 34.70;
	x[9][1] = 26.40;
	x[10][0] = 28.40;
	x[10][1] = 31.70;
	x[11][0] = 33.40;
	x[11][1] = 60.50;
	/*x[12][0] = 22.90;
	x[12][1] = 32.70;
	x[13][0] = 21.50;
	x[13][1] = 45.80;
	x[14][0] = 15.30;
	x[14][1] = 37.80;
	x[15][0] = 15.10;
	x[15][1] = 49.60;
	x[16][0] = 9.10;
	x[16][1] = 52.80;
	x[17][0] = 9.10;
	x[17][1] = 40.30;
	x[18][0] = 2.70;
	x[18][1] = 56.80;
	x[19][0] = 2.70;
	x[19][1] = 33.10;*/

	for(int i = 0; i < N; i++)
		for (int j = 0; j < N; j++) {
			if (i != j)
				cost[i][j] = sqrt(pow(x[i][0] - x[j][0], 2) + pow(x[i][1] - x[j][1], 2));
			else
				cost[i][j] = DBL_MAX;
		}
}


void genPerm(int k, int n, int i, int* P) {
	int q;

	if (k == -1)
		for (q = 0; q < n; q++)
			P[q] = 0;

	P[i] = k + 1;

	// obrada
	if (k == n - 1) {
		double pt = pd(P, cost);
		if (pt < minP) {
			std::cout << "Min: " << pt << " Route: ";
			for (int i = 0; i < N; i++)
				std::cout << P[i] << " ";
			std::cout<< std::endl;
			minP = pt;
			for (int ind = 0; ind < N; ind++)
				minR[ind] = P[ind];
		}
	}
	//

	for (q = 0; q < n; q++)
		if (P[q] == 0)
			genPerm(k + 1, n, q, P);

	P[i] = 0;
}

int main()
{
	timeCnt = clock();
	init();
	std::cout << std::fixed << std::setprecision(2);
	int* P = new int[N];

	genPerm(-1, N, 0, P);

	std::cout << "Time passed: " << ((double)clock() - timeCnt) / CLOCKS_PER_SEC;

	delete[] P;

	std::cout << std::endl;
	return 0;
}