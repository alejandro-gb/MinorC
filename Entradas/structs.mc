struct contacto
{
    int telefono, edad;
    char nombre[], apellido[];
    char sexo;
};

int main()
{
    struct contacto directorio[5];
    directorio[0].nombre = "Luis";
    directorio[0].apellido = "Espino";
    directorio[0].sexo = 'm';
    directorio[0].telefono = 54682145;
    directorio[0].edad = 40;

    directorio[1].nombre = "Juan";
    directorio[1].apellido = "Maeda";
    directorio[1].sexo = 'm';
    directorio[1].telefono = 34586245;
    directorio[1].edad = 24;

    directorio[2].nombre = "Pavel";
    directorio[2].apellido = "Vasquez";
    directorio[2].sexo = 'm';
    directorio[2].telefono = 95862451;
    directorio[2].edad = 23;

    directorio[3].nombre = "Maria";
    directorio[3].apellido = "Ramirez";
    directorio[3].sexo = 'f';
    directorio[3].telefono = 56145233;
    directorio[3].edad = 30;

    directorio[4].nombre = "Pablo";
    directorio[4].apellido = "Escobar";
    directorio[4].sexo = 'm';
    directorio[4].telefono = 85462592;
    directorio[4].edad = 60;

    for(int i = 0; i < 5; i++)
    {
        printf("Datos del contacto numero %i:\n", i+1);
        printf("\tNombre: %s\n", directorio[i].nombre);
        printf("\tApellido: %s\n", directorio[i].apellido);
        printf("\tSexo: %c\n", directorio[i].sexo);
        printf("\tTelefono: %d\n", directorio[i].telefono);
        printf("\tEdad: %i\n", directorio[i].edad);
    }
    printf("------------------------------\n");
    int matriz[5][5] = {{0,1,2,3,4},{5,6,7,8,9},{10,11,12,13,14},{15,16,17,18,19},{20,21,22,23,24}};

    for(int i = 0; i < 5; i ++)
    {
        for(int j = 0; j < 5; j++)
        {
            printf("Posicion [%d][%d] = %d\n", i, j, matriz[i][j]);
        }
    }

    return 0;
}




