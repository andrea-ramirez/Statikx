import sys

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
    tempPointer = 12000 # TEMPORAL POINTER
    tempBool = 13000
    countTemInt = 9000
    countTemFloat = 10000
    countTemC = 11000
    countTemPointer = 12000 # TEMPORAL POINTER
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
        self.tempPointer = 12000 # Temp Pointer
        self.tempBool = 13000
        self.countTemInt = 9000
        self.countTemFloat = 10000
        self.countTemC = 11000
        self.countTemPointer = 12000 # Temp Pointer
        self.countTemBool = 13000

        self.CteInt = 14000
        self.CteFloat = 15000
        self.CteC = 16000
        self.CteLetrero = 17000,
        self.countCteInt = 14000
        self.countCteFloat = 15000
        self.countCteC = 16000
        self.countCteLetrero = 17000

    def getMemoriaTemporal(self,resultType,isLocal):
        temp = ""
        print(resultType)
        if resultType == 1:
            if isLocal:
                temp = self.countTemBool
                self.countTemBool += 1
            else:
                temp = self.countGlTempBool
                self.countGlTempBool += 1
        elif resultType == 2:
            if isLocal:
                temp = self.countTemInt
                self.countTemInt += 1
            else:
                temp = self.countGlTempInt
                self.countGlTempInt += 1
        elif resultType == 3:
            if isLocal:
                temp = self.countTemFloat
                self.countTemFloat += 1
            else:
                temp = self.countGlTempFloat
                self.countGlTempFloat += 1
        elif resultType == 4:
            if isLocal:
                temp = self.countTemC
                self.countTemC += 1
            else:
                temp = self.countGlTempC
                self.countGlTempC += 1
        elif resultType == 'pointer':
            if isLocal:
                temp = self.countTemPointer
                self.countTemPointer += 1
            else:
                temp = self.countGlTempPointer
                self.countGlTempPointer += 1
        else:
            print("ERROR AL ASIGNAR TEMPORAL")
            sys.exit()

        return temp
    
    def reset(self):
        self.countGlInt = 1000
        self.countGlFloat = 2000
        self.countGlC = 3000
        self.countGlDf = 4000

        self.countLocInt = 5000
        self.countLocFloat = 6000
        self.countLocC = 7000
        self.countLocDf = 8000

        self.countTemInt = 9000
        self.countTemFloat = 10000
        self.countTemC = 11000
        self.countTemDf = 12000
        self.countTemBool = 13000

