
int var1 = 1;
int punteo = 0;

void Declaracion()
{
    printf("========= Metodo Declaracion =========\n");
    int n4 = 2;
    double db4 = 0.0;
    double db1 = db4;
    char chr4 = 's';
    if (db1 == db4){
        printf( "Declaraciones Bien :D\n");
        punteo = punteo + 5;
    }else {
        printf("Problemas en el metodo declaracion :(\n");
    }
    printf("======================================\n");
    
}

void operacionesBasicas()
{
    printf("Operaciones Aritmeticas 1: valor esperado:  \na)62   \nb)0   \nc)-19   \nd)256   \nresultados:\n");
    double a = (20-10+8/2*3+10-10-10+50);
    int a2 = (int) a;
    double b = (50/50*50+50-100+100-100);
    int b2 = (int) b;
    double c = (100/20*9-78+6-7+8-7+7*1*2*3/3);
    int c2 = (int) c;
    printf("a) %d\n", a2);
    printf("b) %d\n", b2);
    printf("c) %d\n", c2);
    if (a2==62 && b2==0 && c2 == -19)
    {
        printf("Operaciones aritmeticas 1 bien :D\n");
        punteo = punteo + 5;
    }
    else 
    {
        printf("Error en las operaciones basicas :(\n");
    }
}

void operacionesAvanzadas(){
    int aritmetica1 = 2;
    int aritmetica2 = -10;
    printf("Operaciones Aritmeticas 2:\n valor esperado:\n -20  2.0\n resultado:\n");
    int aritmetica3 = aritmetica2*aritmetica1;
    printf("%d  ",aritmetica3);
    double aritmetica4 = aritmetica3/aritmetica1+50/50+50*2-100+100/100-0;
    printf("%f\n",aritmetica4);
    if (aritmetica3 == -20 && aritmetica4 == -8.0){
        printf("Operaciones aritmeticas 2 bien :D\n");
        punteo = punteo + 5;
    }else {
        printf("Error Operaciones Aritmeticas :c\n");
    }
}

void Aritmeticas(){
   
    
    printf("==============Aritmeticas=============\n");

    double n1 = 0.0 + 1 + 1 + 1 + 0.1 + 49;
    printf("El valor de  n1 = %f\n", n1);
    if (n1 == 52.1)
    {
        punteo = punteo + 5;
    }
    else 
    {
        printf("Perdiste 5 puntos en suma de enteros y decimales :c\n");
    }

    double n4 = (5750 * 2) - 11800 + 1.0;
    double n3 = (((3 * 3) + 4) - 80 + 40.00 * 2 + 358.50 - (29 / 14.50)) - (0.50) + n4;
    printf("El valor de n3 = %f\n", n3);
    if (n3 == 70)
    {
        punteo = punteo + 3;
    }
    else 
    {
        printf("Perdiste 3 puntos :c\n");
    }
    operacionesBasicas();
    operacionesAvanzadas();
    printf("======================================\n");
}

void Logicas2(){
    int n0 = 16;
    printf("==============Logicas2=============\n");

    if (!(!(n0 == 16 && 0==1) && !(1))){
        printf("Not y Ands Correctos\n");
        punteo = punteo +3;
    }else {
        printf("No funcionan nots y ands :(\n");
    }

    double n1 = n0 /16;
    n1 = n1 + 1;
    int condicion1 = n1 != 2;
    double aritmetica1 = n0/16 + 0;
    int condicion2 = aritmetica1 == n1;
    int condicion3 = !1;
        
    if (!(!(!(condicion1 || condicion2) || condicion3 ))){
        printf("Nots y Ors correctos\n");
        punteo = punteo + 3;
    }else {
        printf("No Funciona nots y ands :(\n");
    }
    printf("======================================\n");
}

void BitABit(){
    int n0 = 16;
    printf("==============Bit a Bit=============\n");

    int n1 = n0 & n0;

    if( n1 == 16)
    {
        printf("AND Bit a Bit bien\n");
        punteo = punteo + 1;
    }
    else
    {
        printf("AND Bit a Bit mal\n");
    }

    n1 = 51 | ~30;
    int n2 = n1 ^ 60 ^ 70 ^ 32;
    if( n2 == -87)
    {
        printf("OR, NOT, XOR Bit a Bit bien\n");
        punteo = punteo + 3;
    }
    else
    {
        printf("OR, NOT, XOR Bit a Bit mal\n");
    }

    printf("======================================\n");
}

void Logicas()
{
    printf("==============Logicas1=============\n");
    if (!!!!!!!!!!!!!!!!!!!!!!1){
        punteo = punteo + 1;
        printf("Bien primera condicion :)\n");
    }else {
        printf("Perdiste 1 punto :c\n");
    }

    if (1 && 1 || 0 && 0 && 0 || !1){
        punteo = punteo + 1;
        printf("Bien segunda condicion :)\n");
    }else {
        printf("Mal segunda condicion :c\n");
    }
    printf("======================================\n");
    Logicas2();
    BitABit();
}

void relaciones1(int salida)
{
    printf("==============relacionales1=============\n");
    double n0 = salida + 0.0;
    if (n0 < 34.44)
    {
        salida = salida+15;
        if (salida > 44)
        {
            salida = salida +1;
        }
    }
    else {
        salida = 1;
    }
        
    if (salida != 1)
        {
            if (salida == 50)
                {
                    printf("salida Correcta Relacionales 1!\n");
                    punteo = punteo + 5;
                }
                else {
                    printf("salida incorrecta!!\n");
                }
        }
        else {
            printf("salida incorrecta!!\n");
        }
    printf("======================================\n");
}

void relaciones2(int n0)
{
    printf("============Relacionales2=============\n");

    if (10-15 >= 0 && 44.44 == 44.44)
    {
        printf("salida incorrecta primer if relacionales2!!\n");
    }
    else {
        if (15+8 == 22-10+5*3-4 && 13*0>-1)
        {
            if (10.0 != 11.0-1.01 )
            {
                printf("salida CORRECTA en relacionales2!!\n");
                punteo = punteo + 5;
            }
            else {
                printf("salida incorrecta segundo if relacionales 2!!\n");
            }
        }
        else 
        {
            if (1 == 1)
            {
                printf("salida incorrecta relacionales 2 3er if !!\n");
            }
            else {
                printf("salida incorrecta relacionales 2 Sino3er if !!\n");
            }
        }
    }
    printf("======================================\n");
}

void Relacionales()
{
    int n0 = 34;
    int n1 = 16;
    
    relaciones1(n0);
    relaciones2(n1);
}

int main()
{
    int var1 = 0;

    printf("-----------------CALIFICACION-----------------\n");

    if (var1 != 0)
    {
        printf("No se toma con prioridad la variable local ante la global\n");
        printf("Perdiste 5 puntos :c\n");
    }
    else
    {
        punteo = punteo + 5;
    }

    Declaracion();

    Aritmeticas();

    Logicas();

    Relacionales();

    printf("punteo Final: %d\n", punteo);

    printf("FINNNNNNNN\n");
}
