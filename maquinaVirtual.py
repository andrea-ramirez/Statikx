import lexerParser
import memoriaVirtual
from memoriaVM import MemoriaFuncion
from memoriaVM import MemoriaGlobal
from queue import LifoQueue
import sys


datos = lexerParser.exportData()
cuadruplos = datos['cuads']
dirFunc = datos['dirfunc']
tablaConst = datos['tablaconst']
currentScript = datos['script']
dirsVirtuales = datos['direcciones']

# Para acceder a variables
currentFunction = "" # deberia ser pila

# print(cuadruplos,dirFunc,tablaConst)

# Mapa de memoria
pilaMemoriasLocales = LifoQueue(maxsize=0) # Para mandar a dormir la memoria
memoriaGlobal = MemoriaGlobal()
memoriaLocal = MemoriaFuncion()

memoriaLocal.localInt = ['-'] * 10
memoriaLocal.localFloat = ['-'] * 10
memoriaLocal.localC = ['-'] * 10
memoriaLocal.localDf = ['-'] * 10

memoriaLocal.tempInt = ['-'] * 10
memoriaLocal.tempFloat = ['-'] * 10
memoriaLocal.tempC = ['-'] * 10
memoriaLocal.tempPointer = ['-'] * 10
memoriaLocal.tempBool = ['-'] * 10


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

    pilaMemoriasLocales.put(currentMemoriaLocal)

def resizeMemoriaGlobal(recursosFuncion):
    # memoriaGlobal.globalInt = ['-'] * recursosFuncion['vI']
    # memoriaGlobal.globalFloat = ['-'] * recursosFuncion['vF']
    # memoriaGlobal.globalC = ['-'] * recursosFuncion['vC']
    # memoriaGlobal.globalDf = ['-'] * recursosFuncion['vDf']

    memoriaGlobal.globalInt = ['-'] * 10
    memoriaGlobal.globalFloat = ['-'] * 10
    memoriaGlobal.globalC = ['-'] * 10
    memoriaGlobal.globalDf = ['-'] * 10

    memoriaGlobal.tempInt = ['-'] * 10
    memoriaGlobal.tempFloat = ['-'] * 10
    memoriaGlobal.tempC = ['-'] * 10
    memoriaGlobal.tempPointer = ['-'] * 10
    memoriaGlobal.tempBool = ['-'] * 10

def getConstante(direccion):
    for const in tablaConst.keys():
        if tablaConst[const][1] == direccion:
            if tablaConst[const][0] == '4':
                # Para constantes char
                return chr(const)
            else:
                return const
    print("ERROR: No se encontró {} en tabla de constantes".format(direccion))

def getVariableAddress(nombreVariable):
    if type(nombreVariable) != int:
            #Local
            try:
                direccionVariable = dirFunc[currentFunction][3][nombreVariable]
            except:
                # Global
                direccionVariable = dirFunc[currentScript][3][nombreVariable]
            
            direccionVariable = direccionVariable[1]
            return direccionVariable
    else:
        return nombreVariable
    

def getValue(direccion):
    # Locales
    if currentFunction != "":
        memoriaLocal = pilaMemoriasLocales.get()
        pilaMemoriasLocales.put(memoriaLocal)

        if dirsVirtuales.localInt <= direccion < dirsVirtuales.localFloat:
            # Int
            if memoriaLocal.localInt[direccion - dirsVirtuales.localInt] == '-':
                print("No hay valor en la direccion {} para locales ints".format(direccion))
            return memoriaLocal.localInt[direccion - dirsVirtuales.localInt]
        elif dirsVirtuales.localFloat <= direccion < dirsVirtuales.localC:
            # Float
            if memoriaLocal.localFloat[direccion - dirsVirtuales.localFloat] == '-':
                print("No hay valor en la direccion {} para locales floats".format(direccion))
            return memoriaLocal.localFloat[direccion - dirsVirtuales.localFloat]
        elif dirsVirtuales.localC <= direccion < dirsVirtuales.localDf:
            # Char
            if memoriaLocal.localC[direccion - dirsVirtuales.localC] == '-':
                print("No hay valor en la direccion {} para locales chars".format(direccion))
            return memoriaLocal.localC[direccion - dirsVirtuales.localC]
        elif dirsVirtuales.localDf <= direccion < dirsVirtuales.tempInt:
            # Df
            if memoriaLocal.localDf[direccion - dirsVirtuales.localDf] == '-':
                print("No hay valor en la direccion {} para locales dfs".format(direccion))
            return memoriaLocal.localDf[direccion - dirsVirtuales.localDf]
        # Temporales
        elif dirsVirtuales.tempInt <= direccion < dirsVirtuales.tempFloat:
            # Int
            if memoriaLocal.tempInt[direccion - dirsVirtuales.tempInt] == '-':
                print("No hay valor en la direccion {} para temporales ints".format(direccion))
            return memoriaLocal.tempInt[direccion - dirsVirtuales.tempInt]
        elif dirsVirtuales.tempFloat <= direccion < dirsVirtuales.tempC:
            # Floats
            if memoriaLocal.tempFloat[direccion - dirsVirtuales.tempFloat] == '-':
                print("No hay valor en la direccion {} para temporales floats".format(direccion))
            return memoriaLocal.tempFloat[direccion - dirsVirtuales.tempFloat]
        elif dirsVirtuales.tempC <= direccion < dirsVirtuales.tempPointer:
            # C
            if memoriaLocal.tempC[direccion - dirsVirtuales.tempC] == '-':
                print("No hay valor en la direccion {} para temporales chars".format(direccion))
            return memoriaLocal.tempC[direccion - dirsVirtuales.tempC]
        elif dirsVirtuales.tempPointer <= direccion < dirsVirtuales.tempB:
            # Pointers
            if memoriaLocal.tempPointer[direccion - dirsVirtuales.tempPointer] == '-':
                print("No hay valor en la direccion {} para temporales pointers".format(direccion))
            return memoriaLocal.tempPointer[direccion - dirsVirtuales.tempPointer]
        elif dirsVirtuales.tempB <= direccion < (dirsVirtuales.tempB+1000):
            # Booleans
            if memoriaLocal.tempB[direccion - dirsVirtuales.tempB] == '-':
                print("No hay valor en la direccion {} para temporales booleans".format(direccion))
            return memoriaLocal.tempB[direccion - dirsVirtuales.tempB]
        
    
    # Globales
    elif dirsVirtuales.globalInt <= direccion < dirsVirtuales.globalFloat:
        # Int
        if memoriaGlobal.globalInt[direccion - dirsVirtuales.globalInt] == '-':
            print("No hay valor en la direccion {} para gloables ints".format(direccion))
        return memoriaGlobal.globalInt[direccion - dirsVirtuales.globalInt]
    elif dirsVirtuales.globalFloat <= direccion < dirsVirtuales.globalC:
        # Float
        if memoriaGlobal.globalFloat[direccion - dirsVirtuales.globalFloat] == '-':
            print("No hay valor en la direccion {} para gloables floats".format(direccion))
        return memoriaGlobal.globalFloat[direccion - dirsVirtuales.globalFloat]
    elif dirsVirtuales.globalC <= direccion < dirsVirtuales.globalDf:
        # C
        if memoriaGlobal.globalC[direccion - dirsVirtuales.globalC] == '-':
            print("No hay valor en la direccion {} para gloables chars".format(direccion))
        return memoriaGlobal.globalC[direccion - dirsVirtuales.globalC]
    elif dirsVirtuales.globalDf <= direccion < (dirsVirtuales.globalDf+1000):
        # Df
        if memoriaGlobal.globalDf[direccion - dirsVirtuales.globalDf] == '-':
            print("No hay valor en la direccion {} para gloables dfs".format(direccion))
        return memoriaGlobal.globalDf[direccion - dirsVirtuales.globalDf]
    # Temporales globales
    elif 9000 <= direccion < 10000:
        # Int
        if memoriaGlobal.tempInt[direccion - 9000] == '-':
            print("No hay valor en la direccion {} para temporales globales ints".format(direccion))
        return memoriaGlobal.tempInt[direccion - 9000]
    elif 10000 <= direccion < 11000:
        # Float
        if memoriaGlobal.tempFloat[direccion - 10000] == '-':
            print("No hay valor en la direccion {} para temporales globales floats".format(direccion))
        return memoriaGlobal.tempFloat[direccion - 10000]
    elif 11000 <= direccion < 12000:
        # C
        if memoriaGlobal.tempC[direccion - 11000] == '-':
            print("No hay valor en la direccion {} para temporales globales chars".format(direccion))
        return memoriaGlobal.tempC[direccion - 11000]
    elif 12000 <= direccion < 13000:
        # Pointer
        if memoriaGlobal.tempPointer[direccion - 12000] == '-':
            print("No hay valor en la direccion {} para temporales globales pointers".format(direccion))
        return memoriaGlobal.tempPointer[direccion - 12000]
    elif 13000 <= direccion < 14000:
        # Pointer
        if memoriaGlobal.tempBool[direccion - 13000] == '-':
            print("No hay valor en la direccion {} para temporales globales booleanos".format(direccion))
        return memoriaGlobal.tempBool[direccion - 13000]
    
    #Constantes
    else:
        return getConstante(direccion)

def printPilaMemoriasLocales():
    index = 0
    for mem in list(pilaMemoriasLocales.queue):
        print("MEMORIA {}".format(index))
        mem.print()


# Procesador
currentIp = 0

while currentIp < len(cuadruplos):

    # GOTO
    if cuadruplos[currentIp][0] == 'Goto':
        # Goto Main
        try:
            if cuadruplos[currentIp][3] != int:
                currentIp = dirFunc[cuadruplos[currentIp][3]][1] - 1
                resizeMemoriaGlobal("recursosfnucion")
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

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 9000 <= resp < 10000:
            # temp int
                memoriaGlobal.tempInt[resp-9000] = getValue(elemIzq) + getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaGlobal.tempFloat[resp-10000] = getValue(elemIzq) + getValue(elemDer)
            elif 12000 <= resp < 13000:
            # temp pointer
                memoriaGlobal.tempPointer[resp-12000] = getValue(elemIzq) + getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()
        # Local
        else:
            if 9000 <= resp < 10000:
            # temp int
                memoriaLocal.tempInt[resp-9000] = getValue(elemIzq) + getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaLocal.tempFloat[resp-10000] = getValue(elemIzq) + getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()

        currentIp += 1

    # MINUS
    elif cuadruplos[currentIp][0] == '-':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 9000 <= resp < 10000:
            # temp int
                memoriaGlobal.tempInt[resp-9000] = getValue(elemIzq) - getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaGlobal.tempFloat[resp-10000] = getValue(elemIzq) - getValue(elemDer)
            elif 12000 <= resp < 13000:
            # temp pointer
                memoriaGlobal.tempPointer[resp-12000] = getValue(elemIzq) - getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()
        # Local
        else:
            if 9000 <= resp < 10000:
            # temp int
                memoriaLocal.tempInt[resp-9000] = getValue(elemIzq) - getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaLocal.tempFloat[resp-10000] = getValue(elemIzq) - getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()

        currentIp += 1

    # MULT
    elif cuadruplos[currentIp][0] == '*':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 9000 <= resp < 10000:
            # temp int
                memoriaGlobal.tempInt[resp-9000] = getValue(elemIzq) * getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaGlobal.tempFloat[resp-10000] = getValue(elemIzq) * getValue(elemDer)
            elif 12000 <= resp < 13000:
            # temp pointer
                memoriaGlobal.tempPointer[resp-12000] = getValue(elemIzq) * getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()
        # Local
        else:
            if 9000 <= resp < 10000:
            # temp int
                memoriaLocal.tempInt[resp-9000] = getValue(elemIzq) * getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaLocal.tempFloat[resp-10000] = getValue(elemIzq) * getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()

        currentIp += 1

    # DIV
    elif cuadruplos[currentIp][0] == '/':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        if getValue(elemDer) == 0:
            print("No se puede dividir entre 0")
            sys.exit()

        # Global
        if currentFunction == "":
            if 9000 <= resp < 10000:
            # temp int
                memoriaGlobal.tempInt[resp-9000] = getValue(elemIzq) / getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaGlobal.tempFloat[resp-10000] = getValue(elemIzq) / getValue(elemDer)
            elif 12000 <= resp < 13000:
            # temp pointer
                memoriaGlobal.tempPointer[resp-12000] = getValue(elemIzq) / getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()
        # Local
        else:
            if 9000 <= resp < 10000:
            # temp int
                memoriaLocal.tempInt[resp-9000] = getValue(elemIzq) / getValue(elemDer)
            elif 10000 <= resp < 11000:
            # temp float
                memoriaLocal.tempFloat[resp-10000] = getValue(elemIzq) / getValue(elemDer)
            else:
                print("ALGO MAL")
                sys.exit()

        currentIp += 1

    # MAYOR QUE
    elif cuadruplos[currentIp][0] == '>':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 13000 <= resp < 14000:
            # temp bool
                memoriaGlobal.tempBool[resp-13000] = getValue(elemIzq) > getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()
        # Local
        else:
            if 13000 <= resp < 14000:
            # temp bool
                memoriaLocal.tempBool[resp-13000] = getValue(elemIzq) > getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()

        currentIp += 1

    # MENOR QUE
    elif cuadruplos[currentIp][0] == '<':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 13000 <= resp < 14000:
            # temp bool
                memoriaGlobal.tempBool[resp-13000] = getValue(elemIzq) < getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()
        # Local
        else:
            if 13000 <= resp < 14000:
            # temp bool
                memoriaLocal.tempBool[resp-13000] = getValue(elemIzq) < getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()

        currentIp += 1

    # EQUALS
    elif cuadruplos[currentIp][0] == '==':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 13000 <= resp < 14000:
            # temp bool
                memoriaGlobal.tempBool[resp-13000] = getValue(elemIzq) == getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()
        # Local
        else:
            if 13000 <= resp < 14000:
            # temp bool
                memoriaLocal.tempBool[resp-13000] = getValue(elemIzq) == getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()

        currentIp += 1

    # NOT EQUALS
    elif cuadruplos[currentIp][0] == '!=':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 13000 <= resp < 14000:
            # temp bool
                memoriaGlobal.tempBool[resp-13000] = getValue(elemIzq) != getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()
        # Local
        else:
            if 13000 <= resp < 14000:
            # temp bool
                memoriaLocal.tempBool[resp-13000] = getValue(elemIzq) != getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()

        currentIp += 1

    # AND
    elif cuadruplos[currentIp][0] == '&&':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 13000 <= resp < 14000:
            # temp bool
                memoriaGlobal.tempBool[resp-13000] = getValue(elemIzq) and getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()
        # Local
        else:
            if 13000 <= resp < 14000:
            # temp bool
                memoriaLocal.tempBool[resp-13000] = getValue(elemIzq) and getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()

        currentIp += 1

    # OR
    elif cuadruplos[currentIp][0] == '||':
        elemIzq = cuadruplos[currentIp][1]
        elemDer = cuadruplos[currentIp][2]
        resp = cuadruplos[currentIp][3]

        elemIzq = getVariableAddress(elemIzq)
        elemDer = getVariableAddress(elemDer)

        # Global
        if currentFunction == "":
            if 13000 <= resp < 14000:
            # temp bool
                memoriaGlobal.tempBool[resp-13000] = getValue(elemIzq) or getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()
        # Local
        else:
            if 13000 <= resp < 14000:
            # temp bool
                memoriaLocal.tempBool[resp-13000] = getValue(elemIzq) or getValue(elemDer)
            else:
                print("COMBINACION NO ESPERADA")
                sys.exit()

        currentIp += 1
        

    # ASIGN
    elif cuadruplos[currentIp][0] == '=':
        valor = cuadruplos[currentIp][1]
        aAsignar = cuadruplos[currentIp][3]

        valor = getVariableAddress(valor)
        aAsignar = getVariableAddress(aAsignar)

        if currentFunction == "":
            # Global int
            if 1000 <= aAsignar < 2000:
                # global int
                if 1000 <= valor < 2000:
                    memoriaGlobal.globalInt[aAsignar - 1000] = memoriaGlobal.globalInt[valor - 1000]
                # local int
                elif 5000 <= valor < 6000:
                    memoriaGlobal.globalInt[aAsignar - 1000] = memoriaLocal.localInt[valor - 5000]
                # global temp int
                elif 9000 <= valor < 10000: # Checar
                    memoriaGlobal.globalInt[aAsignar - 1000] = memoriaGlobal.tempInt[valor - 9000]
                # local temp int # Checar
                elif 9000 <= valor < 10000:
                    memoriaGlobal.globalInt[aAsignar - 1000] = memoriaLocal.tempInt[valor - 9000]
                # const int
                elif 14000 <= valor < 15000:
                    memoriaGlobal.globalInt[aAsignar - 1000] = getConstante(valor)
                else:
                    print("FALTA A IMPLEMENTAR")
                    sys.exit()
            # Global Float
            elif 2000 <= aAsignar < 3000:
                # global float
                if 2000 <= valor < 3000:
                    memoriaGlobal.globalFloat[aAsignar - 2000] = memoriaGlobal.globalFloat[valor - 2000]
                # local float
                elif 6000 <= valor < 7000:
                    memoriaGlobal.globalFloat[aAsignar - 2000] = memoriaLocal.localFloat[valor - 6000]
                # global temp float
                elif 10000 <= valor < 11000: # Checar
                    memoriaGlobal.globalFloat[aAsignar - 2000] = memoriaGlobal.tempFloat[valor - 10000]
                # local temp float # Checar
                elif 9000 <= valor < 10000:
                    memoriaGlobal.globalFloat[aAsignar - 2000] = memoriaLocal.tempFloat[valor - 10000]
                # const float
                elif 15000 <= valor < 16000:
                    memoriaGlobal.globalFloat[aAsignar - 2000] = getConstante(valor)
                else:
                    print("FALTA A IMPLEMENTAR")
                    sys.exit()
            else:
                print("FALTA IMPLEMENTAR ASIGN CON {} TIPO DE VALOR".format(aAsignar))
        else:
            # Local int
            if 5000 <= aAsignar < 6000:
                # temp int # Checar
                if 9000 <= valor < 10000:
                    memoriaLocal.localInt[aAsignar - 5000] = memoriaLocal.tempInt[valor - 9000]
                # const int
                elif 14000 <= valor < 15000:
                    memoriaLocal.localInt[aAsignar - 5000] = getConstante(valor)
                else:
                    print("FALTA A IMPLEMENTAR")
                    sys.exit()
        
        currentIp += 1

    # PRINT
    elif cuadruplos[currentIp][0] == 'put':
        toPrint = cuadruplos[currentIp][3]
        toPrint = getVariableAddress(toPrint)

        if 14000 <= toPrint < 18000:
            toPrint = getConstante(toPrint)
            print("Statikx >> {}".format(toPrint))
        else:
            print("Statikx >> {}".format(getValue(toPrint)))
        currentIp += 1


    # FUNCTIONS

    #ERA
    elif cuadruplos[currentIp][0] == 'ERA':
        print("HAY UN ERA")
        nombreFunc = cuadruplos[currentIp][3]
        recursosFuncion = dirFunc[nombreFunc][2]

        createMemoriaLocal(recursosFuncion)
        # printPilaMemoriasLocales()
        currentIp += 1


    else:
        currentIp += 1

print("TERMINO EL PROGRAMA")


    