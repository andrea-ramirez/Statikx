import lexerParser
import memoriaVirtual
from memoriaVM import MemoriaFuncion
from memoriaVM import MemoriaGlobal
from queue import LifoQueue
import sys
import copy


datos = lexerParser.exportData()
cuadruplos = datos['cuads']
dirFunc = datos['dirfunc']
tablaConst = datos['tablaconst']
currentScript = datos['script']
dirsVirtuales = datos['direcciones']

nombreScript = cuadruplos[0][3]

# Pila de current Ips 
pilaCurrIps = LifoQueue(maxsize=0)

# Mapa de memoria
pilaMemoriasLocales = LifoQueue(maxsize=0) # Para mandar a dormir la memoria
memoriaGlobal = MemoriaGlobal()
pilaNuevaMemoriasLocales = []

# Resize Memoria Global
recursosMain = dirFunc[cuadruplos[0][3]][2]
memoriaGlobal.globalInt = ['-'] * recursosMain['vI']
memoriaGlobal.globalFloat = ['-'] * recursosMain['vF']
memoriaGlobal.globalC = ['-'] * recursosMain['vC']
memoriaGlobal.globalDf = ['-'] * recursosMain['vDf']

memoriaGlobal.tempInt = ['-'] * recursosMain['tI']
memoriaGlobal.tempFloat = ['-'] * recursosMain['tF']
memoriaGlobal.tempC = ['-'] * recursosMain['tC']
memoriaGlobal.tempPointer = ['-'] * recursosMain['tPointer']
memoriaGlobal.tempBool = ['-'] * recursosMain['tB']


#Definir vectores de cada memoria, cambiar size dependiendo de qué necesite
def createMemoriaLocal(recursosFuncion):
    currentMemoriaLocal = MemoriaFuncion()

    currentMemoriaLocal.localInt = ['-'] * recursosFuncion['vI']
    currentMemoriaLocal.localFloat = ['-'] * recursosFuncion['vF']
    currentMemoriaLocal.localC = ['-'] * recursosFuncion['vC']
    currentMemoriaLocal.localDf = ['-'] * recursosFuncion['vDf']

    currentMemoriaLocal.tempInt = ['-'] * recursosFuncion['tI']
    currentMemoriaLocal.tempFloat = ['-'] * recursosFuncion['tF']
    currentMemoriaLocal.tempC = ['-'] * recursosFuncion['tC']
    currentMemoriaLocal.tempPointer = ['-'] * recursosFuncion['tPointer']
    currentMemoriaLocal.tempBool = ['-'] * recursosFuncion['tB']

    pilaNuevaMemoriasLocales.append(currentMemoriaLocal)

def getConstante(direccion):
    for const in tablaConst.keys():
        if tablaConst[const][1] == direccion:
            if tablaConst[const][0] == '4':
                # Para constantes char
                return chr(const)
            else:
                return const
    print("ERROR: No se encontró {} en tabla de constantes".format(direccion))

def getValue(direccion):
    # Locales
    if len(list(pilaMemoriasLocales.queue)) > 0:
        memoriaLocal = pilaMemoriasLocales.get()
        pilaMemoriasLocales.put(memoriaLocal)

    # Globales
    if 1000 <= direccion < 2000:
        # Int
        if memoriaGlobal.globalInt[direccion - 1000] == '-':
            print("No hay valor en la direccion {} para globables ints".format(direccion))
            sys.exit()
        return memoriaGlobal.globalInt[direccion - 1000]
    elif 2000 <= direccion < 3000:
        # Float
        if memoriaGlobal.globalFloat[direccion - 2000] == '-':
            print("No hay valor en la direccion {} para globables floats".format(direccion))
        return memoriaGlobal.globalFloat[direccion - 2000]
    elif 3000 <= direccion < 4000:
        # C
        if memoriaGlobal.globalC[direccion - 3000] == '-':
            print("No hay valor en la direccion {} para globables chars".format(direccion))
        return memoriaGlobal.globalC[direccion - 3000]
    elif 4000 <= direccion < 5000:
        # Df
        if memoriaGlobal.globalDf[direccion - 4000] == '-':
            print("No hay valor en la direccion {} para globables dfs".format(direccion))
        return memoriaGlobal.globalDf[direccion - 4000]
    # Locales
    elif 5000 <= direccion < 6000:
        # Int
        if memoriaLocal.localInt[direccion - 5000] == '-':
            print("No hay valor en la direccion {} para locales ints".format(direccion))
        return memoriaLocal.localInt[direccion - 5000]
    elif 6000 <= direccion < 7000:
        # Float
        if memoriaLocal.localFloat[direccion - 6000] == '-':
            print("No hay valor en la direccion {} para locales floats".format(direccion))
        return memoriaLocal.localFloat[direccion - 6000]
    elif 7000 <= direccion < 8000:
        # Char
        if memoriaLocal.localC[direccion - 7000] == '-':
            print("No hay valor en la direccion {} para locales chars".format(direccion))
        return memoriaLocal.localC[direccion - 7000]
    elif 8000 <= direccion < 9000:
        # Df
        if memoriaLocal.localDf[direccion - 8000] == '-':
            print("No hay valor en la direccion {} para locales dfs".format(direccion))
        return memoriaLocal.localDf[direccion - 8000]
    # Temporales
    elif 9000<= direccion < 10000:
        # Int
        if memoriaLocal.tempInt[direccion - 9000] == '-':
            print("No hay valor en la direccion {} para temporales ints".format(direccion))
        return memoriaLocal.tempInt[direccion - 9000]
    elif 10000 <= direccion < 11000:
        # Floats
        if memoriaLocal.tempFloat[direccion - 10000] == '-':
            print("No hay valor en la direccion {} para temporales floats".format(direccion))
        return memoriaLocal.tempFloat[direccion - 10000]
    elif 11000 <= direccion < 12000:
        # C
        if memoriaLocal.tempC[direccion - 11000] == '-':
            print("No hay valor en la direccion {} para temporales chars".format(direccion))
        return memoriaLocal.tempC[direccion - 11000]
    elif 12000 <= direccion < 13000:
        # Pointers
        if memoriaLocal.tempPointer[direccion - 12000] == '-':
            print("No hay valor en la direccion {} para temporales pointers".format(direccion))
        return memoriaLocal.tempPointer[direccion - 12000]
    elif 13000 <= direccion < 14000:
        # Booleans
        if memoriaLocal.tempBool[direccion - 13000] == '-':
            print("No hay valor en la direccion {} para temporales booleans".format(direccion))
        return memoriaLocal.tempBool[direccion - 13000]
    # Constantes
    elif 14000 <= direccion < 18000:
        return getConstante(direccion)
    # Temporales globales
    elif 18000 <= direccion < 19000:
        # Int
        if memoriaGlobal.tempInt[direccion - 18000] == '-':
            print("No hay valor en la direccion {} para temporales globales ints".format(direccion))
        return memoriaGlobal.tempInt[direccion - 18000]
    elif 19000 <= direccion < 20000:
        # Float
        if memoriaGlobal.tempFloat[direccion - 19000] == '-':
            print("No hay valor en la direccion {} para temporales globales floats".format(direccion))
        return memoriaGlobal.tempFloat[direccion - 19000]
    elif 20000 <= direccion < 21000:
        # C
        if memoriaGlobal.tempC[direccion - 20000] == '-':
            print("No hay valor en la direccion {} para temporales globales chars".format(direccion))
        return memoriaGlobal.tempC[direccion - 20000]
    elif 21000 <= direccion < 22000:
        # Pointer
        if memoriaGlobal.tempPointer[direccion - 21000] == '-':
            print("No hay valor en la direccion {} para temporales globales pointers".format(direccion))
        return memoriaGlobal.tempPointer[direccion - 21000]
    elif 22000 <= direccion < 23000:
        # Bool
        if memoriaGlobal.tempBool[direccion - 22000] == '-':
            print("No hay valor en la direccion {} para temporales globales booleanos".format(direccion))
        return memoriaGlobal.tempBool[direccion - 22000]
    
    #Constantes
    else:
        print("DIRECCION VIRTUAL DESCONOCIDA: {}".format(direccion))
        sys.exit()

def printPilaMemoriasLocales():
    index = 0
    for mem in list(pilaMemoriasLocales.queue):
        print("MEMORIA {}".format(index))
        mem.print()
        index += 1


# Procesador
currentIp = 0

while currentIp < len(cuadruplos):

    # GOTO
    if cuadruplos[currentIp][0] == 'Goto':
        # Goto Main
        try:
            if cuadruplos[currentIp][3] != int:
                currentIp = dirFunc[cuadruplos[currentIp][3]][1] - 1
            else:
                # Goto saltos condicinales
                print("No debería llegar aquí")
        except:
            salto = cuadruplos[currentIp][3]
            currentIp = salto - 1

    # GOTOF
    elif cuadruplos[currentIp][0] == 'GotoF':
        tempB = getValue(cuadruplos[currentIp][1])
        salto = cuadruplos[currentIp][3]

        if tempB == False:
            currentIp = salto - 1
        else:
            currentIp += 1


    # PLUS
    elif cuadruplos[currentIp][0] == '+':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer suma

        if 18000 <= resp < 19000:
        # global temp int
            memoriaGlobal.tempInt[resp-18000] = getValue(elemIzq) + getValue(elemDer)
        elif 19000 <= resp < 20000:
        # global temp float
            memoriaGlobal.tempFloat[resp-19000] = getValue(elemIzq) + getValue(elemDer)
        elif 21000 <= resp < 22000:
        # global temp pointer
            memoriaGlobal.tempPointer[resp-21000] = getValue(elemIzq) + getValue(elemDer)
        elif 9000 <= resp < 10000:
        # local temp int
            topMemLocal.tempInt[resp-9000] = getValue(elemIzq) + getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        elif 10000 <= resp < 11000:
        # local temp float
            topMemLocal.tempFloat[resp-10000] = getValue(elemIzq) + getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # local temp pointer
        elif 12000 <= resp < 13000:
            print("ESTAS SUMANDO POINTER - SE HACE DIFERENTE")
            sys.exit()
            topMemLocal.tempPointer[resp-21000] = getValue(elemIzq) + getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("ALGO MAL")
            sys.exit()

        currentIp += 1

    # MINUS
    elif cuadruplos[currentIp][0] == '-':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer resta

        if 18000 <= resp < 19000:
        # global temp int
            memoriaGlobal.tempInt[resp-18000] = getValue(elemIzq) - getValue(elemDer)
            # print(memoriaGlobal.tempInt)
        elif 19000 <= resp < 20000:
        # global temp float
            memoriaGlobal.tempFloat[resp-19000] = getValue(elemIzq) - getValue(elemDer)
        elif 21000 <= resp < 22000:
        # global temp pointer
            print("ESTAS RESTANDO POINTER - SE HACE DIFERENTE")
            memoriaGlobal.tempPointer[resp-21000] = getValue(elemIzq) - getValue(elemDer)
            print("ALGO MAL")
            sys.exit()
        elif 9000 <= resp < 10000:
        # local temp int
            topMemLocal.tempInt[resp-9000] = getValue(elemIzq) - getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        elif 10000 <= resp < 11000:
        # local temp float
            topMemLocal.tempFloat[resp-10000] = getValue(elemIzq) - getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # local temp pointer
        elif 12000 <= resp < 13000:
            print("ESTAS RESTANDO POINTER - SE HACE DIFERENTE")
            topMemLocal.tempPointer[resp-21000] = getValue(elemIzq) - getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("ALGO MAL")
            sys.exit()

        currentIp += 1

    # MULT
    elif cuadruplos[currentIp][0] == '*':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer multiplicación

        if 18000 <= resp < 19000:
        # global temp int
            memoriaGlobal.tempInt[resp-18000] = getValue(elemIzq) * getValue(elemDer)
            # print(memoriaGlobal.tempInt)
        elif 19000 <= resp < 20000:
        # global temp float
            memoriaGlobal.tempFloat[resp-19000] = getValue(elemIzq) * getValue(elemDer)
        elif 21000 <= resp < 22000:
        # global temp pointer
            print("ESTAS MULTIPLICANDO POINTER - SE HACE DIFERENTE")
            memoriaGlobal.tempPointer[resp-21000] = getValue(elemIzq) * getValue(elemDer)
            print("ALGO MAL")
            sys.exit()
        elif 9000 <= resp < 10000:
        # local temp int
            topMemLocal.tempInt[resp-9000] = getValue(elemIzq) * getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        elif 10000 <= resp < 11000:
        # local temp float
            topMemLocal.tempFloat[resp-10000] = getValue(elemIzq) * getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # local temp pointer
        elif 12000 <= resp < 13000:
            print("ESTAS MULTIPLICANDO POINTER - SE HACE DIFERENTE")
            topMemLocal.tempPointer[resp-21000] = getValue(elemIzq) * getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("ALGO MAL")
            sys.exit()

        currentIp += 1

    # DIV
    elif cuadruplos[currentIp][0] == '/':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer división

        if 18000 <= resp < 19000:
        # global temp int
            memoriaGlobal.tempInt[resp-18000] = getValue(elemIzq) / getValue(elemDer)
            # print(memoriaGlobal.tempInt)
        elif 19000 <= resp < 20000:
        # global temp float
            memoriaGlobal.tempFloat[resp-19000] = getValue(elemIzq) / getValue(elemDer)
        elif 21000 <= resp < 22000:
        # global temp pointer
            print("ESTAS DIVIDIENDO POINTER - SE HACE DIFERENTE")
            memoriaGlobal.tempPointer[resp-21000] = getValue(elemIzq) / getValue(elemDer)
            print("ALGO MAL")
            sys.exit()
        elif 9000 <= resp < 10000:
        # local temp int
            topMemLocal.tempInt[resp-9000] = getValue(elemIzq) / getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        elif 10000 <= resp < 11000:
        # local temp float
            topMemLocal.tempFloat[resp-10000] = getValue(elemIzq) / getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # local temp pointer
        elif 12000 <= resp < 13000:
            print("ESTAS DIVIDIENDO POINTER - SE HACE DIFERENTE")
            topMemLocal.tempPointer[resp-21000] = getValue(elemIzq) / getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("ALGO MAL")
            sys.exit()

        currentIp += 1

    # MAYOR QUE
    elif cuadruplos[currentIp][0] == '>':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer mayor que

        if 22000 <= resp < 23000:
        # global temp bool
            memoriaGlobal.tempBool[resp-22000] = getValue(elemIzq) > getValue(elemDer)
        elif 13000 <= resp < 14000:
        # local temp bool
            topMemLocal.tempBool[resp-13000] = getValue(elemIzq) > getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("COMBINACION NO ESPERADA en MAYOR QUE")
            sys.exit()

        currentIp += 1

    # MENOR QUE
    elif cuadruplos[currentIp][0] == '<':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer menor que

        if 22000 <= resp < 23000:
        # global temp bool
            memoriaGlobal.tempBool[resp-22000] = getValue(elemIzq) < getValue(elemDer)
        elif 13000 <= resp < 14000:
        # local temp bool
            topMemLocal.tempBool[resp-13000] = getValue(elemIzq) < getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("COMBINACION NO ESPERADA en MENOR QUE")
            sys.exit()

        currentIp += 1

    # EQUALS
    elif cuadruplos[currentIp][0] == '==':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer equals

        if 22000 <= resp < 23000:
        # global temp bool
            memoriaGlobal.tempBool[resp-22000] = getValue(elemIzq) == getValue(elemDer)
        elif 13000 <= resp < 14000:
        # local temp bool
            topMemLocal.tempBool[resp-13000] = getValue(elemIzq) == getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("COMBINACION NO ESPERADA en EQUALS")
            sys.exit()

        currentIp += 1

    # NOT EQUALS
    elif cuadruplos[currentIp][0] == '!=':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer noequals

        if 22000 <= resp < 23000:
        # global temp bool
            memoriaGlobal.tempBool[resp-22000] = getValue(elemIzq) != getValue(elemDer)
        elif 13000 <= resp < 14000:
        # local temp bool
            topMemLocal.tempBool[resp-13000] = getValue(elemIzq) != getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("COMBINACION NO ESPERADA en NOT EQUALS")
            sys.exit()

        currentIp += 1

    # AND
    elif cuadruplos[currentIp][0] == '&&':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer AND

        if 22000 <= resp < 23000:
        # global temp bool
            memoriaGlobal.tempBool[resp-22000] = getValue(elemIzq) and getValue(elemDer)
        elif 13000 <= resp < 14000:
        # local temp bool
            topMemLocal.tempBool[resp-13000] = getValue(elemIzq) and getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("COMBINACION NO ESPERADA en AND")
            sys.exit()

        currentIp += 1

    # OR
    elif cuadruplos[currentIp][0] == '||':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Checar si alguno de los operandos es tempPointer
        if 21000 <= elemIzq < 22000 or 12000 <= elemIzq < 13000:
            elemIzq = getValue(elemIzq)

        if 21000 <= elemDer < 22000 or 12000 <= elemDer < 13000:
            elemDer = getValue(elemDer)

        # Hacer OR

        if 22000 <= resp < 23000:
        # global temp bool
            memoriaGlobal.tempBool[resp-22000] = getValue(elemIzq) or getValue(elemDer)
        elif 13000 <= resp < 14000:
        # local temp bool
            topMemLocal.tempBool[resp-13000] = getValue(elemIzq) or getValue(elemDer)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        else:
            print("COMBINACION NO ESPERADA en OR")
            sys.exit()

        currentIp += 1
        

    # ASIGN
    elif cuadruplos[currentIp][0] == '=':
        valor = cuadruplos[currentIp][1]
        aAsignar = cuadruplos[currentIp][3]

        if len(list(pilaMemoriasLocales.queue)) > 0:
            topMemLocal = pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)

        # Si es pointer se agarra el valor de la dirección que está en aAsignar
        if 21000 <= aAsignar < 22000 or 12000 <= aAsignar < 13000:
            aAsignar = getValue(aAsignar)
        
        # Si es pointer se agarra el valor de la dirección que está en 'valor'
        if 21000 <= valor < 22000 or 12000 <= valor < 13000:
            valor = getValue(valor)

        # Hace asignación
            
        # Global int
        if 1000 <= aAsignar < 2000:
            memoriaGlobal.globalInt[aAsignar - 1000] = getValue(valor)
        # Global Float
        elif 2000 <= aAsignar < 3000:
            memoriaGlobal.globalFloat[aAsignar - 2000] = getValue(valor)
        # Global Char
        elif 3000 <= aAsignar < 4000:
            memoriaGlobal.globalC[aAsignar - 3000] = getValue(valor)
        # Global DF
        elif 4000 <= aAsignar < 5000:
            memoriaGlobal.globalFloat[aAsignar - 4000] = getValue(valor)
        # Local Int
        elif 5000 <= aAsignar < 6000:
            topMemLocal.localInt[aAsignar - 5000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Local float
        elif 6000 <= aAsignar < 7000:
            topMemLocal.localFloat[aAsignar - 6000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Local Chars
        elif 7000 <= aAsignar < 8000:
            topMemLocal.localC[aAsignar - 7000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Local Dfs
        elif 8000 <= aAsignar < 9000:
            topMemLocal.localDf[aAsignar - 8000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Temp local int
        elif 9000 <= aAsignar < 10000:
            topMemLocal.tempInt[aAsignar - 9000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Temp local float
        elif 10000 <= aAsignar < 11000:
            topMemLocal.tempFloat[aAsignar - 10000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Temp local char
        elif 11000 <= aAsignar < 12000:
            topMemLocal.tempC[aAsignar - 11000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # Temp local pointer
        elif 12000 <= aAsignar < 13000:
            print("ASIGNANDO POINTERS, DEBE SER DIFERENTE")
            print("NUNCA LLEAGAS")
            sys.exit()
            topMemLocal.tempPointer[aAsignar - 12000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
            
        # Temp local BOOL - no creo que sea necesario? no tengo variables booleanas
        elif 13000 <= aAsignar < 14000:
            topMemLocal.tempB[aAsignar - 13000] = getValue(valor)
            pilaMemoriasLocales.get()
            pilaMemoriasLocales.put(topMemLocal)
        # GLOBAL TEMP INT
        elif 18000 <= aAsignar < 19000:
            memoriaGlobal.tempInt[aAsignar - 18000] = getValue(valor)
        # GLOBAL TEMP float
        elif 19000 <= aAsignar < 20000:
            memoriaGlobal.tempFloat[aAsignar - 19000] = getValue(valor)
        # GLOBAL TEMP char
        elif 20000 <= aAsignar < 21000:
            memoriaGlobal.tempC[aAsignar - 20000] = getValue(valor)
        # GLOBAL TEMP pointer
        elif 21000 <= aAsignar < 22000:
            print("NUNCA LLEAGAS")
            sys.exit()
            print("ASIGNANDO POINTERS, DEBE SER DIFERENTE")
            print(aAsignar)
            aAsignar = getValue(aAsignar)
            print(aAsignar)
            # memoriaGlobal.tempPointer[aAsignar - 21000] = getValue(valor)
            sys.exit()
        # GLOBAL TEMP bool = no creo que sea necesairo
        elif 22000 <= aAsignar < 23000:
            memoriaGlobal.tempBool[aAsignar - 22000] = getValue(valor)
        else:
            print("FALTA IMPLEMENTAR ASIGN CON {} TIPO DE VALOR".format(aAsignar))
        
        currentIp += 1

    # PRINT
    elif cuadruplos[currentIp][0] == 'put':
        toPrint = cuadruplos[currentIp][3]

        if 21000 <= toPrint < 22000 or 12000 <= toPrint < 13000:
            toPrint = getValue(toPrint)

        print("Statikx >> {}".format(getValue(toPrint)))
        currentIp += 1


    # FUNCTIONS

    # ERA
    elif cuadruplos[currentIp][0] == 'ERA':
        nombreFunc = cuadruplos[currentIp][3]
        recursosFuncion = dirFunc[nombreFunc][2]
        createMemoriaLocal(recursosFuncion)

        currentIp += 1

    # PARAM
    elif cuadruplos[currentIp][0] == 'Parameter':
        param = cuadruplos[currentIp][1]
        indexP = cuadruplos[currentIp][3]

        topMemNueva = pilaNuevaMemoriasLocales[-1]

        # Global int, global temp int, local int, local temp int, constante int
        if 1000 <= param < 2000 or 18000 <= param < 19000 or 5000 <= param < 6000 or 9000 <= param < 10000 or 14000 <= param < 15000:
            topMemNueva.localInt[indexP - 1] = getValue(param)
        # Global float, global temp float, local float, local temp float, constante float
        elif 2000 <= param < 3000 or 19000 <= param < 20000 or 6000 <= param < 7000 or 10000 <= param < 11000 or 15000 <= param < 16000:
            topMemNueva.localFloat[indexP - 1] = getValue(param)
        # Global char, global temp char, local char, local temp char, constante char
        elif 3000 <= param < 4000 or 20000 <= param < 21000 or 7000 <= param < 8000 or 11000 <= param < 12000 or 16000 <= param < 17000:
            topMemNueva.localC[indexP - 1] = getValue(param)
        # Global df, local df
        elif 4000 <= param < 5000 or 8000 <= param < 9000:
            topMemNueva.localDf[indexP - 1] = getValue(param)
        # Global temp Pointer, local temp pointer
        elif 21000 <= param < 22000 or 12000 <= param < 13000:
            print("Todavía no implementado pointers")
            sys.exit()
            # Tengo que checar qué hay dentro de esa direccion y después ver qué tipo de variable es. Al final lo asigno a topMemNueva
            topMemNueva.tempPointer[indexP - 1] = getValue(param)
        # Global temp bool, local temp bool
        elif 22000 <= param < 23000 or 13000 <= param < 14000:
            print("No se puede pasar un valor booleano como parámetro")
            sys.exit()
        # Constantes
        elif 17000 <= param < 18000:
            # topMemNueva.localInt[indexP - 1] = getValue(param)
            print("No se puede pasar un letrero como parámetro")
            sys.exit()

        topMemNueva = pilaNuevaMemoriasLocales[-1]


        currentIp += 1

    # GOSUB
    elif cuadruplos[currentIp][0] == 'GOSUB':
        pilaMemoriasLocales.put(pilaNuevaMemoriasLocales.pop())
        pilaCurrIps.put(currentIp + 1)
        currentIp = cuadruplos[currentIp][3] - 1

    # Ret
    elif cuadruplos[currentIp][0] == 'Ret':
        retorno = cuadruplos[currentIp][3]
        direcRetFunction = cuadruplos[currentIp][1]

        # Asignación a variable global de retorno de funcion
        if 1000 <= direcRetFunction < 2000:
            memoriaGlobal.globalInt[direcRetFunction - 1000] = getValue(retorno)
        elif 2000 <= direcRetFunction < 3000:
            memoriaGlobal.globalFloat[direcRetFunction - 2000] = getValue(retorno)
        elif 3000 <= direcRetFunction < 4000:
            memoriaGlobal.globalC[direcRetFunction - 3000] = getValue(retorno)
        else:
            print("Se está tratando de regresar algo en dirección {}".format(direcRetFunction))
            sys.exit()

        currentIp += 1

    # ENDFUNC
    elif cuadruplos[currentIp][0] == 'ENDFUNC':
        pilaMemoriasLocales.get()
        # # restaurar el current pointer al previo
        currentIp = pilaCurrIps.get()

    # Arreglos 
    # Verify
    elif cuadruplos[currentIp][0] == 'Ver':
        dim = cuadruplos[currentIp][1]
        limSup = cuadruplos[currentIp][3]

        if getValue(dim) >= limSup:
            print("ERROR: Array/Matrix index out of range")
            sys.exit()

        currentIp += 1
        
    # END
    elif cuadruplos[currentIp][0] == 'END':
        print("TERMINO EL PROGRAMA")
        sys.exit()

    else:
        currentIp += 1

