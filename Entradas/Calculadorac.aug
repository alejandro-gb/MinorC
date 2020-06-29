main:
L1:
print("Ingrese el primer numero:\n");
$t2 = read();
print("\n");
print("Ingrese el segundo numero:\n");
$t3 = read();
print("\n");
print("Que opcion desea realizar?\n");
print("+, -, *, /\n");
$t4 = read();
print("\n");
$t7 = $t4 == "+";
 if (!$t7) goto et6;
print("El ");
print("resultado ");
print("de ");
print("la ");
print("suma ");
print("es: ");
$t9 = $t2 + $t3;
print($t9);
print("\n");goto et5;
et6:
$t11 = $t4 == "-";
 if (!$t11) goto et10;
print("El ");
print("resultado ");
print("de ");
print("la ");
print("resta ");
print("es: ");
$t13 = $t2 - $t3;
print($t13);
print("\n");goto et5;
et10:
$t15 = $t4 == "*";
 if (!$t15) goto et14;
print("El ");
print("resultado ");
print("de ");
print("la ");
print("multiplicacion ");
print("es: ");
$t17 = $t2 * $t3;
print($t17);
print("\n");goto et5;
et14:
$t19 = $t4 == "/";
 if (!$t19) goto et5;
print("El ");
print("resultado ");
print("de ");
print("la ");
print("division ");
print("es: ");
$t21 = $t2 / $t3;
print($t21);
print("\n");et5:
print("¿Deseas continuar? Y/N\n");
$t22 = read();
$t25 = $t22 == "Y";
$t26 = $t22 == "y";
$t27 = $t25 || $t26;
 if (!$t27) goto ft24;
print("\n");
goto L1;
goto et23;
ft24:
print("Adios\n");
et23: