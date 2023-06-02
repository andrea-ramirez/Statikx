import ply.lex as lex
import ply.yacc as yacc
from cuboSemantico import CuboSemantico
from directorioFunciones import DirectorioFunciones
import codecs
import json
from queue import LifoQueue
from cuadruplos import Cuadruplo
import sys
from memoriaVirtual import MemoriaVirtual

# Tabla de constantes
# {nombre, tipo, direccionVirtual} Por ahora guardo el tipo, mientas no tenga el número de memoria con que checar el rango, o sea el tipo
tablaConst = {}

# Cubo Semántico
semantica = CuboSemantico()
# Se accede al cubo semantico de la siguiente forma:
# print(semantica.tablaSimbolos[2][2]['+'])

currentScript = ""
currentFunction = ""
currentTypeVar = ""
currentLlamada = ""
currentDecID = ""
arrSize = 1

cuadruplos = Cuadruplo()

pilaOperadores = LifoQueue(maxsize=0)
pilaOperandos = LifoQueue(maxsize=0)
pilaTipo = LifoQueue(maxsize=0)
pilaSaltos = LifoQueue(maxsize=0)
pilaDim = LifoQueue(maxsize=0)

# Iniciar Memoria virtual
memoria = MemoriaVirtual()

# For loop - debo cambiar a pila
pilaVControlLoop = LifoQueue(maxsize=0)

#  LEXER
reserved = {
    'script' : 'SCRIPT',        # script
    'var' : 'VAR',              # var
    'func' : 'FUNC',            # func
    'DO' : 'DO',                # DO main function
    'if' : 'IF',                # if
    'True' : 'IF_TRUE',         # True{ part of if condition
    'False' : 'IF_FALSE',       # False{ part of if condition
    'while' : 'WHILE',          # while
    'for' : 'FOR',              # for
    'returns' : 'RETURNS',      # returns statement
    'get' : 'READ',             # read from terminal
    'put' : 'WRITE',            # write on terminal
    'copy' : 'READ_FILE',       # read from file, to be used to add data to a dataframe
    'int' : 'INT',              # int
    'float' : 'FLOAT',          # float
    'char' : 'CHAR',            # char
    'void' : 'VOID',            # void
    'mean' : 'MEAN',            # mean special function
    'mode' : 'MODE',            # mode special function
    'median' : 'MEDIAN',        # median special function
    'variance' : 'VARIANCE',    # variance special function
    'max' : 'MAX',              # max special function
    'min' : 'MIN',              # min special function
    'stadDes' : 'STADDES',      # stadDes special function standard deviation
    'boxplot' : 'BOXPLOT',      # boxPlot special function
    'linReg' : 'LINREG',        # linReg special function simple linear regression
    'dataframe' : 'DATAFRAME'   # dataframe donde cargar datos
}

tokens = [
    'ID',                   # id
    'LETRERO',              # "letreros"
    'CTEI',                 # constant int
    'CTEF',                 # constant float
    'CTEC',                 # constant char
    'ARROW',                # ->
    'EQUALS',               # ==
    'GREATER_THAN',         # >
    'LESS_THAN',            # <
    'NOTEQUALS',            # !=
    'PLUS',                 # +
    'MINUS',                # -
    'MULT',                 # *
    'DIV',                  # /
    'AND',                  # &&
    'OR',                   # ||
    'ASIGN',                # =
    'LEFT_CUR_BRACKET',     # {
    'RIGHT_CUR_BRACKET',    # }
    'LEFT_SQR_BRACKET',     # [
    'RIGHT_SQR_BRACKET',    # ]
    'LEFT_PARENT',          # (
    'RIGHT_PARENT',         # )
    'SEMICOLON',            # ;
    'COMMA',                # ,
    'COMMENT',              # comments initiated by two consecutive exclamation marks - !!MyComent
] + list(reserved.values())

t_ASIGN= r'\='
t_NOTEQUALS= r'!='
t_ARROW= r'->'
t_EQUALS= r'\=\='
t_GREATER_THAN= r'\>'
t_LESS_THAN= r'\<'
t_PLUS= r'\+'
t_MINUS= r'\-'
t_MULT= r'\*'
t_DIV= r'\/'
t_AND= r'\&\&'
t_OR= r'\|\|'
t_LEFT_CUR_BRACKET= r'\{'
t_RIGHT_CUR_BRACKET= r'\}'
t_LEFT_SQR_BRACKET= r'\['
t_RIGHT_SQR_BRACKET= r'\]'
t_LEFT_PARENT= r'\('
t_RIGHT_PARENT= r'\)'
t_SEMICOLON= r'\;'
t_COMMA= r'\,'

def t_CTEF(t):
  r'\d+[.]\d+'
  t.value = float(t.value)
  return t

def t_CTEI(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_LETRERO(t):
  r'\"[a-zA-Z0-9!@#$%^&_\s\.]*\"'
  t.type = 'LETRERO'
  return t

def t_ID(t):
  r'[a-zA-Z_]*[a-zA-Z_0-9]+'
  t.type = reserved.get(t.value,'ID')
  return t

def t_COMMENT(t):
    r'\!\!.*'
    pass

def t_CTEC(t):
  r'\'.?\''
  t.value = t.value[:-1]
  t.value = t.value[1:]
  t.value = ord(t.value)
  return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

#lexer = lex.lex(debug=True)
lexer = lex.lex()

def test_lexer(fileName):
    file = open(fileName)
    accum = ""

    while True:
        line = file.readline()
        if (line):
            accum += line
        else: 
            break

    lexer.input(accum)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


# test_lexer("testP.txt")

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
)

# PARSER
def p_programa(p):
    '''
    programa : SCRIPT pnCrearDirFunc ID pnScriptFuncDir pnCuadGotoMain SEMICOLON varp funcp bloque pnCuadEND
    varp : var varp 
         | empty
    funcp : func funcp 
          | empty
    '''
    p[0] = None

def p_bloque(p):
    '''
    bloque : DO pnDirMain LEFT_CUR_BRACKET varp funcp estatutop RIGHT_CUR_BRACKET pnEndScript
    estatutop : estatuto estatutop 
              | empty
    '''
    p[0] = None

def p_tipo_simp(p):
    '''
    tipo_simp : INT pnSaveTypeVar
              | FLOAT pnSaveTypeVar
              | CHAR pnSaveTypeVar
    '''
    p[0] = None

def p_copy(p):
    '''
    copy : READ_FILE LEFT_PARENT variable COMMA LETRERO pnCuadCopy RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_variable(p):
    '''
    variable : ID pnSaveOperandos indexp
    indexp : LEFT_SQR_BRACKET pnArrIni exp pnArrVerify indexpp RIGHT_SQR_BRACKET pnArrFFPop
           | empty
    indexpp : COMMA pnArrAccIncDim exp pnMatCalc
            | empty pnArrCalc
    '''
    p[0] = None

def p_llamada(p):
    '''
    llamada : ID pnCheckFunc LEFT_PARENT pnGenerateEra expp RIGHT_PARENT pnCheckNoParam SEMICOLON pnCuadGoSub pnHandleReturnValue
    expp : exp pnCuadParametro exppp
         | empty
    exppp : COMMA pnUpdateK exp pnCuadParametro exppp
          | empty
    '''
    p[0] = None

def p_var(p):
    '''
    var : VAR pnCheckTablaVar v ARROW idp SEMICOLON
    v : DATAFRAME pnSaveTypeVar
      | tipo_simp vp
    vp : LEFT_SQR_BRACKET pnArrCreateNode CTEI pnArrSaveLim vpp RIGHT_SQR_BRACKET pnArrCuadriplificar
       | empty
    vpp : COMMA CTEI pnArrSaveLim
        | empty
    idp : ID pnCheckNameTablaVar pnArrAddDim idpp
    idpp : COMMA ID pnCheckNameTablaVar pnArrAddDim idpp
         | empty
    '''
    p[0] = None

def p_func(p):
    '''
    func : FUNC returnval ARROW ID pnAddFuncinDir LEFT_PARENT pnCheckTablaVar pnCrearListaParam param RIGHT_PARENT LEFT_CUR_BRACKET varp pnDirecIniFunc estatutop RIGHT_CUR_BRACKET pnCountVarsINTOResources pnCloseCurrentFunction
    returnval : tipo_simp
              | VOID pnSaveTypeVar
    '''
    p[0] = None

def p_param(p):
    '''
    param : paramlist
          | empty
    paramlist : tipoparam ARROW ID pnAddParametersTablaVar paramlistp
    tipoparam : tipo_simp
              | DATAFRAME pnSaveTypeVar
    paramlistp : COMMA paramlist
               | empty
    '''
    p[0] = None

def p_estatuto(p):
    '''
    estatuto : asign
             | llamada
             | lee
             | escribe
             | condicion
             | ciclow
             | ciclof
             | funcesp
             | return
             | copy
    '''
    p[0] = None

def p_asign(p):
    '''
    asign : variable ASIGN pnSaveOperadorAsign exp pnCuadAsign SEMICOLON
    '''
    p[0] = None

def p_lee(p):
    '''
    lee : READ LEFT_PARENT variable pnCuadLee RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_escribe(p):
    '''
    escribe :  WRITE LEFT_PARENT escribep RIGHT_PARENT SEMICOLON
    escribep : exp pnCuadEscribe
             | LETRERO pnCuadEscribe
    '''
    p[0] = None

def p_return(p):
    '''
    return : RETURNS exp pnCuadRet SEMICOLON
    '''
    p[0] = None

def p_exp(p):
    '''
    exp : exprel pnCuadOplog logic
    logic : logicsig exprel pnCuadOplog logic 
          | empty
    logicsig : AND pnSaveOperadorLog
             | OR pnSaveOperadorLog
    '''
    p[0] = None

def p_exprel(p):
    '''
    exprel : e pnCuadOpRelacional relacionalp
    relacionalp : relsig e pnCuadOpRelacional relacionalp 
                | empty
    relsig : LESS_THAN pnSaveOperadorRel
           | GREATER_THAN pnSaveOperadorRel
           | EQUALS pnSaveOperadorRel
           | NOTEQUALS pnSaveOperadorRel
    '''
    p[0] = None

def p_e(p):
    '''
    e : t pnCuadPlMi tp
    tp : tsig t pnCuadPlMi tp 
       | empty
    tsig : PLUS pnSaveOperadorPlMi
         | MINUS pnSaveOperadorPlMi
    '''
    p[0] = None

def p_t(p):
    '''
    t : f pnCuadMuDi fp
    fp : fsig f pnCuadMuDi fp 
       | empty
    fsig : MULT pnSaveOperadorMuDi
         | DIV pnSaveOperadorMuDi
    '''
    p[0] = None

def p_f(p):
    '''
    f : LEFT_PARENT pnSaveFondoFalso exp RIGHT_PARENT pnPopFondoFalso
      | CTEI pnSaveCteI  pnSaveOperandoConstante
      | CTEF pnSaveCteF pnSaveOperandoConstante
      | CTEC pnSaveCteC pnSaveOperandoConstante
      | variable
      | llamada
      | funcesp
    '''
    p[0] = None

def p_condicion(p):
    '''
    condicion : IF LEFT_PARENT exp pnCheckBoolIf RIGHT_PARENT IF_TRUE LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET falsop pnEndIf
    falsop : IF_FALSE pnElseIf LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET 
           | empty
    '''
    p[0] = None

def p_ciclow(p):
    '''
    ciclow : WHILE pnSaveWhile LEFT_PARENT exp pnCheckBoolIf RIGHT_PARENT LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET pnEndWhile
    '''
    p[0] = None

def p_ciclof(p):
    '''
    ciclof : FOR LEFT_PARENT variable pnSaveForID ASIGN exp pnCreateVControl COMMA exp pnCompControlFinal RIGHT_PARENT LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET pnEndFor
    '''
    p[0] = None

def p_funcesp(p):
    '''
    funcesp : mean
            | mode
            | median
            | variance
            | max
            | min
            | staddes
            | boxplot
            | linreg
            | copy
    '''
    p[0] = None

def p_mean(p):
    '''
    mean : MEAN LEFT_PARENT variable COMMA exp pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_mode(p):
    '''
    mode : MODE LEFT_PARENT variable  pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_median(p):
    '''
    median : MEDIAN LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_variance(p):
    '''
    variance : VARIANCE LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_max(p):
    '''
    max : MAX LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_min(p):
    '''
    min : MIN LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_staddes(p):
    '''
    staddes : STADDES LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_boxplot(p):
    '''
    boxplot : BOXPLOT LEFT_PARENT variable COMMA LETRERO pnCuadBoxplot RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_linreg(p):
    '''
    linreg : LINREG LEFT_PARENT variable COMMA exp COMMA exp pnCuadLinReg RIGHT_PARENT SEMICOLON
    '''
    p[0] = None


# Puntos neuralgicos

# Crear Directorio de Funciones al principio del Script
def p_pnCrearDirFunc(p):
    '''
    pnCrearDirFunc : empty
    '''
    p[0] = None
    global dirFunc 
    dirFunc = DirectorioFunciones()
    # print("Se crea directorio de funciones")

#Genera el cuádruplo de Goto Main
def p_pnCuadGotoMain(p):
    '''
    pnCuadGotoMain : empty
    '''
    nuevoCuadruplo = ["Goto","","",currentScript]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
    p[0] = None

# Registra la direccion Inicial de main en directorio de funciones
def p_pnDirMain(p):
    '''
    pnDirMain : empty
    '''
    dirFunc.registrosFunciones[currentScript][1] = cuadruplos.getCont()
    p[0] = None

# Guardar registro de la funcion Script en DirFunc
def p_pnScriptFuncDir(p):
    '''
    pnScriptFuncDir : empty
    '''
    global currentScript 
    currentScript = p[-1]
    dirFunc.insertNewScript(currentScript)
    p[0] = None

def p_pnCheckTablaVar(p):
    '''
    pnCheckTablaVar : empty
    '''
    # Función checa si ya existe una tabla de variables para esta función
    dirFunc.createTablaVar(currentScript,currentFunction)
    p[0] = None

def p_pnCrearListaParam(p):
    '''
    pnCrearListaParam : empty
    '''
    dirFunc.createListaParam(currentScript,currentFunction)
    p[0] = None

def p_pnSaveTypeVar(p):
    '''
    pnSaveTypeVar : empty
    '''
    global currentTypeVar 
    currentTypeVar = p[-1]
    # print("Se cambió currentTypeVar a: {}".format(currentTypeVar))
    p[0] = None

# Función que inserta una variable en la tabla de variables. Le asigna una dirección virtual
def p_pnCheckNameTablaVar(p):
    '''
    pnCheckNameTablaVar : empty
    '''
    dirFunc.insertVariable(p[-1],currentTypeVar,currentScript,currentFunction)

    global currentDecID
    currentDecID = p[-1]

    tipoActual = semantica.convertion[currentTypeVar]

    #Asignar direccion virtual
    # Hice esto porque no podía llevar memoria a directiorio de funciones como parametro por referencia
    if currentFunction == "":
        # es global
        if tipoActual == 2:
            dirFunc.registrosFunciones[currentScript][3][p[-1]][1] = memoria.countGlInt
            memoria.countGlInt += arrSize
        elif tipoActual == 3:
            dirFunc.registrosFunciones[currentScript][3][p[-1]][1] = memoria.countGlFloat
            memoria.countGlFloat += arrSize
        elif tipoActual == 4:
            dirFunc.registrosFunciones[currentScript][3][p[-1]][1] = memoria.countGlC
            memoria.countGlC += arrSize
        elif tipoActual == 'dataframe':
            dirFunc.registrosFunciones[currentScript][3][p[-1]][1] = memoria.countGlDf
            memoria.countGlDf += 1
        else:
            print("Error al asignar posible memoria virtual")
    else:
        # Es local
        if tipoActual == 2:
            dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocInt
            memoria.countLocInt += arrSize
        elif tipoActual == 3:
            dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocFloat
            memoria.countLocFloat += arrSize
        elif tipoActual == 4:
            dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocC
            memoria.countLocC += arrSize
        elif tipoActual == 'dataframe':
            dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocDf
            memoria.countLocDf += 1
        else:
            print("Error al asignar posible memoria virtual")

    p[0] = None

# Función 
def p_pnAddFuncinDir(p):
    '''
    pnAddFuncinDir : empty
    '''
    global currentFunction
    currentFunction = p[-1]
    
    dirFunc.insertNewFunction(p[-1],currentTypeVar)

    # Crea variable global con nombre de funcion que regresa una variable - handle returns
    if currentTypeVar != 'void':

        tipoSemantica = semantica.convertion[currentTypeVar]
        dirFunc.insertVariable(currentFunction,tipoSemantica,currentScript,'')

        # Asignar dirección virtual
        if tipoSemantica == 2:
            dirFunc.registrosFunciones[currentScript][3][currentFunction][1] = memoria.countGlInt
            memoria.countGlInt += 1
        elif tipoSemantica == 3:
            dirFunc.registrosFunciones[currentScript][3][currentFunction][1] = memoria.countGlFloat
            memoria.countGlFloat += 1
        elif tipoSemantica == 4:
            dirFunc.registrosFunciones[currentScript][3][currentFunction][1] = memoria.countGlC
            memoria.countGlC += 1
        else:
            print("Error al asignar posible memoria virtual a variable que representa funcion que regresa un valor")
            sys.exit()

    p[0] = None

# Inserta parametros en la tabla de variables de la función
def p_pnAddParametersTablaVar(p):
    '''
    pnAddParametersTablaVar : empty
    '''
    # Checar que el parametro no exista en tabla de variables e insertar
    dirFunc.insertVariable(p[-1],currentTypeVar,currentScript,currentFunction)
    dirFunc.insertarParam(currentScript,currentFunction,currentTypeVar)

    tipoActual = semantica.convertion[currentTypeVar]

    # Es variable local
    if tipoActual == 2:
        dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocInt
        memoria.countLocInt += 1
    elif tipoActual == 3:
        dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocFloat
        memoria.countLocFloat += 1
    elif tipoActual == 4:
        dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocC
        memoria.countLocC += 1
    elif tipoActual == 'dataframe':
        dirFunc.registrosFunciones[currentFunction][3][p[-1]][1] = memoria.countLocDf
        memoria.countLocDf += 1
    else:
        print("Error al asignar posible memoria virtual")


    p[0] = None

# Cuenta el número de recursos de la funcion. Variables locales + parámetros en la tabla de variables
def p_pnCountVarsINTOResources(p):
    '''
    pnCountVarsINTOResources : empty
    '''

    dirFunc.registrosFunciones[currentFunction][2]['vI'] = memoria.countLocInt - memoria.localInt

    dirFunc.registrosFunciones[currentFunction][2]['vF'] = memoria.countLocFloat - memoria.localFloat

    dirFunc.registrosFunciones[currentFunction][2]['vC'] = memoria.countLocC - memoria.localC

    dirFunc.registrosFunciones[currentFunction][2]['vDf'] = memoria.countLocDf - memoria.localDf

    dirFunc.registrosFunciones[currentFunction][2]['tI'] = memoria.countTemInt - memoria.tempInt

    dirFunc.registrosFunciones[currentFunction][2]['tF'] = memoria.countTemFloat - memoria.tempFloat

    dirFunc.registrosFunciones[currentFunction][2]['tC'] = memoria.countTemC - memoria.tempC

    dirFunc.registrosFunciones[currentFunction][2]['tPointer'] = memoria.countTemPointer - memoria.tempPointer

    dirFunc.registrosFunciones[currentFunction][2]['tB'] = memoria.countTemBool - memoria.tempBool

    #Los contadores de las variables se regresan al límite inferior original
    memoria.reset()

    p[0] = None

# Agrega direccion inicial de funcion en directorio de funciones 
def p_pnDirecIniFunc(p):
    '''
    pnDirecIniFunc : empty
    '''
    dirFunc.registrosFunciones[currentFunction][1] = cuadruplos.getCont()
    p[0] = None

def p_pnCloseCurrentFunction(p):
    '''
    pnCloseCurrentFunction : empty
    '''
    global currentFunction
    # Checar que sí regrese algo si es diferente de void
    tipoFunction = dirFunc.registrosFunciones[currentFunction][0]
    if tipoFunction != 'void' and cuadruplos.listaCuadruplos[-1][0] != 'Ret':
        print("Se debe regresar un valor de tipo {} en la función {}".format(tipoFunction,currentFunction))
        sys.exit()

    # Borrar tabla de variables de la funcion

    # dirFunc.registrosFunciones[currentFunction][3] = {}

    currentFunction = ""


    nuevoCuadruplo = ['ENDFUNC','','','']
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

def p_pnEndScript(p):
    '''
    pnEndScript : empty
    '''
    # printDir()
    # dirFunc.endScript(currentScript)

    # Contabilizar recursos que consumió main
    dirFunc.registrosFunciones[currentScript][2]['vI'] = memoria.countGlInt - memoria.globalInt
    dirFunc.registrosFunciones[currentScript][2]['vF'] = memoria.countGlFloat - memoria.globalFloat
    dirFunc.registrosFunciones[currentScript][2]['vC'] = memoria.countGlC - memoria.globalC
    dirFunc.registrosFunciones[currentScript][2]['vDf'] = memoria.countGlDf - memoria.globalDf
    dirFunc.registrosFunciones[currentScript][2]['tI'] = memoria.countGlTempInt - memoria.globalTempInt
    dirFunc.registrosFunciones[currentScript][2]['tF'] = memoria.countGlTempFloat - memoria.globalTempFloat
    dirFunc.registrosFunciones[currentScript][2]['tC'] = memoria.countGlTempC - memoria.globalTempC
    dirFunc.registrosFunciones[currentScript][2]['tPointer'] = memoria.countGlTempPointer - memoria.globalTempPointer
    dirFunc.registrosFunciones[currentScript][2]['tB'] = memoria.countGlTempBool - memoria.globalTempBool

    p[0] = None

# Checar en la llamada a la función que la función esté en el directorio de funciones
def p_pnCheckFunc(p):
    '''
    pnCheckFunc : empty
    '''
    if p[-1] not in dirFunc.registrosFunciones:
        print("La función {} no está definida".format(p[-1]))
        sys.exit()
    else:
        global currentLlamada 
        currentLlamada = p[-1]

    p[0] = None

# Generar cuadruplo era e inicializar K para checar argumentos/parametros
def p_pnGenerateEra(p):
    '''
    pnGenerateEra : empty
    '''
    # Generate cuadruplo ERA
    nuevoCuadruplo = ['ERA','','',currentLlamada]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    #Counter para parámetros
    dirFunc.registrosFunciones[currentLlamada][4][0] = 1 

    # Agregar fondo falso
    pilaOperadores.put(" FF ")

    p[0] = None

def getDirVirtual(argument):
    if type(argument) is not int:
            if currentFunction != "":
                try:
                    argument = dirFunc.registrosFunciones[currentFunction][3][argument][1]
                    return argument
                except:
                    argument = dirFunc.registrosFunciones[currentScript][3][argument][1]
                    return argument
            else:
                argument = dirFunc.registrosFunciones[currentScript][3][argument][1]
                return argument
    else:
        return argument

# Genera cuadruplo de parametro y checa tipo
def p_pnCuadParametro(p):
    '''
    pnCuadParametro : empty
    '''
    argument = pilaOperandos.get()
    argumentTipo = pilaTipo.get()

    listaParametrica = dirFunc.registrosFunciones[currentLlamada][4]
    index = listaParametrica[0]

    try:
        parametroActual = listaParametrica[index]
    except:
        print("Se declaró un parámetro de más en la llamada a la funcion {}".format(currentLlamada))
        sys.exit()

    if semantica.convertion[argumentTipo] == semantica.convertion[parametroActual]:
        argument = getDirVirtual(argument)

        # Generate cuadruplo Parameter
        nuevoCuadruplo = ['Parameter',argument,'',index]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
    else:
        print("Lista Parametrica no hace match con llamada")
        sys.exit()

    p[0] = None

# Actualiza K por nuevo parámetro
def p_pnUpdateK(p):
    '''
    pnUpdateK : empty
    '''
    dirFunc.registrosFunciones[currentLlamada][4][0] += 1

    p[0] = None

# Chequea K con lista paramétrica
def p_pnCheckNoParam(p):
    '''
    pnCheckNoParam : empty
    '''
    listaParametrica = dirFunc.registrosFunciones[currentLlamada][4]
    index = listaParametrica[0]

    if index != len(listaParametrica)-1:
        print("Error en número de parametros en la llamada de la funcion {} {}".format(currentLlamada, index))
        sys.exit()

    # Popear Fondo falso
    pilaOperadores.get()

    p[0] = None

# Genera cuadruplo de GoSub
def p_pnCuadGoSub(p):
    '''
    pnCuadGoSub : empty
    '''

    iniAddress = dirFunc.registrosFunciones[currentLlamada][1]
    nuevoCuadruplo = ["GOSUB",currentLlamada,'',iniAddress]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

# Parche Guadalupano
def p_pnHandleReturnValue(p):
    '''
    pnHandleReturnValue : empty
    '''
    global currentLlamada

    resultType = dirFunc.getTipoReturnFunction(currentLlamada)

    if resultType != 'void':
        tipoSemantica = semantica.convertion[resultType]

        isLocalTemp = False
        if currentFunction != "":
            isLocalTemp = True
        
        temporalActual = memoria.getMemoriaTemporal(tipoSemantica,isLocalTemp)
        direccionVarFuncion = dirFunc.getVirtualAddress(currentScript,currentLlamada)

        nuevoCuadruplo = ['=',direccionVarFuncion,'',temporalActual]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        pilaOperandos.put(temporalActual)
        pilaTipo.put(tipoSemantica)

    currentLlamada = ""

    p[0] = None

# Genera cuadruplo de Ret
def p_pnCuadRet(p):
    '''
    pnCuadRet : empty
    '''
    # Checar que no se regrese en main
    if currentFunction == "":
        print("ERROR: No se puede realizar return en DO")
        sys.exit()

    retorno = pilaOperandos.get()
    retornoTipo = pilaTipo.get()

    tipoFunction = dirFunc.getTipoReturnFunction(currentFunction)
    if tipoFunction == 'void':
        print("ERROR: No se puede incluir un returns en una funcion de tipo void".format(tipoFunction))
        sys.exit()

    # Checar que esté regresando el tipo de expresión de la funcion
    if semantica.convertion[retornoTipo] != semantica.convertion[tipoFunction]:
        print("ERROR: No se puede regresar un valor de tipo {} en una función que regresa {}".format(retornoTipo,tipoFunction))
        sys.exit()

    # Agregar dirección virtual de la variable con el nombre de la funcion que regresa
    direcCurFunc = dirFunc.registrosFunciones[currentScript][3][currentFunction][1]

    retorno = getDirVirtual(retorno)

    nuevoCuadruplo = ['Ret',direcCurFunc,'',retorno]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

# Da de alta constante entera en tabla de constantes si no está previamente
def p_pnSaveCteI(p):
    '''
    pnSaveCteI : empty
    '''
    if p[-1] not in tablaConst:
        direccion = memoria.countCteInt
        tablaConst[p[-1]] = ['2',direccion]
        memoria.countCteInt += 1

    p[0] = None

# Da de alta constante float en tabla de constantes si no está previamente
def p_pnSaveCteF(p):
    '''
    pnSaveCteF : empty
    '''
    if p[-1] not in tablaConst:
        direccion = memoria.countCteFloat
        tablaConst[p[-1]] = ['3',direccion]
        memoria.countCteFloat += 1
    p[0] = None

# Da de alta constante char en tabla de constantes si no está previamente
def p_pnSaveCteC(p):
    '''
    pnSaveCteC : empty
    '''
    if p[-1] not in tablaConst:
        direccion = memoria.countCteC
        tablaConst[p[-1]] = ['4',direccion]
        memoria.countCteC += 1
    p[0] = None

# Insertar fondo falso en pilaOperadores
def p_pnSaveFondoFalso(p):
    '''
    pnSaveFondoFalso : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

# Remover fondo falso de pilaOperadores
def p_pnPopFondoFalso(p):
    '''
    pnPopFondoFalso : empty
    '''
    if p[-1] == ')':
        pilaOperadores.get()
    p[0] = None

# Cuadruplos

def p_pnSaveOperandos(p):
    '''
    pnSaveOperandos : empty
    '''
    # checar que sea una variable declarada
    if currentFunction != "" and p[-1] not in dirFunc.registrosFunciones[currentFunction][3] and p[-1] not in dirFunc.registrosFunciones[currentScript][3]:
        print("VARIABLE NO DECLARADA {}".format(p[-1]))
        sys.exit()
    elif currentFunction == "" and p[-1] not in dirFunc.registrosFunciones[currentScript][3]:
        print("VARIABLE NO DECLARADA {}".format(p[-1]))
        sys.exit()

    # Insertar variable a pilaOperandos y pilaSaltos
    pilaOperandos.put(p[-1])

    # dirFunc.registrosFunciones[funcionActual][tablaVariables][nombreVariable][tipo]
    try:
        #LOCAL
        pilaTipo.put(dirFunc.registrosFunciones[currentFunction][3][p[-1]][0])
    except:
        #GLOBAL
        pilaTipo.put(dirFunc.registrosFunciones[currentScript][3][p[-1]][0])

    p[0] = None

# Insertar en pilaOperandos la constante y su tipo en pilaTipo 
def p_pnSaveOperandoConstante(p):
    '''
    pnSaveOperandoConstante : empty
    '''
    pilaOperandos.put(tablaConst[p[-2]][1])
    pilaTipo.put(tablaConst[p[-2]][0])
    p[0] = None

def p_pnSaveOperadorPlMi(p):
    '''
    pnSaveOperadorPlMi : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

def p_pnSaveOperadorMuDi(p):
    '''
    pnSaveOperadorMuDi : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

def p_pnSaveOperadorRel(p):
    '''
    pnSaveOperadorRel : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

def p_pnSaveOperadorLog(p):
    '''
    pnSaveOperadorLog : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

def p_pnCuadPlMi(p):
    '''
    pnCuadPlMi : empty
    '''
    if pilaOperadores.qsize() > 0:
        top = pilaOperadores.get()
        pilaOperadores.put(top)

        if top == '+' or top == '-':
            rightOperand = pilaOperandos.get()
            rightType = pilaTipo.get()
            leftOperand = pilaOperandos.get()
            leftType = pilaTipo.get()
            operador = pilaOperadores.get()

            resultType = semantica.tablaSimbolos[semantica.convertion[rightType]][semantica.convertion[leftType]][operador]

            if resultType != 0:
                
                isLocalTemp = False
                if currentFunction != "":
                    isLocalTemp = True

                temporalActual = memoria.getMemoriaTemporal(resultType,isLocalTemp)
                leftOperand = getDirVirtual(leftOperand)
                rightOperand = getDirVirtual(rightOperand)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

    p[0] = None

def p_pnCuadMuDi(p):
    '''
    pnCuadMuDi : empty
    '''
    if pilaOperadores.qsize() > 0:
        top = pilaOperadores.get()
        pilaOperadores.put(top)

        if top == '*' or top == '/':
            rightOperand = pilaOperandos.get()
            rightType = pilaTipo.get()
            leftOperand = pilaOperandos.get()
            leftType = pilaTipo.get()
            operador = pilaOperadores.get()

            resultType = semantica.tablaSimbolos[semantica.convertion[rightType]][semantica.convertion[leftType]][operador]

            if resultType != 0:

                isLocalTemp = False
                if currentFunction != "":
                    isLocalTemp = True

                temporalActual = memoria.getMemoriaTemporal(resultType,isLocalTemp)
                leftOperand = getDirVirtual(leftOperand)
                rightOperand = getDirVirtual(rightOperand)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

    p[0] = None

# Genera cuadruplo de operadores relacionales
def p_pnCuadOpRelacional(p):
    '''
    pnCuadOpRelacional : empty
    '''
    if pilaOperadores.qsize() > 0:
        top = pilaOperadores.get()
        pilaOperadores.put(top)

        operadoresRelacionales = ['>', '<','==','!=']

        if top in operadoresRelacionales:
            rightOperand = pilaOperandos.get()
            rightType = pilaTipo.get()
            leftOperand = pilaOperandos.get()
            leftType = pilaTipo.get()

            operador = pilaOperadores.get()

            resultType = semantica.tablaSimbolos[semantica.convertion[rightType]][semantica.convertion[leftType]][operador]

            if resultType != 0:

                isLocalTemp = False
                if currentFunction != "":
                    isLocalTemp = True

                temporalActual = memoria.getMemoriaTemporal(resultType,isLocalTemp)
                leftOperand = getDirVirtual(leftOperand)
                rightOperand = getDirVirtual(rightOperand)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

# Genera cuadruplo de operadores lógicos
def p_pnCuadOplog(p):
    '''
    pnCuadOplog : empty
    '''
    if pilaOperadores.qsize() > 0:
        top = pilaOperadores.get()
        pilaOperadores.put(top)

        if top == '&&' or top == '||':
            rightOperand = pilaOperandos.get()
            rightType = pilaTipo.get()
            leftOperand = pilaOperandos.get()
            leftType = pilaTipo.get()

            operador = pilaOperadores.get()

            resultType = semantica.tablaSimbolos[semantica.convertion[rightType]][semantica.convertion[leftType]][operador]

            if resultType != 0:

                isLocalTemp = False
                if currentFunction != "":
                    isLocalTemp = True

                temporalActual = memoria.getMemoriaTemporal(resultType,isLocalTemp)
                leftOperand = getDirVirtual(leftOperand)
                rightOperand = getDirVirtual(rightOperand)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

# Guarda operador de asign en pilaOperadores
def p_pnSaveOperadorAsign(p):
    '''
    pnSaveOperadorAsign : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

# Genera cuadruplo de Asign
def p_pnCuadAsign(p):
    '''
    pnCuadAsign : empty
    '''
    if pilaOperadores.qsize() > 0:
        top = pilaOperadores.get()
        pilaOperadores.put(top)

        if top == '=':
            valor = pilaOperandos.get()
            valorTipo = pilaTipo.get()
            aAsignar = pilaOperandos.get()
            aAsignarTipo = pilaTipo.get()

            operador = pilaOperadores.get()
            
            if semantica.convertion[valorTipo] == semantica.convertion[aAsignarTipo]:
                valor = getDirVirtual(valor)
                aAsignar = getDirVirtual(aAsignar)

                nuevoCuadruplo = [operador,valor,"",aAsignar]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
            else:
                print("Se deben asignar valores del mismo tipo")
                print("{} es {} \n {} es {}".format(valor,valorTipo,aAsignar,aAsignarTipo))
                sys.exit()

    p[0] = None

# Genera cuadruplo de escribeC
def p_pnCuadEscribe(p):
    '''
    pnCuadEscribe : empty
    '''
    if p[-3] == 'put':
        if p[-1] is None:
            toPrint = pilaOperandos.get()
            pilaTipo.get()

            operador = 'put'

            toPrint = getDirVirtual(toPrint)
            
            nuevoCuadruplo = [operador,"", "",toPrint]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        else:
            try:
                firstCharacter = p[-1][0]
                lastCharacter = p[-1][-1]

                if firstCharacter == '"' and lastCharacter == '"':
                    #Se guarda letrero como una constante
                    if p[-1] not in tablaConst:
                        direccion = memoria.countCteLetrero
                        tablaConst[p[-1]] = ['LETRERO',direccion]
                        memoria.countCteLetrero += 1
                        toPrint = tablaConst[p[-1]][1]
                    else:
                        toPrint = tablaConst[p[-1]][1]

                    operador = 'put'
            
                    nuevoCuadruplo = [operador,"", "",toPrint]
                    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
            except:
                print("No se puede imprimir esto. Sólo se imprimen expresiones o letreros")
                sys.exit()

    p[0] = None

def p_pnCuadLee(p):
    '''
    pnCuadLee : empty
    '''
    if p[-3] == 'get':
        # Checar que lo que se está insertando es válido con respecto a tipos
        leerVariable = pilaOperandos.get()
        leerTipo = pilaTipo.get()
        
        operador = 'get'
        leerVariable = getDirVirtual(leerVariable)
        leerTipo = semantica.convertion[leerTipo]

        nuevoCuadruplo = [operador,"", leerTipo,leerVariable]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        print("Checar que lo que se lee es de un tipo de variable compatible")

    p[0] = None

def p_pnCuadCopy(p):
    '''
    pnCuadCopy : empty
    '''
    if p[-5] == 'copy':
        # Checar que sea un letrero y que termine en .csv
        if p[-1][0] == '"' and p[-1].endswith('.csv"'):
            df = pilaOperandos.get()
            tipo = pilaTipo.get()

            if semantica.convertion[tipo] != 'dataframe':
                print("ERROR: Type Mismatch. Función 'copy' sólo se puede utilizar con variables de tipo dataframe")
                sys.exit()

            toRead = p[-1]
            toRead = toRead[:-1]
            toRead = toRead[1:]

            operador = 'copy'
            df = getDirVirtual(df)

            nuevoCuadruplo = [operador,"", df,toRead]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        else:
            print("You can only read from .csv files")
            sys.exit()
    else:
        print("se leyó copy, pero no se generó el cuadruplo")
        sys.exit()

    p[0] = None

# Generación de cuadruplos para funciones especiales que regresan un número
def p_pnCuadFuncEsp(p):
    '''
    pnCuadFuncEsp : empty
    '''
    top = p[-5]
    
    funcEspReturn = ['mean','mode','median','variance','max','min','stadDes']

    if top in funcEspReturn:
        resultType = 3
        newIndex = pilaOperandos.get()
        tipoIndex = pilaTipo.get()

        toCalculate = pilaOperandos.get()
        tipoToCalculate = pilaTipo.get()

        if semantica.convertion[tipoToCalculate] != 'dataframe':
            print("ERROR: sólo se puede generar {} con una variable de tipo dataframe".format(top))
            sys.exit()

        if semantica.convertion[tipoIndex] != 2:
            print("ERROR: Type Mismatch. Se espera una expresión de tipo entera para indexar el dataframe")
            sys.exit()

        operador = top

        isLocalTemp = False
        if currentFunction != "":
            isLocalTemp = True

        temporalActual = memoria.getMemoriaTemporal(resultType,isLocalTemp)
        toCalculate = getDirVirtual(toCalculate)
        newIndex = getDirVirtual(newIndex)

        # mean,df,index,res
        nuevoCuadruplo = [operador,toCalculate,newIndex,temporalActual]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        pilaOperandos.put(temporalActual)
        pilaTipo.put(resultType)

    p[0] = None

# Generación de cuadruplos para boxplots
def p_pnCuadBoxplot(p):
    '''
    pnCuadBoxplot : empty
    '''
    top = p[-5]

    if top in 'boxplot':
        toCalculate = pilaOperandos.get()
        tipoToCalculate = pilaTipo.get()
        titulo = p[-1]
        titulo = insertTablaConst(titulo,'letrero')

        if semantica.convertion[tipoToCalculate] != 'dataframe':
            print("ERROR: sólo se puede generar {} con una variable de tipo dataframe".format(top))
            sys.exit()

        operador = top

        toCalculate = getDirVirtual(toCalculate)

        nuevoCuadruplo = [operador,"", titulo,toCalculate]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

# Generación de cuadruplos para regresiones lineales
def p_pnCuadLinReg(p):
    '''
    pnCuadLinReg : empty
    '''
    top = p[-7]

    if top == 'linReg':
        indexB = pilaOperandos.get()
        tipoIndexB = pilaTipo.get()

        indexA = pilaOperandos.get()
        tipoIndexA = pilaTipo.get()

        toCalculate = pilaOperandos.get()
        tipoToCalculate = pilaTipo.get()

        if semantica.convertion[tipoToCalculate] != 'dataframe':
            print("ERROR: sólo se puede generar {} con una variable de tipo dataframe".format(top))
            sys.exit()

        if semantica.convertion[tipoIndexA] != 2 or semantica.convertion[tipoIndexB] != 2:
            print("ERROR: Type Mismatch. Se espera una expresión de tipo entera para indexar el dataframe")
            sys.exit()

        operador = top

        toCalculate = getDirVirtual(toCalculate)
        indexA = getDirVirtual(indexA)
        indexB = getDirVirtual(indexB)

        nuevoCuadruplo = [operador,indexA,indexB,toCalculate]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None


# Cuadruplos No lineales

# Genera cuadruplo de GotoF
def p_pnCheckBoolIf(p):
    '''
    pnCheckBoolIf : empty
    '''
    expTipo = pilaTipo.get()

    if expTipo != 1:
        print("ERROR: Type Mismatch. Expected boolean condition in IF statement")
        sys.exit()
    else:
        result = pilaOperandos.get()

        result = getDirVirtual(result)

        nuevoCuadruplo = ['GotoF',result,"","_"]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        pilaSaltos.put(cuadruplos.getCont()-1)

    p[0] = None

# Genera cuadruplo de Goto
def p_pnElseIf(p):
    '''
    pnElseIf : empty
    '''
    nuevoCuadruplo = ['Goto',"","","_"]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
    false = pilaSaltos.get()
    pilaSaltos.put(cuadruplos.getCont()-1)
    cuadruplos.fill(false,cuadruplos.getCont())
    p[0] = None

# Actualiza pilaSaltos y rellena cuadruplo
def p_pnEndIf(p):
    '''
    pnEndIf : empty
    '''
    end = pilaSaltos.get()
    cuadruplos.fill(end,cuadruplos.getCont())
    p[0] = None

# WHILE

# Guardar contador cuadruplos en pilaSaltos
def p_pnSaveWhile(p):
    '''
    pnSaveWhile : empty
    '''
    pilaSaltos.put(cuadruplos.getCont())
    p[0] = None

# Genera cuadruplo de Goto. Actualiza pilaSaltos y rellena cuadruplo anterior
def p_pnEndWhile(p):
    '''
    pnEndWhile : empty
    '''
    end = pilaSaltos.get()
    retorno = pilaSaltos.get()
    nuevoCuadruplo = ['Goto',"","",retorno]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
    cuadruplos.fill(end,cuadruplos.getCont())
    p[0] = None


# FOR

# Chequea que la variable sea de tipo int. Guarda variable en pilaOperandos
def p_pnSaveForID(p):
    '''
    pnSaveForID : empty
    '''
    # checar que sea una variable que ya esté declarada en la funcion o en el scrpipt
    funcionActual = ""
    if currentFunction == "":
        funcionActual = currentScript
    else:
        funcionActual = currentFunction

    topPila = pilaOperandos.get()
    pilaTipo.get()

    if topPila in dirFunc.registrosFunciones[funcionActual][3]:
        # Ver el tipo de la variable
        if semantica.convertion[dirFunc.registrosFunciones[funcionActual][3][topPila][0]] != 2:
            print("ERROR: Type Mismatch. You can only use an id with int as type")
            sys.exit()
        else:
            pilaOperandos.put(topPila)
            pilaTipo.put(semantica.convertion[dirFunc.registrosFunciones[funcionActual][3][topPila][0]])
    else:
        print("ERROR: Se debe declarar la variable a usar en el for loop")
        sys.exit()
    p[0] = None

# Genera cuadruplo de variable de control de for loop
def p_pnCreateVControl(p):
    '''
    pnCreateVControl : empty
    '''
    expTipo = pilaTipo.get()

    if semantica.convertion[expTipo] != 2:
        print("ERROR: Type Mismatch")
        sys.exit()
    else:
        exp = pilaOperandos.get()

        VControl = pilaOperandos.get()
        pilaOperandos.put(VControl)

        VControl = getDirVirtual(VControl)
        
        pilaVControlLoop.put(VControl)

        controlTipo = pilaTipo.get()
        pilaTipo.put(controlTipo)

        tipoRes = semantica.tablaSimbolos[semantica.convertion[controlTipo]][semantica.convertion[expTipo]]['==']
        
        if tipoRes == 0:
            print("ERROR Type Mismatch. Variable en for no puede asignar el tipo resultante de la expresión")
        else:
            exp = getDirVirtual(exp)

            nuevoCuadruplo = ['=',exp,"",VControl]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

# Genera cuadruplos para chequear condición booleana del for loop
def p_pnCompControlFinal(p):
    '''
    pnCompControlFinal : empty
    '''
    expTipo = pilaTipo.get()
    if semantica.convertion[expTipo] != 2:
        print("ERROR: Type Mismatch en For loop, Expresión Final")
        sys.exit()
    else:
        exp = pilaOperandos.get()

        isLocalTemp = False
        if currentFunction != "":
            isLocalTemp = True

        VFinal = memoria.getMemoriaTemporal(2,isLocalTemp)

        exp = getDirVirtual(exp)

        nuevoCuadruplo = ['=',exp,"",VFinal]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        isLocalTemp = False
        if currentFunction != "":
            isLocalTemp = True
        # 1 porque es un temporal de tipo booleano
        temporalActual = memoria.getMemoriaTemporal(1,isLocalTemp)

        topVC = pilaVControlLoop.get()
        pilaVControlLoop.put(topVC)

        nuevoCuadruplo = ['<',topVC,VFinal,temporalActual]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        pilaSaltos.put(cuadruplos.getCont()-1)

        nuevoCuadruplo = ['GotoF',temporalActual,"","_"]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        pilaSaltos.put(cuadruplos.getCont()-1)
    p[0] = None

# Genera cuadruplos para actualizar variable de control, y el Goto para otro loop
def p_pnEndFor(p):
    '''
    pnEndFor : empty
    '''
    isLocalTemp = False
    if currentFunction != "":
        isLocalTemp = True

    temporalActual = memoria.getMemoriaTemporal(2,isLocalTemp)

    if 1 not in tablaConst:
        direccion = memoria.countCteInt
        tablaConst[1] = ['2',direccion]
        memoria.countCteInt += 1

    topVC = pilaVControlLoop.get()
    pilaVControlLoop.put(topVC)

    nuevoCuadruplo = ['+',topVC,tablaConst[1][1],temporalActual]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    nuevoCuadruplo = ['=',temporalActual,"",topVC]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    debeSerIdOriginal = pilaOperandos.get()
    pilaOperandos.put(debeSerIdOriginal)

    debeSerIdOriginal = getDirVirtual(debeSerIdOriginal)

    nuevoCuadruplo = ['=',temporalActual,"",debeSerIdOriginal]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    fin = pilaSaltos.get()
    ret = pilaSaltos.get()

    nuevoCuadruplo = ['Goto',"","",ret]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    cuadruplos.fill(fin,cuadruplos.getCont())

    elimina = pilaOperandos.get() #Sacamos el id original
    eliminaTipo = pilaTipo.get()

    pilaVControlLoop.get()

    p[0] = None


# Arreglos

# Inicializa los nodos para arreglos
def p_pnArrCreateNode(p):
    '''
    pnArrCreateNode : empty
    '''
    # Inicializar lista de nodos
    dirFunc.currDecArreglo[1] = []

    # R = 1
    dirFunc.currDecArreglo[0] = 1

    p[0] = None


# Guarda Limites Superiores de arreglos y calcula R acumulada
def p_pnArrSaveLim(p):
    '''
    pnArrSaveLim : empty
    '''
    # Guarda Límite superior
    if p[-1] <= 0:
        print("ERROR: Se debe incluir un tamaño mayor a 0 para la declaración de arreglos y matrices")
        sys.exit()

    dirFunc.currDecArreglo[1].append([p[-1],'m'])

    # R = R * (Lsup + 1)
    R = dirFunc.currDecArreglo[0]
    dirFunc.currDecArreglo[0] = R * (p[-1]+1)

    p[0] = None

# Llena la lista de nodos con cuadriplificacion de receta de cocina
def p_pnArrCuadriplificar(p):
    '''
    pnArrCuadriplificar : empty
    '''
    global arrSize
    arrSize = dirFunc.currDecArreglo[0] # R
    listaNodos = dirFunc.currDecArreglo[1]

    for nodo in listaNodos:
        m = dirFunc.currDecArreglo[0] / (nodo[0] + 1)
        nodo[1] = m
        dirFunc.currDecArreglo[0] = m

    dirFunc.currDecArreglo[1][-1:][0][1] = 0

    p[0] = None


# Añade dimensiones de arreglo tablaVar
def p_pnArrAddDim(p):
    '''
    pnArrAddDim : empty
    '''
    # Checar si variable es arreglo
    global arrSize

    if dirFunc.currDecArreglo[1] != "":

        # get funcion actual
        funcionActual = ""
        if currentFunction == "":
            funcionActual = currentScript
        else:
            funcionActual = currentFunction
        
        dirFunc.registrosFunciones[funcionActual][3][currentDecID].append(dirFunc.currDecArreglo[1])

        # borrar lista Nodos 
        dirFunc.currDecArreglo[1] = ""
        arrSize = 1

    p[0] = None


# verificar variable dim, Inicializar el acceso de arreglo/matriz, poner fondo falso, #2
def p_pnArrIni(p):
    '''
    pnArrIni : empty
    '''
    # Sacar nombre de arreglo de la listaOperandos
    ide = pilaOperandos.get()
    tipo = pilaTipo.get()

    # Verificar que ID tiene dimensiones
    if dirFunc.isDim(ide,currentScript,currentFunction):
        # Guardar nombre de arreglo

        pilaDim.put([ide,1])
        pilaOperadores.put(" FF ")
    else:
        print("variable no dimensionada")
        sys.exit()

    p[0] = None


# Generar cuadruplo verify index
def p_pnArrVerify(p):
    '''
    pnArrVerify : empty
    '''
    s1 = pilaOperandos.get()
    pilaOperandos.put(s1)

    # Agarrar dimension de arreglo/matriz actual
    topPilaDim = pilaDim.get()
    pilaDim.put(topPilaDim)

    limSup = dirFunc.getLimSup(currentScript,currentFunction,topPilaDim[0],1)

    s1 = getDirVirtual(s1)

    nuevoCuadruplo = ['Ver', s1, '', limSup]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
    
    p[0] = None

# Incrementar dimension de arreglos 
def p_pnArrAccIncDim(p):
    '''
    pnArrAccIncDim : empty
    '''
    # Siempre va a ser matriz d2 después de popear matriz d1
    nombreMatriz = pilaDim.get()[0]
    pilaDim.put([nombreMatriz,2])

    p[0] = None

def insertTablaConst(dirBase,tipo):
    # No está dentro de la tabla de variables
    if dirBase not in tablaConst:
        if tipo == '2':
            direccion = memoria.countCteInt
            tablaConst[dirBase] = [tipo,direccion]
            memoria.countCteInt += 1
            return direccion
        elif tipo == '3':
            direccion = memoria.countCteFloat
            tablaConst[dirBase] = [tipo,direccion]
            memoria.countCteFloat += 1
            return direccion
        elif tipo == '4':
            direccion = memoria.countCteC
            tablaConst[dirBase] = [tipo,direccion]
            memoria.countCteC += 1
            return direccion
        elif tipo == 'letrero':
            direccion = memoria.countCteLetrero
            tablaConst[dirBase] = [tipo,direccion]
            memoria.countCteLetrero += 1
            return direccion
    else:
    # Está dentro de la tabla de variables
        return tablaConst[dirBase][1]


# Realiza cáculos de arreglos (1 dimension) para temp Pointer
def p_pnArrCalc(p):
    '''
    pnArrCalc : empty
    '''

    # Debe ser expresion
    s1 = pilaOperandos.get()
    s1Tipo = pilaTipo.get()

    if semantica.convertion[s1Tipo] != 2:
        print("ERROR: Expresión de indexación en arreglos debe ser int")
        sys.exit() 

    top = pilaDim.get()[0]
    pilaDim.put(top)

    dirBaseArreglo = dirFunc.getDirBaseArreglo(currentScript,currentFunction,top)
    dirBaseArreglo = insertTablaConst(dirBaseArreglo,'2')

    isLocalTemp = False
    if currentFunction != "":
        isLocalTemp = True
    temporalPointerActual = memoria.getMemoriaTemporal('pointer',isLocalTemp)
    resultType = semantica.tablaSimbolos[semantica.convertion[s1Tipo]][semantica.convertion['int']]['+']
    
    s1 = getDirVirtual(s1)

    # + dirBase()
    nuevoCuadruplo = ['+',s1,dirBaseArreglo,temporalPointerActual]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    pilaOperandos.put(temporalPointerActual)
    pilaTipo.put(resultType)

    pilaDim.get()

    p[0] = None

# Realiza cáculos de matrices (2 dimensiones) para temp Pointer
def p_pnMatCalc(p):
    '''
    pnMatCalc : empty
    '''
    s2 = pilaOperandos.get()
    s2Tipo = pilaTipo.get()

    s1 = pilaOperandos.get()
    s1Tipo = pilaTipo.get()

    if len(pilaTipo.queue) != len(pilaOperandos.queue):
        print("algo mal sis")
        sys.exit()

    if semantica.convertion[s2Tipo] != 2 or semantica.convertion[s1Tipo] != 2:
        print("ERROR: Expresión de indexación en arreglos debe ser int")
        sys.exit()

    # s1*m1
    top = pilaDim.get()
    pilaDim.put(top)

    m1 = dirFunc.getM1(currentScript,currentFunction,top[0])
    isLocalTemp = False
    if currentFunction != "":
        isLocalTemp = True
    temporalActual1 = memoria.getMemoriaTemporal(2,isLocalTemp)

    s1 = getDirVirtual(s1)
    m1 = insertTablaConst(m1,'2')

    nuevoCuadruplo = ['*',s1,m1,temporalActual1]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    # Verificar
    matrizActual = pilaDim.get()
    pilaDim.put(matrizActual)

    limSup = dirFunc.getLimSup(currentScript,currentFunction,matrizActual[0],2)

    s2 = getDirVirtual(s2)

    nuevoCuadruplo = ['Ver', s2, '', limSup]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)


    # +s2
    isLocalTemp = False
    if currentFunction != "":
        isLocalTemp = True
    temporalActual2 = memoria.getMemoriaTemporal(2,isLocalTemp)

    nuevoCuadruplo = ['+',temporalActual1,s2,temporalActual2]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)


    # + dirBase()
    dirBaseMatriz = dirFunc.getDirBaseArreglo(currentScript,currentFunction,matrizActual[0])
    dirBaseMatriz = insertTablaConst(dirBaseMatriz,'2')

    isLocalTemp = False
    if currentFunction != "":
        isLocalTemp = True
    temporalPointerActual = memoria.getMemoriaTemporal('pointer',isLocalTemp)

    nuevoCuadruplo = ['+',temporalActual2,dirBaseMatriz,temporalPointerActual]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    pilaOperandos.put(temporalPointerActual)
    pilaTipo.put('int')

    pilaDim.get()

    p[0] = None

# Elimina el fondo falso
def p_pnArrFFPop(p):
    '''
    pnArrFFPop : empty
    '''
    pilaOperadores.get()
    p[0] = None

# Genera cuadruplo de final de programa
def p_pnCuadEND(p):
    '''
    pnCuadEND : empty
    '''

    nuevoCuadruplo = ['END','','','']
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
    
    p[0] = None

def p_empty(p):
    '''
    empty :'''
    pass

def p_error(p):
  if p:
    print("ERROR")
    print(f"{p.type}({p.value}) on line {p.lineno}")
  else:
      print("Syntax error at EOF")

#Function to print directorio de funciones
def printDir():
    print("\n\n\n\n")
    prettyDirFunc = json.dumps(dirFunc.registrosFunciones,indent=4)
    print(prettyDirFunc)

# Build the parser
parser = yacc.yacc(debug=True)

# filename = 'testPropuesta.txt'
filename = 'test.txt'
# filename = 'testArrays.txt'
# filename = 'testBubbleSort.txt'
# filename = 'testMultMatrices.txt'
# filename = 'testModulos.
# filename = 'testArreglos.txt'
# filename = 'testForLoop.txt'
# filename = 'testArreglo2.txt'
# filename = 'testModulosNonVoid.txt'
# filename = 'testFuncArreglos.txt'
fp = codecs.open(filename, "r", "utf-8")
text = fp.read()
fp.close()

with open(filename) as fp:
    try:
        yacc.parse(text)
    except EOFError:
        pass


printDir()

print("LISTA DE CUADRUPLOS \n")
index = 1
for cuad in cuadruplos.listaCuadruplos:
    temp = [index] + cuad
    cuad = temp
    print(cuad)
    index += 1

# print(*cuadruplos.listaCuadruplos, sep="\n")

# print("  \n\n TABLA CONSTANTES")
print(tablaConst)

data = {
    'cuads': cuadruplos.listaCuadruplos,
    'dirfunc' : dirFunc.registrosFunciones,
    'tablaconst' : tablaConst,
    'script' : currentScript,
    'direcciones' : memoria,
    #maybe incluir memoria aquí
}

def exportData():
    return data
