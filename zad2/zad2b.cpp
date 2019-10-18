#include <iostream>
#include <vector>
#include <time.h>

using namespace std;

static long TimeCnt = 0;
static long ItCnt = 0;
static long ZBIR = 711;
static long PROIZVOD = 711000000;

/*
* ISPIS CENA PROIZVODA
*/
static void print(int x1, int x2, int x3, int x4) {
	cout
		<< "Prvi proizvod: "
		<< (double)x1 / 100
		<< endl
		<< "Drugi proizvod: "
		<< (double)x2 / 100
		<< endl
		<< "Treci proizvod: "
		<< (double)x3 / 100
		<< endl
		<< "Cetvrti proizvod: "
		<< (double)x4 / 100
		<< endl;
}

/*
* ISPIS BROJA ITERACIJA I PROTEKLOG VREMENA
*/
static void printStat() {
	cout
		<< "Broj iteracija: "
		<< ItCnt
		<< endl;

	cout
		<< "Vreme izvrsavanja: "
		<< ((double)clock() - TimeCnt) / CLOCKS_PER_SEC
		<< endl
		<< endl
		<< endl;
}


void func1(long zbir, long proizvod) {
	TimeCnt = clock();
	ItCnt = 0;

	for (long x1 = 1; x1 < zbir; x1++) {
		for (long x2 = x1; x2 < zbir; x2++) {
			for (long x3 = x2; x3 < zbir; x3++) {
				for (long x4 = x3; x4 < zbir; x4++) {
					ItCnt++;
					if ((x1 + x2 + x3 + x4 > zbir) || (x1 * x2 * x3 * x4) > proizvod)
						break;
					if ((x1 + x2 + x3 + x4 == zbir) && (x1 * x2 * x3 * x4 == proizvod))
						print(x1, x2, x3, x4);
				}
			}
		}
	}
	printStat();
}

void func2(long zbir, long proizvod) {
	TimeCnt = clock();
	ItCnt = 0;

	for (long x1 = 1; x1 < zbir; x1++) {
		for (long x2 = x1; x2 < zbir; x2++) {
			for (long x3 = x2; x3 < zbir; x3++) {
				ItCnt++;
				long x4 = zbir - x1 - x2 - x3;
				if ((x1 * x2 * x3 * x4) > proizvod)
					break;
				if ((x1 * x2 * x3 * x4) == proizvod)
					print(x1, x2, x3, x4);
			}
		}
	}
	printStat();
}

void func3(long zbir, long proizvod) {
	TimeCnt = clock();
	ItCnt = 0;
	vector<long> factors;
	for (int f = 2; f < zbir; f++) {
		if (proizvod % f == 0) {
			factors.push_back(f);
		}
	}
	for (int a = 0; a < (int)factors.size() - 3; a++) {
		for (int b = a + 1; b < (int)factors.size() - 2; b++) {
			for (int c = b + 1; c < (int)factors.size() - 1; c++) {
				for (int d = c + 1; d < (int)factors.size(); d++) {
					ItCnt++;
					if ((factors[a] + factors[b] + factors[c] + factors[d] > ZBIR) || (factors[a] * factors[b] * factors[c] * factors[d] > PROIZVOD))
						break;
					if ((factors[a] + factors[b] + factors[c] + factors[d] == ZBIR) && (factors[a] * factors[b] * factors[c] * factors[d] == PROIZVOD)) {
						print(factors[a], factors[b], factors[c], factors[d]);
					}
				}
			}
		}
	}
	printStat();
}

int main() {
	cout
		<< "--- Prvo resenje ---"
		<< endl
		<< endl;
	func1(ZBIR, PROIZVOD);

	cout
		<< "--- Drugo resenje ---"
		<< endl
		<< endl;
	func2(ZBIR, PROIZVOD);

	cout
		<< "--- Trece resenje ---"
		<< endl
		<< endl;
	func3(ZBIR, PROIZVOD);

	system("pause");
	return 0;
}