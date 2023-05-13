import ply.lex as lex
import ply.yacc as yacc
from cuboSemantico import CuboSemantico
from directorioFunciones import DirectorioFunciones
import codecs
import json
from queue import LifoQueue
from cuadruplos import Cuadruplo
import sys

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

cuadruplos = Cuadruplo()

pilaOperadores = LifoQueue(maxsize=0)
pilaOperandos = LifoQueue(maxsize=0)
pilaTipo = LifoQueue(maxsize=0)
identificadorTemporales = 0
pilaSaltos = LifoQueue(maxsize=0)

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
    programa : SCRIPT pnCrearDirFunc ID pnScriptFuncDir SEMICOLON varp funcp bloque
    varp : var varp 
         | empty
    funcp : func funcp 
          | empty
    '''
    p[0] = None

def p_bloque(p):
    '''
    bloque : DO LEFT_CUR_BRACKET varp funcp estatutop RIGHT_CUR_BRACKET pnEndScript
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

def p_tipo_comp(p):
    '''
    tipo_comp : DATAFRAME 
              | file
    '''
    p[0] = None

def p_copy(p):
    '''
    copy : READ_FILE LEFT_PARENT LETRERO pnCuadCopy RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_file(p):
    '''
    file : ID
    '''
    p[0] = None

def p_variable(p):
    '''
    variable : ID pnSaveOperandos indexp
    indexp : LEFT_SQR_BRACKET exp indexpp RIGHT_SQR_BRACKET 
           | empty
    indexpp : COMMA exp 
            | empty
    '''
    p[0] = None

def p_llamada(p):
    '''
    llamada : ID LEFT_PARENT expp RIGHT_PARENT SEMICOLON
    expp : exp exppp
         | empty
    exppp : COMMA exp exppp
          | empty
    '''
    p[0] = None

def p_var(p):
    '''
    var : VAR pnCheckTablaVar v ARROW idp SEMICOLON
    v : DATAFRAME pnSaveTypeVar
      | tipo_simp vp
    vp : LEFT_SQR_BRACKET CTEI vpp RIGHT_SQR_BRACKET 
       | empty
    vpp : COMMA CTEI 
        | empty
    idp : ID pnCheckNameTablaVar idpp
    idpp : COMMA ID pnCheckNameTablaVar idpp
         | empty
    '''
    p[0] = None

def p_func(p):
    '''
    func : FUNC returnval ARROW ID pnAddFuncinDir LEFT_PARENT pnCheckTablaVar param RIGHT_PARENT LEFT_CUR_BRACKET varp estatutop RIGHT_CUR_BRACKET pnCloseCurrentFunction
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
    return : RETURNS exp SEMICOLON
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
    ciclof : FOR LEFT_PARENT ID pnSaveForID ASIGN exp pnCreateVControl COMMA exp pnCompControlFinal RIGHT_PARENT LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET pnEndFor
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
    mean : MEAN LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
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
    boxplot : BOXPLOT LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_linreg(p):
    '''
    linreg : LINREG LEFT_PARENT variable pnCuadFuncEsp RIGHT_PARENT SEMICOLON
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

def p_pnSaveTypeVar(p):
    '''
    pnSaveTypeVar : empty
    '''
    global currentTypeVar 
    currentTypeVar = p[-1]
    # print("Se cambió currentTypeVar a: {}".format(currentTypeVar))
    p[0] = None

def p_pnCheckNameTablaVar(p):
    '''
    pnCheckNameTablaVar : empty
    '''
    dirFunc.insertVariable(p[-1],currentTypeVar,currentScript,currentFunction)
    p[0] = None

def p_pnAddFuncinDir(p):
    '''
    pnAddFuncinDir : empty
    '''
    global currentFunction
    currentFunction = p[-1]
    # print("Se cambió currentFunction a {}".format(currentFunction))

    # Si quires insertar functions como variables dentro de modulos, I think it would be here.
    # Check current function / script and so on, como en createTablaVar
    dirFunc.insertNewFunction(p[-1],currentTypeVar)

    p[0] = None

def p_pnAddParametersTablaVar(p):
    '''
    pnAddParametersTablaVar : empty
    '''
    # Checar que el parametro no exista en tabla de variables e insertar
    dirFunc.insertVariable(p[-1],currentTypeVar,currentScript,currentFunction)
    p[0] = None

def p_pnCloseCurrentFunction(p):
    '''
    pnCloseCurrentFunction : empty
    '''
    global currentFunction
    currentFunction = ""
    # Darle cuello a la función?
    p[0] = None

def p_pnEndScript(p):
    '''
    pnEndScript : empty
    '''
    # printDir()
    dirFunc.endScript(currentScript)
    p[0] = None

def p_pnSaveCteI(p):
    '''
    pnSaveCteI : empty
    '''
    tablaConst[p[-1]] = ['2',"direccionVirtual"]
    p[0] = None

def p_pnSaveCteF(p):
    '''
    pnSaveCteF : empty
    '''
    tablaConst[p[-1]] = ['3',"direccionVirtual"]
    p[0] = None

def p_pnSaveCteC(p):
    '''
    pnSaveCteC : empty
    '''
    tablaConst[p[-1]] = ['4',"direccionVirtual"]
    p[0] = None

def p_pnSaveFondoFalso(p):
    '''
    pnSaveFondoFalso : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

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
    pilaOperandos.put(p[-1])

    funcionActual = ""
    if currentFunction == "":
        funcionActual = currentScript
    else:
        funcionActual = currentFunction

    # dirFunc.registrosFunciones[funcionActual][tablaVariables][nombreVariable][tipo]
    pilaTipo.put(dirFunc.registrosFunciones[funcionActual][3][p[-1]][0])
    p[0] = None

def p_pnSaveOperandoConstante(p):
    '''
    pnSaveOperandoConstante : empty
    '''
    pilaOperandos.put(p[-2])
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
                # Sustituir con procedimiento avail
                global identificadorTemporales 
                identificadorTemporales += 1
                temporalActual = "temporal{}".format(identificadorTemporales)

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
                # Sustituir con procedimiento avail
                global identificadorTemporales 
                identificadorTemporales += 1
                temporalActual = "temporal{}".format(identificadorTemporales)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

    p[0] = None

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
                # Sustituir con procedimiento avail
                global identificadorTemporales 
                identificadorTemporales += 1
                temporalActual = "temporal{}".format(identificadorTemporales)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

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
                # Sustituir con procedimiento avail
                global identificadorTemporales 
                identificadorTemporales += 1
                temporalActual = "temporal{}".format(identificadorTemporales)

                nuevoCuadruplo = [operador,leftOperand,rightOperand,temporalActual]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
                pilaOperandos.put(temporalActual)
                pilaTipo.put(resultType)
                # missing: if any operand were a temporal space, return it to AVAIL
            else:
                print("ERROR: Type Mismatch")
                sys.exit()

def p_pnSaveOperadorAsign(p):
    '''
    pnSaveOperadorAsign : empty
    '''
    pilaOperadores.put(p[-1])
    p[0] = None

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
                nuevoCuadruplo = [operador,valor,"",aAsignar]
                cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
            else:
                print("Se deben asignar valores del mismo tipo")
                print("{} es {} \n {} es {}".format(valor,valorTipo,aAsignar,aAsignarTipo))
                sys.exit()

    p[0] = None

def p_pnCuadEscribe(p):
    '''
    pnCuadEscribe : empty
    '''
    if p[-3] == 'put':
        if p[-1] is None:
            toPrint = pilaOperandos.get()
            pilaTipo.get()

            operador = 'put'
            
            nuevoCuadruplo = [operador,"", "",toPrint]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        else:
            try:
                firstCharacter = p[-1][0]
                lastCharacter = p[-1][-1]

                if firstCharacter == '"' and lastCharacter == '"':
                    toPrint = p[-1]
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
        pilaTipo.get()

        operador = 'get'

        nuevoCuadruplo = [operador,"", "",leerVariable]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        print("Checar que lo que se lee es de un tipo de variable compatible")

    p[0] = None

def p_pnCuadCopy(p):
    '''
    pnCuadCopy : empty
    '''
    if p[-3] == 'copy':
        # Checar que sea un letrero y que termine en .csv
        if p[-1][0] == '"' and p[-1].endswith('.csv"'):
            toRead = p[-1]

            operador = 'copy'

            nuevoCuadruplo = [operador,"", "",toRead]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        else:
            print("You can only read from .csv files")
            sys.exit()

    p[0] = None

def p_pnCuadFuncEsp(p):
    '''
    pnCuadFuncEsp : empty
    '''
    top = p[-3]
    # Aquí no estoy manejando copy por el momento
    funcEspReturn = ['mean','mode','median','variance','max','min','staddes']
    funcEspGraficas = ['boxplot', 'linreg']

    if top in funcEspReturn:
        # Checar si es un arreglo o dataframe en un futuro
        print("al llamar funciones especiales, FALTA VALIDAR QUE SEA arreglo o dataframe")
        #cambiar result type, ahora está que regresan floats
        resultType = '3'

        toCalculate = pilaOperandos.get()
        pilaTipo.get()

        operador = top

        # Sustituir con procedimiento avail
        global identificadorTemporales 
        identificadorTemporales += 1
        temporalActual = "temporal{}".format(identificadorTemporales)

        nuevoCuadruplo = [operador,toCalculate, "",temporalActual]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        pilaOperandos.put(temporalActual)
        pilaTipo.put(resultType)

    elif top in funcEspGraficas:

        print("al llamar funciones especiales, FALTA VALIDAR QUE SEA arreglo o dataframe")
        toCalculate = pilaOperandos.get()
        pilaTipo.get()

        operador = top

        nuevoCuadruplo = [operador,"", "",toCalculate]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

# Cuadruplos No lineales

# IF
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

        nuevoCuadruplo = ['GotoF',result,"","_"]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)
        pilaSaltos.put(cuadruplos.getCont()-1)

    p[0] = None

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

def p_pnEndIf(p):
    '''
    pnEndIf : empty
    '''
    end = pilaSaltos.get()
    cuadruplos.fill(end,cuadruplos.getCont())
    p[0] = None

# WHILE
def p_pnSaveWhile(p):
    '''
    pnSaveWhile : empty
    '''
    pilaSaltos.put(cuadruplos.getCont())
    p[0] = None

# Estoy utilizando para checar que la expresion sea booleana, el mismo punto neuralgico de if
# def p_pnCheckBoolIf(p):

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

def p_pnSaveForID(p):
    '''
    pnSaveForID : empty
    '''
    print(p[-1])
    # checar que sea una variable que ya esté declarada en la funcion o en el scrpipt
    funcionActual = ""
    if currentFunction == "":
        funcionActual = currentScript
    else:
        funcionActual = currentFunction

    if p[-1] in dirFunc.registrosFunciones[funcionActual][3]:
        # Ver el tipo de la variable
        if semantica.convertion[dirFunc.registrosFunciones[funcionActual][3][p[-1]][0]] != 2:
            print("ERROR: Type Mismatch. You can only use an id with int as type")
            sys.exit()
        else:
            pilaOperandos.put(p[-1])
            pilaTipo.put(semantica.convertion[dirFunc.registrosFunciones[funcionActual][3][p[-1]][0]])
    else:
        print("Se debe declarar la variable a usar en el for loop")
        sys.exit()
    p[0] = None

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
        print("Exp es {}".format(exp))

        VControl = pilaOperandos.get()
        pilaOperandos.put(VControl)

        controlTipo = pilaTipo.get()
        pilaTipo.put(controlTipo)

        tipoRes = semantica.tablaSimbolos[semantica.convertion[controlTipo]][semantica.convertion[expTipo]]['==']
        
        if tipoRes == 0:
            print("ERROR Type Mismatch. Variable en for no puede asignar el tipo resultante de la expresión")
        else:
            nuevoCuadruplo = ['=',exp,"",VControl]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

            nuevoCuadruplo = ['=',VControl,"","VControl"]
            cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    p[0] = None

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

        nuevoCuadruplo = ['=',exp,"","VFinal"]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        # Sustituir con procedimiento avail
        global identificadorTemporales 
        identificadorTemporales += 1
        temporalActual = "temporal{}".format(identificadorTemporales)

        nuevoCuadruplo = ['<',"VControl","VFinal",temporalActual]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        pilaSaltos.put(cuadruplos.getCont()-1)

        nuevoCuadruplo = ['GotoF',temporalActual,"","_"]
        cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

        pilaSaltos.put(cuadruplos.getCont()-1)
    p[0] = None

def p_pnEndFor(p):
    '''
    pnEndFor : empty
    '''
    # Sustituir con procedimiento avail
    global identificadorTemporales 
    identificadorTemporales += 1
    temporalActual = "temporal{}".format(identificadorTemporales)

    nuevoCuadruplo = ['+',"VControl",1,temporalActual]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    nuevoCuadruplo = ['=',temporalActual,"","VControl"]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    debeSerIdOriginal = pilaOperandos.get()
    pilaOperandos.put(debeSerIdOriginal)

    nuevoCuadruplo = ['=',temporalActual,"",debeSerIdOriginal]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    fin = pilaSaltos.get()
    ret = pilaSaltos.get()

    nuevoCuadruplo = ['Goto',"","",ret]
    cuadruplos.listaCuadruplos.append(nuevoCuadruplo)

    cuadruplos.fill(fin,cuadruplos.getCont())

    elimina = pilaOperandos.get() #Sacamos el id original
    eliminaTipo = pilaTipo.get()
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
# filename = 'test.txt'
filename = 'testForLoop.txt'
fp = codecs.open(filename, "r", "utf-8")
text = fp.read()
fp.close()

with open(filename) as fp:
    try:
        yacc.parse(text)
    except EOFError:
        pass

# printDir()
print("LISTA DE CUADRUPLOS \n")
index = 1
for cuad in cuadruplos.listaCuadruplos:
    temp = [index] + cuad
    cuad = temp
    print(cuad)
    index += 1

# print(*cuadruplos.listaCuadruplos, sep="\n")
print("  \n\n TABLA CONSTANTES")
print(tablaConst)
