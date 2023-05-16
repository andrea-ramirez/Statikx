import sys

class MemoriaVirtual:
    #Rangos
    globalInt = 1000,
    globalFloat = 2000,
    globalC = 3000,
    globalDf = 4000,
    countGlInt = 1000
    countGlFloat = 2000
    countGlC = 3000
    countGlDf = 4000

    localInt = 5000,
    localFloat = 6000,
    localC = 7000,
    localDf = 8000,
    countLocInt = 5000
    countLocFloat = 6000
    countLocC = 7000
    countLocDf = 8000

    tempInt = 9000,
    tempFloat = 10000,
    tempC = 11000,
    tempDf = 12000, # not sure if I need this one
    tempBool = 13000,
    countTemInt = 9000
    countTemFloat = 10000
    countTemC = 11000
    countTemDf = 12000
    countTemBool = 13000

    CteInt = 14000,
    CteFloat = 15000,
    CteC = 16000,
    CteLetrero = 17000,
    countCteInt = 14000
    countCteFloat = 15000
    countCteC = 16000
    countCteLetrero = 17000

    def _init_(self):
        self.globalInt = 1000,
        self.globalFloat = 2000,
        self.globalC = 3000,
        self.globalDf = 4000,
        self.countGlInt = 1000
        self.countGlFloat = 2000
        self.countGlC = 3000
        self.countGlDf = 4000

        self.localInt = 5000,
        self.localFloat = 6000,
        self.localC = 7000,
        self.localDf = 8000,
        self.countLocInt = 5000
        self.countLocFloat = 6000
        self.countLocC = 7000
        self.countLocDf = 8000

        self.tempInt = 9000,
        self.tempFloat = 10000,
        self.tempC = 11000,
        self.tempDf = 12000, # not sure if I need this one
        self.tempBool = 13000,
        self.countTemInt = 9000
        self.countTemFloat = 10000
        self.countTemC = 11000
        self.countTemDf = 12000
        self.countTemBool = 13000

        self.CteInt = 14000,
        self.CteFloat = 15000,
        self.CteC = 16000,
        self.CteLetrero = 17000,
        self.countCteInt = 14000
        self.countCteFloat = 15000
        self.countCteC = 16000
        self.countCteLetrero = 17000

    def getMemoriaTemporal(self,resultType):
        temp = ""
        print(resultType)
        if resultType == 1:
            temp = self.countTemBool
            self.countTemBool += 1
        elif resultType == 2:
            temp = self.countTemInt
            self.countTemInt += 1
        elif resultType == 3:
            temp = self.countTemFloat
            self.countTemFloat += 1
        elif resultType == 4:
            temp = self.countTemC
            self.countTemC += 1
        elif resultType == 4:
            temp = self.countTemDf
            self.countTemDf += 1
        else:
            print("ERROR AL ASIGNAR TEMPORAL")
            sys.exit()

        return temp


