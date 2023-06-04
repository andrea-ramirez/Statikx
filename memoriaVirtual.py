import sys

# Clase que define los rangos para el direccionamiento de variables

class MemoriaVirtual:
    #Rangos
    globalInt = 1000
    globalFloat = 2000
    globalC = 3000
    globalDf = 4000
    countGlInt = 1000
    countGlFloat = 2000
    countGlC = 3000
    countGlDf = 4000

    globalTempInt = 18000
    globalTempFloat = 19000
    globalTempC = 20000
    globalTempPointer = 21000
    globalTempBool = 22000
    countGlTempInt = 18000
    countGlTempFloat = 19000
    countGlTempC = 20000
    countGlTempPointer = 21000
    countGlTempBool = 22000

    localInt = 5000
    localFloat = 6000
    localC = 7000
    localDf = 8000
    countLocInt = 5000
    countLocFloat = 6000
    countLocC = 7000
    countLocDf = 8000

    tempInt = 9000
    tempFloat = 10000
    tempC = 11000
    tempPointer = 12000
    tempBool = 13000
    countTemInt = 9000
    countTemFloat = 10000
    countTemC = 11000
    countTemPointer = 12000
    countTemBool = 13000

    CteInt = 14000
    CteFloat = 15000
    CteC = 16000
    CteLetrero = 17000
    countCteInt = 14000
    countCteFloat = 15000
    countCteC = 16000
    countCteLetrero = 17000


    def _init_(self):
        self.globalInt = 1000
        self.globalFloat = 2000
        self.globalC = 3000
        self.globalDf = 4000
        self.countGlInt = 1000
        self.countGlFloat = 2000
        self.countGlC = 3000
        self.countGlDf = 4000

        self.globalTempInt = 18000
        self.globalTempFloat = 19000
        self.globalTempC = 20000
        self.globalTempPointer = 21000
        self.globalTempBool = 22000
        self.countGlTempInt = 18000
        self.countGlTempFloat = 19000
        self.countGlTempC = 20000
        self.countGlTempPointer = 21000
        self.countGlTempBool = 22000

        self.localInt = 5000
        self.localFloat = 6000
        self.localC = 7000
        self.localDf = 8000
        self.countLocInt = 5000
        self.countLocFloat = 6000
        self.countLocC = 7000
        self.countLocDf = 8000

        self.tempInt = 9000
        self.tempFloat = 10000
        self.tempC = 11000
        self.tempPointer = 12000
        self.tempBool = 13000
        self.countTemInt = 9000
        self.countTemFloat = 10000
        self.countTemC = 11000
        self.countTemPointer = 12000
        self.countTemBool = 13000

        self.CteInt = 14000
        self.CteFloat = 15000
        self.CteC = 16000
        self.CteLetrero = 17000,
        self.countCteInt = 14000
        self.countCteFloat = 15000
        self.countCteC = 16000
        self.countCteLetrero = 17000

    # Función que regresa la siguiente dirección virtual de memoria displonible
    def getMemoriaTemporal(self,resultType,isLocal):
        temp = ""
        if resultType == 1:
            if isLocal:
                if self.countTemBool < (self.tempBool + 1000):
                    temp = self.countTemBool
                    self.countTemBool += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales locales booleanos")
                    sys.exit()
            else:
                if self.countGlTempBool < (self.globalTempBool + 1000):
                    temp = self.countGlTempBool
                    self.countGlTempBool += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales globales booleanos")
                    sys.exit()
        elif resultType == 2:
            if isLocal:
                if self.countTemInt < (self.tempInt + 1000):
                    temp = self.countTemInt
                    self.countTemInt += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales locales ints")
                    sys.exit()
            else:
                if self.countGlTempInt < (self.globalTempInt + 1000):
                    temp = self.countGlTempInt
                    self.countGlTempInt += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales globales ints")
                    sys.exit()
        elif resultType == 3:
            if isLocal:
                if self.countTemFloat < (self.tempFloat + 1000):
                    temp = self.countTemFloat
                    self.countTemFloat += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales locales floats")
                    sys.exit()
            else:
                if self.countGlTempFloat < (self.globalTempFloat + 1000):
                    temp = self.countGlTempFloat
                    self.countGlTempFloat += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales globales floats")
                    sys.exit()
        elif resultType == 4:
            if isLocal:
                if self.countTemC < (self.tempC + 1000):
                    temp = self.countTemC
                    self.countTemC += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales locales chars")
                    sys.exit()
            else:
                if self.countGlTempC < (self.globalTempC + 1000):
                    temp = self.countGlTempC
                    self.countGlTempC += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales globales chars")
                    sys.exit()
        elif resultType == 'pointer':
            if isLocal:
                if self.countTemPointer < (self.tempPointer + 1000):
                    temp = self.countTemPointer
                    self.countTemPointer += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales locales pointers")
                    sys.exit()
            else:
                if self.countGlTempPointer < (self.globalTempPointer + 1000):
                    temp = self.countGlTempPointer
                    self.countGlTempPointer += 1
                else:
                    print("ERROR: Stack overflow. No hay más espacio para temporales globales pointers")
                    sys.exit()
        else:
            print("ERROR AL ASIGNAR TEMPORAL")
            sys.exit()

        return temp
    
    # Función que cambia los contadores de recursos a su estado original
    def reset(self):
        self.countLocInt = 5000
        self.countLocFloat = 6000
        self.countLocC = 7000
        self.countLocDf = 8000

        self.countTemInt = 9000
        self.countTemFloat = 10000
        self.countTemC = 11000
        self.countTemDf = 12000
        self.countTemBool = 13000

    # Función que checa si una nueva variable llena el stack
    # No checa stack para temporales
    def isOverflow(self):
        if self.countGlInt >= (self.globalInt + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countGlFloat >= (self.globalFloat + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countGlC >= (self.globalC + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countGlDf >= (self.globalDf + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countLocInt >= (self.localInt + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countLocFloat >= (self.localFloat + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countLocC >= (self.localC + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()
        elif self.countLocDf >= (self.localDf + 1000):
            print("ERROR: Stack Overflow.")
            sys.exit()

    # Función que checa si una nueva constante llena el stack
    def isOverflowConstants(self):
        if self.countCteInt >= (self.CteInt + 1000):
            print("ERROR: Stack Overflow in constants.")
            sys.exit()
        elif self.countCteFloat >= (self.CteFloat + 1000):
            print("ERROR: Stack Overflow in constants.")
            sys.exit()
        elif self.countCteC >= (self.CteC + 1000):
            print("ERROR: Stack Overflow in constants.")
            sys.exit()
        elif self.countCteLetrero >= (self.CteLetrero + 1000):
            print("ERROR: Stack Overflow in constants.")
            sys.exit()