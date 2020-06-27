
import gramatica as g
import ts as TS
from expresiones import *
from instruccionesAugus import *
from six import string_types
import threading
import time
from erroresA import *
import re

indice = 0
tag=''
LisErr=TablaError([])

def remplazar_cadena(cadena,indice,new_char):
    result=''
    if len(cadena)<indice :
        for i in range(0,len(cadena)) :
                result+=cadena[i] 
        for j in range(len(cadena),indice) : #for j in range(len(cadena),indice+1) :
            result+=' '
        result+=new_char  
    elif len(cadena)>indice :
        for i in range(0,len(cadena)) :
            if i==indice:
                result+=new_char
            else:
                result+=cadena[i]
    elif len(cadena)==indice:
        result=cadena+new_char
    return result



def get_primer_elemento_arr(id,ts):
    simbolo=ts.obtener(id)
    diccionario=simbolo.valor
    concat='0_'
    if len(simbolo.dimension)>= 1:
        for i in range(0,len(simbolo.dimension)):
            if concat in diccionario:
                return diccionario[concat]
            concat=concat+'0_'
    return None

def procesar_variable(tipoVar,ts) :
    val=ts.obtener(tipoVar.id)
    if val is None:
        print('Error: Variable no declarada')
        consola.insert('end','>>Error: Variable no declarada '+str(tipoVar.id)+'\n>>')
        newErr=ErrorRep('Semantico','Variable no declarada: '+str(tipoVar.id),indice)
        LisErr.agregar(newErr)
        return None
    if val.tipo==TS.TIPO_DATO.ARREGLO:
        consola.insert('end','>>Error: No se pueden imprimir arreglos '+str(tipoVar.id)+'\n>>')
        newErr=ErrorRep('Semantico','No se pueden imprimir arreglos: '+str(tipoVar.id),indice)
        LisErr.agregar(newErr)
        print('Error: No se pueden imprimir arreglos')
        return None
    return val.valor

def procesar_definicion(asig, ts) :
    global tag,indice
    valor=procesar_expresion(asig.valor,ts)

    simbolo=ts.obtener(asig.variable.id)
    tipo_dato=0

    if isinstance(valor,int): tipo_dato = TS.TIPO_DATO.ENTERO
    elif isinstance(valor,float): tipo_dato = TS.TIPO_DATO.FLOTANTE
    elif isinstance(valor,string_types): tipo_dato = TS.TIPO_DATO.CADENA
    
    if valor is not None:
        if isinstance(valor,TS.Simbolo):
            newsimbolo = TS.Simbolo(asig.variable.id, TS.TIPO_DATO.REFERENCIA,valor,valor.dimension,tag,[indice])
            ts.agregar(newsimbolo)

        elif simbolo is None :        
            newsimbolo = TS.Simbolo(asig.variable.id, tipo_dato, valor,[],tag,[indice])
            ts.agregar(newsimbolo)
        else:
            ref=simbolo.referencia
            if indice not in ref:
                simbolo.referencia.append(indice)
            ts.actualizar(asig.variable.id,tipo_dato,valor)
            
    
def procesar_definicion_arr(asig,ts):
    global tag
    tipo_var=asig.id
    simbolo=ts.obtener(tipo_var.id)
    if simbolo is None :        
        newsimbolo = TS.Simbolo(tipo_var.id, TS.TIPO_DATO.ARREGLO, {},[],tag,[indice])
        ts.agregar(newsimbolo)
    else:
        if indice not in simbolo.referencia:
            simbolo.referencia.append(indice)
        ts.actualizar(tipo_var.id,TS.TIPO_DATO.ARREGLO,{})

def resolver_parametros(params,ts) :
    result=[]
    for param in params :
        if isinstance(param.expresion,ExpresionValor):
            val=procesar_expresion(param.expresion,ts)
        else:
            val=procesar_expresion(param.expresion,ts)
        result.append(val)
    return result


def nueva_dimension(parametros, dim_original,index=0):
    retorno=[]
    for i in range(0,len(parametros)-index) :
        if i<len(dim_original) : 
            if isinstance(parametros[i], int) :
                if parametros[i] > dim_original[i]:
                    retorno.append(parametros[i])
                else :
                    retorno.append(dim_original[i])
            else: #si encuentra un string, significa que almacena un struct
                retorno.append(1)
                break
        else:
            if isinstance(parametros[i],int) :
                retorno.append(parametros[i])
            else:
                retorno.append(1)
                break
    return retorno

def new_dimension(parametros, dim_original):
    arreglo=parametros.split('_')
    arreglo.remove('')
    if len(arreglo)>len(dim_original):
        return arreglo
    else:
        return dim_original

def verificar_indice(parametros) :
    no_cad=0
    for i in range(0,len(parametros)):
        if isinstance(parametros[i],string_types) :
            if no_cad >= 1:
                return False
            no_cad=no_cad+1
        else:
            no_cad=0
    return True

def procesar_asign_arr(asig_arr_st,ts):
    
    tipo_var=asig_arr_st.variable
    parametros=resolver_parametros(asig_arr_st.indices,ts)
    simbolo=ts.obtener(tipo_var.id)

    if simbolo is None:
        print('Error: Variable no declarada '+tipo_var.id)
        consola.insert('end','>>Error: Variable no declarada '+str(tipo_var.id)+'\n>>')
        newErr=ErrorRep('Semantico','Variable no declarada: '+str(tipo_var.id),indice)
        LisErr.agregar(newErr)
        return None
    diccionario=simbolo.valor

    if not isinstance(diccionario,dict) and not isinstance(diccionario,string_types):
        print('Error: Variable no es arreglo '+str(tipo_var.id))
        consola.insert('end','>>Error: Variable no es arreglo '+str(tipo_var.id)+'\n>>')
        newErr=ErrorRep('Semantico','Variable no es arreglo: '+str(tipo_var.id),indice)
        LisErr.agregar(newErr)
        return None
    # OBTENER EL NUEVO VALOR
    new_value=procesar_expresion(asig_arr_st.valor,ts)
    # OBTENER LOS PARAMETROS
    temp=''
    last=''
    if not verificar_indice(parametros) :
        print('Arreglo de arreglo no permitido ',new_value)
        consola.insert('end','>>Error: Arreglo de arreglo no permitido '+str(tipo_var.id)+'\n>>')
        newErr=ErrorRep('Semantico','Arreglo de arreglo no permitido: '+str(tipo_var.id),indice)
        LisErr.agregar(newErr)
        return None
    #Concatenar Parametros
    for par in range(0,len(parametros)):
        if(par==len(parametros)-1) :
            last=parametros[par]
        else :
            temp+=str(parametros[par])+'_'
    dim=[]
    #Puede ser arreglo de caracteres
    if isinstance(diccionario,string_types) :
        cambiar_caracter_cadena(tipo_var.id,diccionario,last,new_value,ts)
    #Arreglos y Structs
    else:
        if temp !='':
            if temp in diccionario:
                if isinstance(diccionario[temp],string_types): #comprobar si es una cadena
                    if isinstance(last,int) : #Reemplazar caracter o nuevo elemento
                        last=int(last)
                        if isinstance(new_value,int) or isinstance(new_value,float) : #Nuevo Elemento
                            diccionario.update({temp+str(last)+'_':new_value})
                            #dim=nueva_dimension(parametros,simbolo.dimension,0)
                            dim=new_dimension(temp+str(last)+'_',simbolo.dimension)
                        elif len(new_value)==1: #Reemplazo de Caracter
                            cad=remplazar_cadena(diccionario[temp],last,str(new_value))
                            diccionario.update({temp:cad})
                        elif len(new_value)>1: #El indice esta ocupado
                            print('Error el indice esta ocupado con un string')
                            consola.insert('end','>>Error: Indice ocupado '+str(parametros)+'\n>>')
                            newErr=ErrorRep('Semantico','Indice ocupado '+str(parametros),indice)
                            LisErr.agregar(newErr)
                            return None
                        else: #Nuevo Elemento
                            diccionario.update({temp+str(last)+'_':new_value})
                            #dim=nueva_dimension(parametros,simbolo.dimension,0)
                            dim=new_dimension(temp+str(last)+'_',simbolo.dimension)
                    elif isinstance(last,string_types) : #Actualizar Valor !!! POSIBLE ELIMINACION ['Hola']['NoPermitido']
                        #print('Arreglo de arreglo no permitido '+new_value)
                        diccionario[temp+last+'_']=new_value
                        dim=new_dimension(temp+str(last)+'_',simbolo.dimension)
                elif isinstance(diccionario[temp],int) or isinstance(diccionario[temp],float):
                    print('Error: el indice esta ocupado')
                    consola.insert('end','>>Error: Indice ocupado '+str(parametros)+'\n>>')
                    newErr=ErrorRep('Semantico','Indice ocupado '+str(parametros),indice)
                    LisErr.agregar(newErr)
                    return None
            else:
                diccionario.update({temp+str(last)+'_':new_value})
                #dim=nueva_dimension(parametros,simbolo.dimension,0)
                dim=new_dimension(temp+str(last)+'_',simbolo.dimension)
        else :
            diccionario.update({str(last)+'_':new_value})
            dim=[1]
        if indice not in simbolo.referencia:
            simbolo.referencia.append(indice)
        ts.actualizar(tipo_var.id,TS.TIPO_DATO.ARREGLO,diccionario,dim)


def cambiar_caracter_cadena(id,cadena,index,new_value,ts):
    if isinstance(index,int) : 
        index=int(index)
        if isinstance(new_value,int) or isinstance(new_value,float) :
            print('Error: no se puede asignar un int a una cadena')
            consola.insert('end','>>Error: No se puede asignar un int a una cadena '+id+'\n>>')
            newErr=ErrorRep('Semantico','No se puede asignar un int'+str(index)+' a una cadena '+str(id),indice)
            LisErr.agregar(newErr)
        elif isinstance(new_value,string_types) and len(new_value)==1:
            cad=remplazar_cadena(cadena,index,str(new_value))
            ts.actualizar(id,TS.TIPO_DATO.CADENA,cad)
        else:
            print('Error: no se reconoce el tipo de dato')
    elif isinstance(index,string_types) :
        print('Error: Indice debe ser int '+index)
        consola.insert('end','>>Error: Indice debe ser int '+id+'\n>>')
        newErr=ErrorRep('Semantico','Indice debe ser int '+str(id),indice)
        LisErr.agregar(newErr)


def procesar_if(instr, ts,index) :
    val = procesar_expresion(instr.expLogica, ts)
    if val==1 :
        ret=ejecutarGoTo(instr.instrucciones,ts)
        return ret
    return index

def procesar_aritmetica(expresion,ts) :
    val=procesar_expresion(expresion.exp1,ts)
    val2=procesar_expresion(expresion.exp2,ts)
    if expresion.operador==OPERACION_ARITMETICA.MAS :
        if isinstance(val,string_types) and isinstance(val2,string_types) :
            return val+val2
        elif ((isinstance(val,int) or isinstance(val,float)) 
            and ((isinstance(val2,int) or isinstance(val2,float)))) :
            return val+val2
        else:
            consola.insert('end','>>Error: tipos no pueden sumarse \n>>')
            newErr=ErrorRep('Semantico','Tipos no puden sumarse ',indice)
            LisErr.agregar(newErr)
            return None
    elif expresion.operador==OPERACION_ARITMETICA.MENOS :
        if ((isinstance(val,int) or isinstance(val,float)) 
            and ((isinstance(val2,int) or isinstance(val2,float)))) :
            return val-val2
        else:
            consola.insert('end','>>Error: tipos no pueden restarse \n>>')
            newErr=ErrorRep('Semantico','Tipos no puden restarse ',indice)
            LisErr.agregar(newErr)
            return None
    elif expresion.operador==OPERACION_ARITMETICA.MULTI :
        if ((isinstance(val,int) or isinstance(val,float)) 
            and ((isinstance(val2,int) or isinstance(val2,float)))) :
            return val*val2
        else:
            consola.insert('end','>>Error: tipos no pueden multiplicarse \n>>')
            newErr=ErrorRep('Semantico','Tipos no puden multiplicarse ',indice)
            LisErr.agregar(newErr)
            return None
    elif expresion.operador==OPERACION_ARITMETICA.DIVIDIDO :
        if val2==0:
            print('Error: No se puede dividir entre 0')
            consola.insert('end','>>Error: No se puede dividir entre cero'+str(val)+' '+str(val2)+'\n>>')
            newErr=ErrorRep('Semantico','No se puede dividir entre cero '+str(val)+' '+str(val2),indice)
            LisErr.agregar(newErr)
            return None
        if ((isinstance(val,int) or isinstance(val,float)) 
            and ((isinstance(val2,int) or isinstance(val2,float)))) :
            return val/val2
        else:
            print('Error: Tipos no pueden dividirse')
            consola.insert('end','>>Error: tipos no pueden dividires \n>>')
            newErr=ErrorRep('Semantico','Tipos no puden dividirse ',indice)
            LisErr.agregar(newErr)
            return None
    elif expresion.operador==OPERACION_ARITMETICA.RESIDUO:
        if ((isinstance(val,int) or isinstance(val,float)) 
            and ((isinstance(val2,int) or isinstance(val2,float)))) :
            return val % val2
        else:
            print('Error: Tipos no pueden operarse %')
            consola.insert('end','>>Error: tipos no pueden operarse por residuo \n>>')
            newErr=ErrorRep('Semantico','Tipos no puden operarse por residuo ',indice)
            LisErr.agregar(newErr)
            return None

def procesar_relacional(expresion,ts):
    val=procesar_expresion(expresion.exp1,ts)
    val2=procesar_expresion(expresion.exp2,ts)

    if (isinstance(val,int) and isinstance(val2,float) 
        or isinstance(val,float) and isinstance(val2,int)
        or isinstance(val,float) and isinstance(val2,float)
        or isinstance(val,int) and isinstance(val2,int)) :
        if expresion.operador==OPERACION_RELACIONAL.IGUALQUE:
            return 1 if (val==val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.DISTINTO :
            return 1 if (val!=val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MAYORIGUAL:
            return 1 if (val>=val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MENORIGUAL:
            return 1 if (val<=val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MAYORQUE:
            return 1 if (val>val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MENORQUE:
            return 1 if (val<val2) else 0
    elif isinstance(val,string_types) and isinstance(val2,string_types) :
        if expresion.operador==OPERACION_RELACIONAL.IGUALQUE:
            return 1 if (val==val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.DISTINTO :
            return 1 if (val!=val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MAYORIGUAL:
            return 1 if (val>=val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MENORIGUAL:
            return 1 if (val<=val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MAYORQUE:
            return 1 if (val>val2) else 0
        elif expresion.operador==OPERACION_RELACIONAL.MENORQUE:
            return 1 if (val<val2) else 0
    else:
        print('Error: Expresion relacional con tipos incompatibls')
        consola.insert('end','>>Error: Expresion relacional con tipos incompatibles'+str(expresion.operador)+'\n>>')
        newErr=ErrorRep('Semantico','Expresion relacional con tipos incompatibles '+str(expresion.operador),indice)
        LisErr.agregar(newErr)
        return None
    

def procesar_logica(expresion,ts) :
    val=procesar_expresion(expresion.exp1,ts)
    val2=procesar_expresion(expresion.exp2,ts)

    if ((isinstance(val,int) or isinstance(val,float)) 
        and ((isinstance(val2,int) or isinstance(val2,float)))) :
        if expresion.operador==OPERACION_LOGICA.AND:
            return 1 if (val and val2) else 0
        elif expresion.operador==OPERACION_LOGICA.OR:
            return 1 if (val or val2) else 0
        elif expresion.operador==OPERACION_LOGICA.XOR:
            return 1 if (val ^ val2) else 0
        
    else:
        print('Error: No se puede realizar la op. logica')
        consola.insert('end','>>Error: Expresion logica con tipos incompatibles'+str(expresion.operador)+'\n>>')
        newErr=ErrorRep('Semantico','Expresion logica con tipos incompatibles '+str(expresion.operador),indice)
        LisErr.agregar(newErr)


def procesar_accesoarray(acceso_array,ts) :
    tipo_var=acceso_array.tipoVar
    parametros=resolver_parametros(acceso_array.params,ts)
    simbolo=ts.obtener(tipo_var.id)
    if simbolo is None:
        print('Error: Acceso a variable no existente')
        consola.insert('end','>>Error: Acceso a variable no existente'+str(tipo_var.id)+'\n>>')
        newErr=ErrorRep('Semantico','Acceso a variable no existente '+str(tipo_var.id),indice)
        LisErr.agregar(newErr)
        return None
    diccionario=simbolo.valor

    #if isinstance(diccionario,TS.Simbolo):
    #    diccionario=diccionario.valor

    temp=''
    for par in range(0,len(parametros)):
            temp+=str(parametros[par])+'_'

    if simbolo.tipo==TS.TIPO_DATO.CADENA:
        if len(parametros)==1:
            try:
                return simbolo.valor[parametros[0]]
            except:
                print('Error: El indice excede tamaño de la cadena')
                consola.insert('end','>>Error: Indice excede tamaño de la cadena'+str(tipo_var.id)+'\n>>')
                newErr=ErrorRep('Semantico','Indice excede tamaño de la cadena '+str(tipo_var.id),indice)
                LisErr.agregar(newErr)
                return None
        else:
            print('Error: Cadenas solo tienen una posicion')
            consola.insert('end','>>Error: Cadenas solo tienen una dimension'+str(tipo_var.id)+'\n>>')
            newErr=ErrorRep('Semantico','Cadenas solo tienen una dimension '+str(tipo_var.id),indice)
            LisErr.agregar(newErr)
            return None
    elif simbolo.tipo==TS.TIPO_DATO.ARREGLO:
        temp=''
        last=''
        for par in range(0,len(parametros)):
            if(par==len(parametros)-1) :
                last=parametros[par]
            else :
                temp+=str(parametros[par])+'_'
        if temp !='':
            if temp in diccionario:
                #comrpobar si es cadena
                if isinstance(diccionario[temp],string_types):
                    if isinstance(last,int) : 
                        last=int(last)
                        return diccionario[temp][last]
        if temp+str(last)+'_' in diccionario:
            return diccionario[temp+str(last)+'_']
        else:
            print('Error: No se encuentra el indice')
            consola.insert('end','>>Error: No se encuentra el indice para'+str(tipo_var.id)+'\n>>')
            newErr=ErrorRep('Semantico','No se encuentra el indice para'+str(tipo_var.id),indice)
            LisErr.agregar(newErr)
            return None
    else:
        return None

def procesar_casteo(instr,ts):
    varname=''
    if isinstance(instr.variable,Variable) :
        val=ts.obtener(instr.variable.id)
        if val is None:
            print('Indice no definido - Primer valor - var ',instr.variable.id)
            consola.insert('end','>>Error: Valor de variable no encontrado'+str(instr.variable.id)+'\n>>')
            newErr=ErrorRep('Semantico','Valor de variable no encontrado '+str(instr.variable.id),indice)
            LisErr.agregar(newErr)
            return None
        varname=instr.variable.id
        if val.tipo==TS.TIPO_DATO.ARREGLO :
            val=get_primer_elemento_arr(varname,ts)
            if val is None:
                print('Indice no definido - Primer valor - var ',varname)
                consola.insert('end','>>Error: Primer valor no encontrado'+str(varname)+'\n>>')
                newErr=ErrorRep('Semantico','Primer valor no encontrado '+str(varname),indice)
                LisErr.agregar(newErr)
                return None    
        val=val.valor  
    else:
        val=procesar_expresion(instr.variable,ts)

    if instr.tipo_dato.value==TS.TIPO_DATO.ENTERO.value:
        if isinstance(val,float):
            return int(val)
        elif isinstance(val,string_types):
            if len(val)==1:
                return int(ord(val))
            if len(val)>1:
                try:
                    return int(ord(val[0]))
                except:
                    print('Error: No se puede convertir a int ')
                    return None
            else:
                print('Error: cast int la cadena esta vacia')
                consola.insert('end','>>Error: Cast Int, la cadena esta vacia'+str(instr.variable.id)+'\n>>')
                newErr=ErrorRep('Semantico','Cast Int, la cadena esta vacia '+str(instr.variable.id),indice)
                LisErr.agregar(newErr)
                return None
        else: return val
    elif instr.tipo_dato.value==TS.TIPO_DATO.FLOTANTE.value:
        if isinstance(val,int) :
            return float(val)
        elif isinstance(val,float):
            return float(val)
        elif isinstance(val,string_types):
            if len(val)>=1:
                return float(val)
            else:
                print('Error cast to float a cadena vacia '+varname)
                consola.insert('end','>>Error: Cast Float, la cadena esta vacia'+str(instr.variable.id)+'\n>>')
                newErr=ErrorRep('Semantico','Cast Float, la cadena esta vacia '+str(instr.variable.id),indice)
                LisErr.agregar(newErr)
    elif instr.tipo_dato.value == TS.TIPO_DATO.CHAR.value:
        if isinstance(val,int) or isinstance(val,float):
            val_temp=int(val)
            if val_temp<=255:
                return str(chr(val_temp))
            else:
                return chr(val_temp%256)
        elif isinstance(val,string_types) :
            if len(val)>=1:
                return val[0]
            else:
                print('Error cast to char a cadena vacia '+instr.id)
                consola.insert('end','>>Error: Cast Char, la cadena esta vacia'+str(instr.variable.id)+'\n>>')
                newErr=ErrorRep('Semantico','Cast Char, la cadena esta vacia '+str(instr.variable.id),indice)
                LisErr.agregar(newErr)

def procesar_bit_bit(expresion,ts):
    val=procesar_expresion(expresion.exp1,ts)
    val2=procesar_expresion(expresion.exp2,ts)

    if (isinstance(val,int) and isinstance(val2,int)) :
        if expresion.operador==OPERACION_BIT_A_BIT.AND:
            return val & val2
        elif expresion.operador==OPERACION_BIT_A_BIT.OR :
            return val | val2
        elif expresion.operador==OPERACION_BIT_A_BIT.XOR:
            return val ^ val2
        elif expresion.operador==OPERACION_BIT_A_BIT.SHIFT_IZQ:
            return val << val2
        elif expresion.operador==OPERACION_BIT_A_BIT.SHIFT_DER:
            return val >> val2
    else:
        print('Error: tipos no compatibles con op. binarias')
        consola.insert('end','>>Error: Tipos no compatibles con op. binaria'+str(expresion.operador)+'\n>>')
        newErr=ErrorRep('Semantico','Tipos no compatibles con op. binaria '+str(expresion.operador),indice)
        LisErr.agregar(newErr)
    return None
    
def procesar_logicaNOT(instr,ts):
    try:
        val=procesar_expresion(instr.expresion,ts)
        return 0 if (val==1) else 1
    except:
        print('Error no se puede aplicar Neg Logica')
        consola.insert('end','>>Error: No se puede aplicar Neg Logica\n>>')
        newErr=ErrorRep('Semantico','No se puede aplicar Neg Logica ',indice)
        LisErr.agregar(newErr)
        return None

def procesar_NotBB(instr,ts) :
    try:
        val=procesar_expresion(instr.expresion,ts)
        if  isinstance(val,int) :
            binario= ~int(val)
            return int(binario)
        else:
            print('Error: no compatible para aplicar neg binario')
            consola.insert('end','>>Error: No compatible para aplicar neg binario\n>>')
            newErr=ErrorRep('Semantico','No compatible para aplicar neg binario ',indice)
            LisErr.agregar(newErr)
        return None
    except:
        print('Error no compatible para aplicar neg binario')
        consola.insert('end','>>Error: No compatible para aplicar neg binario\n>>')
        newErr=ErrorRep('Semantico','No compatible para aplicar neg binario ',indice)
        LisErr.agregar(newErr)
        return None

def procesar_negAritmetica(expresion,ts) :
    try:
        return -1*procesar_expresion(expresion.exp,ts)
    except:
        print('Error:tipo de dato no se puede multiplicar por -1')
        consola.insert('end','>>Error: No se pudo realizar la neg aritmetica\n>>')
        newErr=ErrorRep('Semantico','No se pudo realizar la neg aritmetica ',indice)
        LisErr.agregar(newErr)
        return None

def procesar_referencia(tipoVar,ts) :
    simbolo=ts.obtener(tipoVar.tipoVar.id)
    return simbolo

def procesar_expresion(expresiones,ts) :
    if isinstance(expresiones,ExpresionAritmetica) : 
        return procesar_aritmetica(expresiones,ts)
    elif isinstance(expresiones,ExpresionRelacional) :
        return procesar_relacional(expresiones,ts)
    elif isinstance(expresiones,ExpresionLogica) :
        return procesar_logica(expresiones,ts)
    elif isinstance(expresiones,ExpresionBitABit) :
        return procesar_bit_bit(expresiones,ts)
    elif isinstance(expresiones,UnitariaNegAritmetica) :
        return procesar_negAritmetica(expresiones,ts)
    elif isinstance(expresiones,UnitariaLogicaNOT) :
        return procesar_logicaNOT(expresiones,ts)
    elif isinstance(expresiones,UnitariaNotBB) :
        return procesar_NotBB(expresiones,ts)
    elif isinstance(expresiones,ExpresionValor) :
        return expresiones.val
    elif isinstance(expresiones,Variable) :
        return procesar_variable(expresiones,ts)
    elif isinstance(expresiones,AccesoArray) :
        return procesar_accesoarray(expresiones,ts)
    elif isinstance(expresiones,Read):
        return procesar_read()
    elif isinstance(expresiones,Casteo):
        return procesar_casteo(expresiones,ts)
    elif isinstance(expresiones, UnariaReferencia) :
        return procesar_referencia(expresiones,ts)
    elif isinstance(expresiones,Absoluto):
        try:
            return abs(procesar_expresion(expresiones.variable,ts))
        except:
            print('Error no se puede aplicar abs() por el tipo de dato')
            consola.insert('end','>>Error: No se puede aplicar abs() al tipo de dato\n>>')
            newErr=ErrorRep('Semantico','No se puede aplicar abs() al tipo de dato ',indice)
            LisErr.agregar(newErr)
            return None
    else: 
        print('Error:Expresion no reconocida')


def ejecutarGoTo(goto_instr,ts):
    global instrucciones,indice
    for i in range(0,len(instrucciones)) :
        if isinstance(instrucciones[i], Etiqueta) : 
            if instrucciones[i].id == goto_instr.id :
                ts.actualizarRefFuncion(goto_instr.id,indice)
                return i
    print('Error: No se encontró la etiqueta.')
    consola.insert('end','>>Error: No se encontro la etiqueta '+str(goto_instr.id)+'\n>>')
    newErr=ErrorRep('Semantico','No se encontro la etiqueta '+str(goto_instr.id),indice)
    LisErr.agregar(newErr)
    return 10000

def ejecutarPrint(imprimir,ts) :
    val=procesar_expresion(imprimir.valor,ts)
    if val is not None:
        if val=='\\n':
            consola.insert('end','\n>>')
        elif isinstance(val,string_types):        
            if val.find('\\n')==-1:
                consola.insert('end',val)            
            else:
                lista=val.split('\\n')
                for item in range(0,len(lista)):
                    if item == len(lista)-1:
                        if lista[item]=='':
                            return None    
                    consola.insert('end',lista[item]) 
                    consola.insert('end','\n>>') 
        else:
            consola.insert('end',val) 

def procesar_unset(unset, ts) :
    ts.unset(unset.id.id)

comando_consola=''
def getInput(event):
    global comando_consola
    contenido=consola.get("1.0","end-1c")
    lines = contenido.split(">>")

    last_line = lines[len(lines)-1]
    #print('El comando es: ',last_line)
    comando_consola=last_line

def wait_for_command():
    global comando_consola
    comando_consola=''
    print('Entro al wait for....')
    #while comando_consola == '':
    #    print('Waiting...')
    #    time.sleep(0.3) 
    #consola.insert('end','>>')
    #return comando_consola
    

def procesar_read() :
    
    global comando_consola
    contenido=consola.get("1.0","end-1c")
    lines = contenido.split(">>")

    last_line = lines[len(lines)-1]
    print('El comando es: ',last_line)
    comando_consola=last_line.replace("\n","")
    consola.insert("end",">>")

    if comando_consola.isalpha():
        return comando_consola
    
    try:
        return int(comando_consola)
    except:
        pass

    try:
        return float(comando_consola)
    except:
        return comando_consola
    return comando_consola

def procesar_instrucciones(instrs, ts,debugMode,indexDeb) :
    #global indice, tag
    global tag, indice
    indice=indexDeb
    #while(indice<len(instrs)): #and indexDeb<len(instrucciones)) :
    #if debugMode==1 and indexDeb != indice: continue
    #for i in range(indice,len(instrs)) :
    if isinstance(instrs[indice], Etiqueta) : tag=instrs[indice].id #print(instrs[indice].id)            
    elif isinstance(instrs[indice],GoTo) : 
        indice = ejecutarGoTo(instrs[indice],ts)
        return indice-1
    elif isinstance(instrs[indice],Print) : ejecutarPrint(instrs[indice],ts)
    elif isinstance(instrs[indice],Asignacion): 
        procesar_definicion(instrs[indice],ts)
    elif isinstance(instrs[indice],Array): procesar_definicion_arr(instrs[indice],ts)
    elif isinstance(instrs[indice],AsignacionArrSt): procesar_asign_arr(instrs[indice],ts)
    elif isinstance(instrs[indice],Unset): procesar_unset(instrs[indice],ts)
    elif isinstance(instrs[indice],ExitInstruccion): return -10
    #elif isinstance(instrs[indice],Read): procesar_read()
    elif isinstance(instrs[indice],If): 
        indice=procesar_if(instrs[indice],ts,indice)
        return indice
    
def ejecutar_instruccion(instrs, ts,debugMode,indexDeb) :
    global indice, tag
    while(indice<len(instrs)): #and indexDeb<len(instrucciones)) :
        if debugMode==1 and indexDeb != indice: continue
        #for i in range(indice,len(instrs)) :
        if isinstance(instrs[indice], Etiqueta) : tag=instrs[indice].id #print(instrs[indice].id)            
        elif isinstance(instrs[indice],GoTo) : indice = ejecutarGoTo(instrs[indice],ts)
        elif isinstance(instrs[indice],Print) : ejecutarPrint(instrs[indice],ts)
        elif isinstance(instrs[indice],Asignacion): procesar_definicion(instrs[indice],ts)
        elif isinstance(instrs[indice],Array): procesar_definicion_arr(instrs[indice],ts)
        elif isinstance(instrs[indice],AsignacionArrSt): procesar_asign_arr(instrs[indice],ts)
        elif isinstance(instrs[indice],Unset): procesar_unset(instrs[indice],ts)
        elif isinstance(instrs[indice],ExitInstruccion): break
        elif isinstance(instrs[indice],If): indice=procesar_if(instrs[indice],ts,indice)
        indice=indice+1

def get_tipo_var(asig,tipo_dato) :
    if isinstance(asig, Asignacion) or isinstance (asig,AsignacionArrSt):
        if asig.variable.tipoVar == tipo_dato:
            return asig.variable.id
    elif isinstance(asig,Array):
        if asig.id.tipoVar == tipo_dato:
            return asig.id.id


def save_tag(parametros,etiq,ts,indexS) :
    if len(parametros)>0 :
        fun=ts.obtenerFuncion(etiq)
        if fun is not None:
            ts.actualizarFuncionPar(etiq,parametros)
        else:
            simbolo=TS.Funcion(etiq,'procedimiento',parametros,[indexS])
            ts.agregarFuncion(simbolo)

def save_main(etiq,ts,indexS) :
    simbolo=TS.Funcion(etiq,'procedimiento',[],[indexS])
    ts.agregarFuncion(simbolo)

def change_proc_to_fun(tags, ts) :
    for i in range(len(tags)-1,-1,-1):
        fun=ts.obtenerFuncion(tags[i])
        if fun is not None:
            ts.actualizarFuncion(fun.id,'funcion')
            break


def fill_tags(instrs,ts) :
    etiq=''
    p_vars=[]
    r_vars=[]
    tags=[]
    if instrs is None:
        return None
    for i in range(0,len(instrs)):
        if isinstance(instrs[i], Etiqueta) : 
            etiq=instrs[i].id #print(instrs[i].id)
            tags.append(etiq)
        elif isinstance(instrs[i],GoTo) : 
            save_tag(p_vars,instrs[i].id,ts,i)
            p_vars=[]
        elif ( isinstance(instrs[i],Asignacion) or isinstance(instrs[i],Array)
            or isinstance(instrs[i],AsignacionArrSt) ):
            val_ret= get_tipo_var(instrs[i],TIPO_VARIABLE.PARAMETRO)
            if val_ret is not None and val_ret not in p_vars: 
                p_vars.append(val_ret)
            val_ret=get_tipo_var(instrs[i],TIPO_VARIABLE.VALOR_DEV_FUN)
            if val_ret is not None : 
                change_proc_to_fun(tags,ts)
                tags.clear()
            val_ret=get_tipo_var(instrs[i],TIPO_VARIABLE.RA)
            if val_ret is not None and val_ret not in r_vars: r_vars.append(val_ret)
        elif isinstance(instrs[i],If): 
            p_vars=[] 

def comprobarMain(instrucciones):
    if instrucciones is not None:
        if instrucciones[0] is not None:
            if isinstance(instrucciones[0],Etiqueta):
                if instrucciones[0].id=="main" :
                    return True
    consola.insert('end','>>Error: No se encontró o se descartó el main\n>>')
    newErr=ErrorRep('Sintactico','No se encontró o se descartó el main',1)
    LisErr.agregar(newErr)
    return False


##------------------------------------------
ts_global = TS.TablaDeSimbolos()
instrucciones = []
editor=None
consola=None
content=''
##------------------------------------------
def limpiarValores():
    global ts_global, instrucciones,indice,tag,LisErr, dot
    ts_global=TS.TablaDeSimbolos
    instrucciones= []
    indice = 0
    tag=''
    LisErr=TablaError([])
    dot=Graph('AST',format='png')

def inicializarEjecucionAscendente(contenido) :
    global LisErr, instrucciones, ts_global

    ts_global = TS.TablaDeSimbolos()
    instrucciones = g.parse(contenido,LisErr)


def inicializarGUI(txtconsola):
    global editor,consola
    consola = txtconsola

def inicializarTS():
    global instrucciones,ts_global,tag
    save_main('main',ts_global,1)
    fill_tags(instrucciones,ts_global)
    consola.insert('end',"\n>> ********  Start  ******** \n>>")
    tag='main'
    if not comprobarMain(instrucciones):
        consola.insert('end',">>Error: Verifique errores lexicos y sintacticos\n>>")
    
def ejecutarInstruccionUnitaria(debugMode,indexDeb):
    global instrucciones,ts_global
    if instrucciones is not None:
        indice_ret=procesar_instrucciones(instrucciones,ts_global,debugMode,indexDeb)   
        return indice_ret

def generarReporteTS():
    tabla_simbolos()

def generarReportesErrores():
    reporte_errores()

def generarReporteGramaticalAsc():
    g.dot.view()

def generarReporteAST():
    global dot
    dot=Graph('AST',format='png')
    dot.attr('node', shape='box')
    graficarAST()

def generarReportes():    
    #graficarAST(instrucciones)
    tabla_simbolos()
    reporte_errores()

#----------------------------------------------------------
#----------------------------------------------------------
#           GRAFICAR AST
#----------------------------------------------------------
#----------------------------------------------------------
from graphviz import Graph
from graphviz import escape

i=0
def inc():
    global i
    i +=1
    return i

dot=Graph('AST',format='png')
#dot.attr(splines='false')
dot.attr('node', shape='box')

def graficarEtiqueta(instrs):
    id=inc()
    padre=id
    dot.node(str(id),'instruccion: Etiqueta')
    id=inc()
    dot.node(str(id),'id')
    dot.edge(str(padre),str(id))
    id=inc()
    dot.node(str(id),str(instrs.id))
    dot.edge(str(id-1),str(id))
    return id

def graficarGoTo(instruccion):
    global id
    id=inc()
    dot.node(str(id),'instruccion:goto')
    id=inc()
    dot.node(str(id),'id')
    dot.edge(str(id-1),str(id))
    id=inc()
    dot.node(str(id),str(instruccion.id))
    dot.edge(str(id-1),str(id))
    return id

def graficarPrint(instruccion):
    id=inc()
    dot.node(str(id),'instruccion: Print ( expresion )')
    dot.edge(str(id),str(id+1))
    graficar_expresion(instruccion.valor)


def graficar_if(instr) :
    id=inc()
    padre=id
    dot.node(str(id),'instruccion: IF ')
    id=inc()
    dot.node(str(id),'expLogica')
    dot.edge(str(padre),str(id))
    dot.edge(str(id),str(id+1))
    graficar_expresion(instr.expLogica)
    id=inc()
    dot.edge(str(padre),str(id+1))
    graficarGoTo(instr.instrucciones)

def getVar(id):
    if id==OPERACION_ARITMETICA.MAS:
        return '+'
    elif id==OPERACION_ARITMETICA.MENOS:
        return '-'
    elif id==OPERACION_ARITMETICA.MULTI:
        return '*'
    elif id==OPERACION_ARITMETICA.DIVIDIDO:
        return '/'
    elif id==OPERACION_ARITMETICA.RESIDUO:
        return '%'
    elif id==OPERACION_LOGICA.AND:
        return '&&'
    elif id==OPERACION_LOGICA.OR:
        return '||'
    elif id==OPERACION_LOGICA.XOR:
        return 'xor'
    elif id==OPERACION_RELACIONAL.IGUALQUE:
        return '=='
    elif id==OPERACION_RELACIONAL.DISTINTO:
        return '!='
    elif id==OPERACION_RELACIONAL.MAYORIGUAL:
        return '>='
    elif id==OPERACION_RELACIONAL.MENORIGUAL:
        return '!='
    elif id==OPERACION_RELACIONAL.MAYORQUE:
        return '>'
    elif id==OPERACION_RELACIONAL.MAYORQUE:
        return '<'
    elif id==OPERACION_BIT_A_BIT.AND:
        return '&'
    elif id==OPERACION_BIT_A_BIT.OR:
        return '|'
    elif id==OPERACION_BIT_A_BIT.XOR:
        return '^'
    elif id==OPERACION_BIT_A_BIT.SHIFT_IZQ:
        return '<<'
    elif id==OPERACION_BIT_A_BIT.SHIFT_DER:
        return '>>'
    else:
        return 'op'

def graficar_arit_log_rel_bb(expresion,tipo_exp="") :
    id=inc()
    padre=id
    dot.node(str(id),'Expresion:Expresion'+tipo_exp)
    id=inc()
    dot.node(str(id),'exp1')
    dot.edge(str(padre),str(id))
    dot.edge(str(id),str(id+1))
    graficar_expresion(expresion.exp1)
    id=inc()
    dot.node(str(id),getVar(expresion.operador))
    dot.edge(str(padre),str(id))
    id=inc()
    dot.node(str(id),'exp2')
    dot.edge(str(padre),str(id))
    dot.edge(str(id),str(id+1))
    graficar_expresion(expresion.exp2)
        
def graficarUnaria(expresion,tipo_exp=""):
    id=inc()
    dot.node(str(id),'Expresion:Expresion'+tipo_exp)
    dot.edge(str(id),str(id+1))
    if isinstance(expresion,UnitariaNegAritmetica):
        graficar_expresion(expresion.exp)
    else:
        graficar_expresion(expresion.expresion)

def graficar_accesoarray(expresion):
    id=inc()
    padre=id
    dot.node(str(id),'Expresion:AccesoArray')
    id=inc()
    dot.node(str(id),"ID: "+str(expresion.tipoVar.id))
    dot.edge(str(padre),str(id))
    id=inc()
    new_padre=id
    dot.node(str(id),"parametros")
    dot.edge(str(padre),str(new_padre))

    for item in expresion.params:
        id=inc()
        dot.edge(str(new_padre),str(id+1))
        graficar_expresion(item.expresion)


    
def get_tipo_dato(tipo):

    if tipo==TS.TIPO_DATO.ENTERO:
        return 'int'
    elif tipo==TS.TIPO_DATO.FLOTANTE:
        return 'float'
    elif tipo==TS.TIPO_DATO.CHAR:
        return 'char'
    else:
        return 'TIPODATO'

def graficar_casteo(expresion):
    id=inc()
    padre=id
    dot.node(str(id),'Expresion:Casteo')
    id=inc()
    dot.node(str(id),"tipo: "+get_tipo_dato(expresion.tipo_dato))
    dot.edge(str(padre),str(id))
    #id=inc()
    #dot.node(str(id),"ID "+str(expresion.variable.val))
    #dot.edge(str(padre),str(id))
    dot.edge(str(padre),str(id+1))
    graficar_expresion(expresion.variable)

def graficar_expresion(expresiones):
    if isinstance(expresiones,ExpresionAritmetica) : 
        graficar_arit_log_rel_bb(expresiones,"Aritmetica")
    elif isinstance(expresiones,ExpresionRelacional) :
        graficar_arit_log_rel_bb(expresiones,"Relacional")
    elif isinstance(expresiones,ExpresionLogica) :
        graficar_arit_log_rel_bb(expresiones,"Logica")
    elif isinstance(expresiones,ExpresionBitABit) :
        graficar_arit_log_rel_bb(expresiones,"BitABit")
    elif isinstance(expresiones,UnitariaNegAritmetica) :
        graficarUnaria(expresiones,"NegAritmetica")
    elif isinstance(expresiones,UnitariaLogicaNOT) :
        graficarUnaria(expresiones,"LogicaNOT")
    elif isinstance(expresiones,UnitariaNotBB) :
        graficarUnaria(expresiones,"NotBB")
    elif isinstance(expresiones,ExpresionValor) :
        id=inc()
        dot.node(str(id),'ExpresionValor')
        dot.edge(str(id),str(id+1))
        id=inc()
        dot.node(str(id),str(expresiones.val))
    elif isinstance(expresiones,Variable) :
        id=inc()
        dot.node(str(id),'Variable')
        dot.edge(str(id),str(id+1))
        id=inc()
        dot.node(str(id),str(expresiones.id))
    elif isinstance(expresiones,AccesoArray) :
        graficar_accesoarray(expresiones)
    elif isinstance(expresiones,Read):
        id=inc()
        dot.node(str(id),'Read()')
        return None
    elif isinstance(expresiones,Casteo):
        return graficar_casteo(expresiones)
    elif isinstance(expresiones, UnariaReferencia) :
        id=inc()
        dot.node(str(id),' ExpresionReferencia')
        dot.edge(str(id),str(id+1))
        id=inc()
        dot.node(str(id),expresiones.tipoVar.id)
    elif isinstance(expresiones,Absoluto):
        id=inc()
        dot.node(str(id),'abs( valor )')
        dot.edge(str(id),str(id+1))
        graficar_expresion(expresiones.variable)


def graficar_Asignacion(asgin):
    id=inc()
    padre=id
    dot.node(str(id),'instruccion:Asignacion')
    id=inc()
    dot.node(str(id),asgin.variable.id)
    dot.edge(str(padre),str(id))
    dot.edge(str(padre),str(id+1))
    graficar_expresion(asgin.valor)

def graficar_AsignacionArr(asign):
    id=inc()
    padre=id
    dot.node(str(id),'instruccion:AsignArray')
    id=inc()
    dot.node(str(id),str(asign.id.id))
    dot.edge(str(padre),str(id))
    id=inc()
    dot.node(str(id),"Array")
    dot.edge(str(padre),str(id))

def graficar_unset(instr):
    id=inc()
    padre=id
    dot.node(str(id),'instruccion:Unset')
    id=inc()
    dot.node(str(id),instr.id.id)
    dot.edge(str(padre),str(id))

def graficar_asign_arr(instr):
    id=inc()
    padre=id
    dot.node(str(id),'instruccion:DefinArray')
    id=inc()
    dot.node(str(id),instr.variable.id)
    dot.edge(str(padre),str(id))
    id=inc()
    new_padre=id
    dot.node(str(id),"indices")
    dot.edge(str(padre),str(id))

    for i in range(0, len(instr.indices)):
        id=inc()
        dot.edge(str(new_padre),str(id+1)) 
        graficar_expresion(instr.indices[i].expresion)

    id=inc()
    dot.edge(str(padre),str(id+1)) 
    graficar_expresion(instr.valor)


def graficarAST():
    id=0
    padre=id
    dot.node(str(id),'inicio')
    for i in range(0,len(instrucciones)):
        id=inc()
        #dot.node(str(id),'instrucciones')
        #dot.edge(str(tempId),str(id))
        dot.edge(str(padre),str(id+1)) 
        if isinstance(instrucciones[i], Etiqueta) : graficarEtiqueta(instrucciones[i])
        elif isinstance(instrucciones[i],GoTo) : graficarGoTo(instrucciones[i])
        elif isinstance(instrucciones[i],Print) : graficarPrint(instrucciones[i])
        elif isinstance(instrucciones[i],Asignacion): graficar_Asignacion(instrucciones[i])
        elif isinstance(instrucciones[i],Array): graficar_AsignacionArr(instrucciones[i])
        elif isinstance(instrucciones[i],AsignacionArrSt): graficar_asign_arr(instrucciones[i])
        elif isinstance(instrucciones[i],Unset): graficar_unset(instrucciones[i])
        elif isinstance(instrucciones[i],ExitInstruccion):
            id=inc()
            dot.node(str(id),"instruccion:ExitIntruccion")
        elif isinstance(instrucciones[i],If): graficar_if(instrucciones[i])
    dot.view()

#----------------------------------------------------------
#----------------------------------------------------------
#           TABLA DE SIMBOLOS
#----------------------------------------------------------
#----------------------------------------------------------
from graphviz import Digraph, nohtml

def tabla_simbolos():
    ts=ts_global
    SymbolT = Digraph('g', filename='btree.gv',
                node_attr={'shape': 'plaintext', 'height': '.1'})

    
    cadena=''
    for item in ts.simbolos:
        sim=ts.obtener(item,1)
        cadena+='<TR><TD>'+str(sim.id)+'</TD>'+'<TD>'+str(sim.tipo)+'</TD>'+'<TD>'+str(len(sim.dimension))+'</TD>'+'<TD>'+str(sim.valor)+'</TD>'+'<TD>'+str(sim.ambito)+'</TD>'+'<TD>'+str(sim.referencia)+'</TD></TR>'

    for fn in ts.funciones:
        fun=ts.obtenerFuncion(fn)
        cadena+='<TR><TD>'+str(fun.id)+'</TD>'+'<TD>'+str(fun.tipo)+'</TD>'+'<TD>'+str(fun.parametros)+'</TD>'+'<TD></TD>'+'<TD></TD>'+'<TD>'+str(fun.referencia)+'</TD></TR>'

    SymbolT.node('table','''<<TABLE>
                            <TR>
                                <TD>ID</TD>
                                <TD>TIPO</TD>
                                <TD>DIMENSION</TD>
                                <TD>VALOR</TD>
                                <TD>DECLARADA EN</TD>
                                <TD>REFERENCIAS</TD>
                            </TR>'''
                            +cadena+
                        '''</TABLE>>''')

    SymbolT.view()

#----------------------------------------------------------
#----------------------------------------------------------
#----------------------------------------------------------
#           ERROREEEEEES
#----------------------------------------------------------
#----------------------------------------------------------
from graphviz import Digraph, nohtml

def reporte_errores():
    ErrReporte = Digraph('g', filename='berrores.gv', format='png',
                node_attr={'shape': 'plaintext', 'height': '.1'})
    cadena=''
    i=1
    for item in LisErr.errores:
        cadena+='<TR><TD>'+str(i)+'</TD><TD>'+str(item.tipo)+'</TD>'+'<TD>'+str(item.descripcion)+'</TD>'+'<TD>'+str(item.linea)+'</TD></TR>'
        i+=1

    ErrReporte.node('table','''<<TABLE>
                            <TR>
                                <TD>No</TD>
                                <TD>Tipo Error</TD>
                                <TD>Descripcion</TD>
                                <TD>Linea</TD>
                            </TR>'''
                            +cadena+
                        '''</TABLE>>''')
    if len(LisErr.errores)>0:
        ErrReporte.view()
