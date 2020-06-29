int factorial(int n)
{
	switch(n) {
		case 0:
			return 1;
		default:
			return n * factorial(n - 1);
			return -100;	
	}
}

double potencia(double base, double exp)
{
	if(exp == 0) {
		return 1;
	}
	return base * potencia(base, exp - 1);
	return -100; 		
}

int mcd(int n1, int n2)
{
	if(n2 != 0) {
		return mcd(n2, n1 % n2);
	} else {
		return n1;
	}
}

int hofstaderFemenina(int n)
{
	if (n < 0) {
		return 0;
	} else {
		if(n != 0) {
			return n - hofstaderFemenina(n - 1);
		} else { 
			return 1;
			return -100; 
		}
	}
}

int hofstaderMasculino(int n)
{
	if (n < 0) {
		return 0;
	} else {
		if(n != 0) {
			return n - hofstaderMasculino(n - 1);
		} else { 
			return 0;
			return -100; 
		}
	}
}

int ackermann(int m, int n)
{
	if (m == 0) {
		return (n + 1);
	} else if (m > 0 && n == 0) {
		return ackermann(m - 1, 1);
	} else {
		return ackermann(m - 1, ackermann(m, n - 1));
	}
}

int main()
{
	printf("Ejecutando factorial de un numero\n");
	if(479001600 == factorial(12)) {
		printf("---> Done.\n");
	} else {
		printf("---> Rip.\n");
	}

	printf("Ejecutando potencia\n");
	if (64 == potencia(2.0, 6.0)) {
		printf("---> Done.\n");
	} else {
		printf("---> RIP.\n");
	}

	printf("Analizando MCD\n");
	if (25 == mcd(25, 75)) {
		printf("---> Done.\n");
	} else {
		printf("---> RIP.\n");
	}

	printf("Ejecutando Hofstadter masculino\n");
	if (8 == hofstaderMasculino(15)) {
		printf("---> Done.\n");
	} else {
		printf("---> RIP.\n");
	}

	printf("Ejecutando Hofstadter femenino\n");
	if (7 == hofstaderFemenina(15)) {
		printf("---> Done.\n");
	} else {
		printf("---> RIP.\n");
	}

	printf("Ejecutando Ackermann\n");
	if (9 == ackermann(2, 3)) {
		printf("---> Done.\n");
	} else {
		printf("---> RIP.\n");
	}

}


