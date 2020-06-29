int main(){
	inicio:
	printf("Ingrese el primer numero:\n");
	int primer_numero = scanf();
	printf("\n");
	printf("Ingrese el segundo numero:\n");
	int segundo_numero = scanf();
	printf("\n");
	printf("Que opcion desea realizar?\n");
	printf("+, -, *, /\n");
	char signo = scanf();
	printf("\n");
	if(signo=="+"){
		printf("El resultado de la suma es: %d\n", primer_numero+segundo_numero);
	}else if(signo=="-"){
		printf("El resultado de la resta es: %d\n", primer_numero-segundo_numero);
	}else if(signo=="*"){
		printf("El resultado de la multiplicacion es: %d\n", primer_numero*segundo_numero);
	}else if(signo=="/"){
		printf("El resultado de la division es: %d\n", primer_numero/segundo_numero);
	}
	
	printf("¿Deseas continuar? Y/N\n");
	char respuesta = scanf();
	if(respuesta == "Y" || respuesta=="y"){
        printf("\n");
		goto inicio;
	}else{
		printf("Adios\n");
	}
}
