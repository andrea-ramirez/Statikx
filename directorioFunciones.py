# Directorio de funciones
# {nombre, [tipoRetorno, direccionInicio, numeroRecursos, tablaVar, listaParametros]}
# tablaVar = {nombre : [tipo,direccionVirtual,dim]}

import sys

# Clase que registra las funciones de un script

class DirectorioFunciones:
    registrosFunciones = {}
    currDecArreglo = [0,""] # [arrR,arrListaNodos]
    
    def _init_(self):
        self.registrosFunciones = {}

    # Función que inicializa un nuevo script en el directorio de funciones
    @classmethod
    def insertNewScript(self,nameScript):
        # Se crea con tabla de variables ya inicializada
        self.registrosFunciones[nameScript] = ["void","",{},{}]
        # Se inicializa el diccionario de recursos del script
        recursosScript = self.registrosFunciones[nameScript][2]
        if recursosScript == {}:
            recursosScript['vI'] = 0
            recursosScript['vF'] = 0
            recursosScript['vC'] = 0
            recursosScript['vDf'] = 0
            recursosScript['tI'] = 0
            recursosScript['tF'] = 0
            recursosScript['tC'] = 0
            recursosScript['tPointer'] = 0
            recursosScript['tB'] = 0

    # Función que inserta una nueva función al directorio de funciones
    # Chequea que no exista una función con ese mismo nombre
    @classmethod
    def insertNewFunction(self,nameFunction,returnValue):
        alreadyAFunction = nameFunction in self.registrosFunciones

        if alreadyAFunction:
            print("ERROR: MULTIPLE DECLARATION OF FUNCTION {}".format(nameFunction))
            sys.exit()
        else:
            self.registrosFunciones[nameFunction] = [returnValue,"",{},""]
            # print("Se ha insertado al Directorio de Funciones la funcion {} con attributos {}".format(nameFunction,self.registrosFunciones[nameFunction]))

    # Función que inicializa la tabla de variables para una función del directorio, si todavía no cuenta con una
    # También inicializa el diccionario para conteo de recursos
    @classmethod
    def createTablaVar(self,currentScript,currentFunction):
        funcionAgregarTablaVar = ""
        if currentFunction == "":
            funcionAgregarTablaVar = currentScript
        else:
            funcionAgregarTablaVar = currentFunction

        if self.registrosFunciones[funcionAgregarTablaVar][3] == "":
            self.registrosFunciones[funcionAgregarTablaVar][3] = {}

        #También inicializa el diccionario de recursos de la funcion
        recursosFuncion = self.registrosFunciones[funcionAgregarTablaVar][2]
        if recursosFuncion == {}:
            recursosFuncion['vI'] = 0
            recursosFuncion['vF'] = 0
            recursosFuncion['vC'] = 0
            recursosFuncion['vDf'] = 0
            recursosFuncion['tI'] = 0
            recursosFuncion['tF'] = 0
            recursosFuncion['tC'] = 0
            recursosFuncion['tPointer'] = 0
            recursosFuncion['tB'] = 0


    # Crea lista de parámetros
    @classmethod
    def createListaParam(self, currentScript,currentFunction):
        funcionCrearListaParam = ""
        if currentFunction == "":
            funcionCrearListaParam = currentScript
        else:
            funcionCrearListaParam = currentFunction

        self.registrosFunciones[funcionCrearListaParam].append([0])

    # Función que inserta tipo de parámetro en la lista paramétrica
    @classmethod
    def insertarParam(self,currentScript,currentFunction,currentTypeVar):
        funcionCrearListaParam = ""
        if currentFunction == "":
            funcionCrearListaParam = currentScript
        else:
            funcionCrearListaParam = currentFunction
        
        self.registrosFunciones[funcionCrearListaParam][4].append(currentTypeVar)

    # Función que inserta una variable a la tabla de variables de la función actual
    @classmethod
    def insertVariable(self,nameVariable,returnValue,currentScript,currentFunction):
        funcionInsertarVariable = ""
        if currentFunction == "":
            funcionInsertarVariable = currentScript
        else:
            funcionInsertarVariable = currentFunction

        # Número 3 apunta a tabla de variables de la funcion funcionInsertarVariable
        alreadyAVariable = nameVariable in self.registrosFunciones[funcionInsertarVariable][3]

        if alreadyAVariable:
            print("ERROR: MULTIPLE DECLARATION OF VARIABLE {} in {}".format(nameVariable,funcionInsertarVariable))
            sys.exit()
        else:
            #insertar valor a tabla de variables
            self.registrosFunciones[funcionInsertarVariable][3][nameVariable] = [returnValue,"direccionVirtual"]

    # Funciones de arreglos
    
    # Función que regresa si una variable es local o global. Me regresa el nombre de la funcion actual a checar la tabla de variables a la cual la variable ide pertenece
    @classmethod
    def tablaVarActual(self,nombreVar,currentFunction, currentScript):
        try:
            # Local
            variable = self.registrosFunciones[currentFunction][3][nombreVar]
            return currentFunction
        except:
            variable = self.registrosFunciones[currentScript][3][nombreVar]
            return currentScript
    
    # Función booleana que checa si una variable es dimensionada o no
    @classmethod
    def isDim(self,ide, currentScript, currentFunction):
        tablaVarIde = self.tablaVarActual(ide,currentFunction, currentScript)

        if len(self.registrosFunciones[tablaVarIde][3][ide]) > 2:
            return True
        else:
            return False
    
    # Regresa el limite superior de un arreglo de una dimension dada
    @classmethod
    def getLimSup(self,currentScript,currentFunction,nombreArreglo,dimension):
        # Trae la funcion de la tabla con la que se tiene que checar, la funcion actual o el script
        tablaVarActual = self.tablaVarActual(nombreArreglo,currentFunction,currentScript)

        if dimension == 1:
                                        # func[tablaVar][arreglo][dimensiones][dim1][limpSup]
            return self.registrosFunciones[tablaVarActual][3][nombreArreglo][2][0][0]
        elif dimension == 2:
                                        # func[tablaVar][arreglo][dimensiones][dim2][limpSup]
            return self.registrosFunciones[tablaVarActual][3][nombreArreglo][2][1][0]
        else:
            print("ERROR: No se pudo acceder con la dimension {} al arreglo {}".format(dimension,nombreArreglo))
            sys.exit()

    # Función que regresa la dirección base de una variable dimensionada
    @classmethod
    def getDirBaseArreglo(self,currentScript,currentFunction,nombreArreglo):
        tablaVarActual = self.tablaVarActual(nombreArreglo,currentFunction,currentScript)
        return self.registrosFunciones[tablaVarActual][3][nombreArreglo][1]
    
    # Función que regresa el tipo de una variable dimensionada
    @classmethod
    def getTipoArrreglo(self,currentScript,currentFunction,nombreArreglo):
        tablaVarActual = self.tablaVarActual(nombreArreglo,currentFunction,currentScript)
        return self.registrosFunciones[tablaVarActual][3][nombreArreglo][0]
    
    # Función que regresa y castea a int, la m de las variables con dos dimensiones
    @classmethod
    def getM1(self,currentScript,currentFunction,nombreMatriz):
        tablaVarActual = self.tablaVarActual(nombreMatriz,currentFunction,currentScript)

        # funcion[tablaVAR][arregloID][dimensiones][dim1][m1]

        return int(self.registrosFunciones[tablaVarActual][3][nombreMatriz][2][0][1])
    
    # Función que regresa el tipo de retorno de una función
    @classmethod
    def getTipoReturnFunction(self,function):
        return self.registrosFunciones[function][0]
    
    # Función que regresa la dirección base de una variable global para parche guadalupano
    @classmethod
    def getVirtualAddress(self,function,variable):
        return self.registrosFunciones[function][3][variable][1]

