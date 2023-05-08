# Directorio de funciones
# {string, [diferentesTipos]}
# {nombre, [tipoRetorno, direccionVirtualInicio, numeroRecursos, tablaVar]}
# tablaVar = {nombre : [tipo,direccionVirtual]}

import sys

class DirectorioFunciones:
    registrosFunciones = {}
    
    def _init_(self):
        self.registrosFunciones = {}

    @classmethod
    def insertNewScript(self,nameScript):
        self.registrosFunciones[nameScript] = ["void","","",""]
        # print("Inició registro de script {} en Directorio de Funciones \n".format(nameScript))

    @classmethod
    def insertNewFunction(self,nameFunction,returnValue):
        alreadyAFunction = nameFunction in self.registrosFunciones

        if alreadyAFunction:
            print("ERROR: MULTIPLE DECLARATION OF FUNCTION {}".format(nameFunction))
            sys.exit()
        else:
            self.registrosFunciones[nameFunction] = [returnValue,"","",""]
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

        
    @classmethod
    def endScript(self,nameScript):
        self.registrosFunciones.pop(nameScript)
        # print("Se eliminó el script {} del Directorio de Funciones".format(nameScript))

