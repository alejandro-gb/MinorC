int arreglo[10] = { 658, 245, 654, 956, 5, 754, 100, 89, 98, 120};

int arregloLength = 10;

void burbuja10()
{
	int i, j, aux;
	for( i = 0; i < arregloLength - 1; i++ )
	{
		for( j = 0; j < arregloLength - i - 1; j++ )
		{
			if(arreglo[ j + 1 ] < arreglo[ j ] )
			{
				aux = arreglo[ j + 1 ];
				arreglo[ j + 1 ] = arreglo[ j ];
                    				arreglo[ j ] = aux;
			}
		}
	}
}

void imprimirBurbuja10()
{
	for( int i  = 0; i < arregloLength; i++)
	{
		printf("posicion %d: %i\n", i, arreglo[i]);
	}
}

int main()
{
	printf("Arreglo Desordenado\n");
	imprimirBurbuja10();
	printf("---------------------------\n");
	burbuja10();
	printf("Arreglo Desordenado\n");
	imprimirBurbuja10();
}








