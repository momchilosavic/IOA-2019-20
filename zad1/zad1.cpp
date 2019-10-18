#include <iostream>
#include <complex>
#include <stdio.h>

using namespace std;

#define PI atan(1)*4


complex<double> func(int n, double delta, double beta, double d, double teta) {
	complex<double> sum;
	sum.real(0.0);
	sum.imag(0.0);

	complex<double> num;

	double fi = delta + d * beta * cos(teta);

	for (int k = 0; k < n; k++) {
		num.real(cos(-k * fi));
		num.imag(sin(-k * fi));
		sum += num;
	}

	return sum;
}

int main() {
	FILE* out;
	fopen_s(&out, "complex.txt", "w");

	int n = 5;
	double beta = 20 * PI;
	double d = 1 / 20;
	double teta = PI / 4;

	complex<double> num;
	for (double delta = 0.0; delta <= 2 * PI; delta += 0.05) {
		num = func(n, delta, beta, d, teta);
		fprintf(out, "%.5f %.5f\n", delta, sqrt(pow(num.real(), 2) + pow(num.imag(), 2)));
	}
	fclose(out);
}