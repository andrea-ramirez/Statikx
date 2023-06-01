# Directorio de funciones
# {string, [diferentesTipos]}
# {nombre, [tipoRetorno, direccionInicio, numeroRecursos, tablaVar, listaParametros]}
# tablaVar = {nombre : [tipo,direccionVirtual,dim]}

import sys

class DirectorioFunciones:
    registrosFunciones = {}
    currDecArreglo = [0,""] # [arrR,arrListaNodos]
    
    def _init_(self):
        self.registrosFunciones = {}
    
    # Para ver si la variable es local o global. Me regresa el nombre de la funcion actual a checar la tabla de variables a la cual la variable ide pertenece
    @classmethod
    def tablaVarActual(self,nombreVar,currentFunction, currentScript):
        try:
            # Local
            variable = self.registrosFunciones[currentFunction][3][nombreVar]
            return currentFunction
        except:
            variable = self.registrosFunciones[currentScript][3][nombreVar]
            return currentScript

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

        # print("Inició registro de script {} en Directorio de Funciones \n".format(nameScript))

    @classmethod
    def insertNewFunction(self,nameFunction,returnValue):
        alreadyAFunction = nameFunction in self.registrosFunciones

        if alreadyAFunction:
            print("ERROR: MULTIPLE DECLARATION OF FUNCTION {}".format(nameFunction))
            sys.exit()
        else:
            self.registrosFunciones[nameFunction] = [returnValue,"",{},""]
            # print("Se ha insertado al Directorio de Funciones la funcion {} con attributos {}".format(nameFunction,self.registrosFunciones[nameFunction]))

    @classmethod
    def createTablaVar(self,currentScript,currentFunction):
        funcionAgregarTablaVar = ""
        if currentFunction == "":
            funcionAgregarTablaVar = currentScript
        else:
            funcionAgregarTablaVar = currentFunction

        if self.registrosFunciones[funcionAgregarTablaVar][3] == "":
            self.registrosFunciones[funcionAgregarTablaVar][3] = {}
            # print("Se ha creado la tabla de variables de {}".format(funcionAgregarTablaVar))

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

    @classmethod
    def insertarParam(self,currentScript,currentFunction,currentTypeVar):
        funcionCrearListaParam = ""
        if currentFunction == "":
            funcionCrearListaParam = currentScript
        else:
            funcionCrearListaParam = currentFunction
        
        self.registrosFunciones[funcionCrearListaParam][4].append(currentTypeVar)

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
            
            # print("Se ha insertado la variable {} en el registro de {}".format(nameVariable,funcionInsertarVariable))

        # print(self.registrosFunciones[funcionInsertarVariable][3])

    @classmethod
    def isVarDeclared(self,nameVariable,currentScript,currentFunction):
        # checar que sea una variable que ya esté declarada en la funcion o en el script
        funcionActual = ""
        if currentFunction == "":
            funcionActual = currentScript
        else:
            funcionActual = currentFunction

        if nameVariable in self.registrosFunciones[funcionActual][3]:
            return True
        else:
            return False
        
    
    # Funciones de arreglos
        
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

    @classmethod
    def getDirBaseArreglo(self,currentScript,currentFunction,nombreArreglo):
        tablaVarActual = self.tablaVarActual(nombreArreglo,currentFunction,currentScript)
        return self.registrosFunciones[tablaVarActual][3][nombreArreglo][1]
    
    @classmethod
    def getM1(self,currentScript,currentFunction,nombreMatriz):
        tablaVarActual = self.tablaVarActual(nombreMatriz,currentFunction,currentScript)

        # funcion[tablaVAR][arregloID][dimensiones][dim1][m1]

        return int(self.registrosFunciones[tablaVarActual][3][nombreMatriz][2][0][1])
    
    @classmethod
    def getTipoReturnFunction(self,function):
        return self.registrosFunciones[function][0]
    
    @classmethod
    def getVirtualAddress(self,function,variable):
        # print("Address a regresar {}".format(self.registrosFunciones[function][3][variable][1]))
        return self.registrosFunciones[function][3][variable][1]

    @classmethod
    def endScript(self,nameScript):
        self.registrosFunciones.pop(nameScript)
        # print("Se eliminó el script {} del Directorio de Funciones".format(nameScript))

