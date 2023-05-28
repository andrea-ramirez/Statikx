class MemoriaFuncion:
    localInt = []
    localFloat = []
    localC = []
    localDf = []
    
    tempInt = []
    tempFloat = []
    tempC = []
    tempPointer = []
    tempBool = []

    def _init_(self):
        self.localInt = []
        self.localFloat = []
        self.localC = []
        self.localDf = []

        self.tempInt = []
        self.tempFloat = []
        self.tempC = []
        self.tempPointer = []
        self.tempBool = []

    def print(self):
        print("Memoria locales enteros: {}".format(self.localInt))
        print("Memoria locales floats: {}".format(self.localFloat))
        print("Memoria locales chars: {}".format(self.localC))
        print("Memoria locales dfs: {}".format(self.localDf))

        print("Memoria temporales enteros: {}".format(self.tempInt))
        print("Memoria temporales floats: {}".format(self.tempFloat))
        print("Memoria temporales chars: {}".format(self.tempC))
        print("Memoria temporales pointers: {}".format(self.tempPointer))
        print("Memoria temporales booleanos: {}".format(self.tempBool))



class MemoriaGlobal:
    globalInt = []
    globalFloat = []
    globalC = []
    globalDf = []

    tempInt = []
    tempFloat = []
    tempC = []
    tempPointer = []
    tempBool = []

    def _init_(self):
        self.globalInt = []
        self.globalFloat = []
        self.globalC = []
        self.globalDf  =[]

        self.tempInt = []
        self.tempFloat = []
        self.tempC = []
        self.tempPointer = []
        self.tempBool = []

    def print(self):
        print(self.globalInt)
        print(self.globalFloat)
        print(self.globalC)
        print(self.globalDf)

        print(self.tempInt)
        print(self.tempFloat)
        print(self.tempC)
        print(self.tempPointer)
        print(self.tempBool)


        