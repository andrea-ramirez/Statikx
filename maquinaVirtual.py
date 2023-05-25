import lexerParser
import memoriaVirtual

datos = lexerParser.exportData()
cuadruplos = datos['cuads']
dirFunc = datos['dirfunc']
tablaConst = datos['tablaconst']

print(cuadruplos,dirFunc,tablaConst)

# Mapa de memoria

#Definir vectores de cada memoria, cambiar size dependiendo de qué necesite
memGlInt = []
memGlFloat = []
memGlC = []
memGlDf = []

memLocInt = []
memLocFloat = []
memLocC = []
memLocDf = []

memTempInt = []
memTempFloat = []
memTempC = []
memTempDf = []
memTempBool = []

memCteInt = []
memCteFloat = []
memCteC = []
memCteLetrero = [] # creo que no necesito esta, porque ya tengo mi tabla de variables

# Procesador
# currentIp = 0

# if cuadruplos[currentIp][0] == '+':
#     elemIzq = cuadruplos[currentIp][1]
#     elemDer = cuadruplos[currentIp][2]
    