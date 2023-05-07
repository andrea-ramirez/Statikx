import ply.lex as lex
import ply.yacc as yacc
from cuboSemantico import CuboSemantico
from directorioFunciones import DirectorioFunciones
import codecs
import json

# Tabla de constantes
# {int, int}
# {nombre, direccionVirtual}
tablaConst = {}

# Cubo Semántico
semantica = CuboSemantico()
# Se accede al cubo semantico de la siguiente forma:
# print(semantica.tablaSimbolos[2][2]['+'])

currentScript = ""
currentFunction = ""
currentTypeVar = ""

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
    copy : READ_FILE LEFT_PARENT LETRERO RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_file(p):
    '''
    file : ID
    '''
    p[0] = None

def p_variable(p):
    '''
    variable : ID indexp
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
    asign : variable ASIGN exp SEMICOLON
    '''
    p[0] = None

def p_lee(p):
    '''
    lee : READ LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_escribe(p):
    '''
    escribe :  WRITE LEFT_PARENT escribep RIGHT_PARENT SEMICOLON
    escribep : exp 
             | LETRERO
    '''
    p[0] = None

def p_return(p):
    '''
    return : RETURNS exp SEMICOLON
    '''
    p[0] = None

def p_exp(p):
    '''
    exp : exprel logic
    logic : logicsig exprel logic 
          | empty
    logicsig : AND 
             | OR
    '''
    p[0] = None

def p_exprel(p):
    '''
    exprel : e relacionalp
    relacionalp : relsig e relacionalp 
                | empty
    relsig : LESS_THAN 
           | GREATER_THAN 
           | EQUALS 
           | NOTEQUALS
    '''
    p[0] = None

def p_e(p):
    '''
    e : t tp
    tp : tsig t tp 
       | empty
    tsig : PLUS 
         | MINUS
    '''
    p[0] = None

def p_t(p):
    '''
    t : f fp
    fp : fsig f fp 
       | empty
    fsig : MULT 
         | DIV
    '''
    p[0] = None

def p_f(p):
    '''
    f : LEFT_PARENT exp RIGHT_PARENT
      | CTEI
      | CTEF
      | CTEC
      | variable
      | llamada
      | funcesp
    '''
    p[0] = None

def p_condicion(p):
    '''
    condicion : IF LEFT_PARENT exp RIGHT_PARENT IF_TRUE LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET falsop
    falsop : IF_FALSE  LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET 
           | empty
    '''
    p[0] = None

def p_ciclow(p):
    '''
    ciclow : WHILE LEFT_PARENT exp RIGHT_PARENT LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET
    '''
    p[0] = None

def p_ciclof(p):
    '''
    ciclof : FOR LEFT_PARENT asign exp RIGHT_PARENT LEFT_CUR_BRACKET estatutop RIGHT_CUR_BRACKET
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
    mean : MEAN LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_mode(p):
    '''
    mode : MODE LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_median(p):
    '''
    median : MEDIAN LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_variance(p):
    '''
    variance : VARIANCE LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_max(p):
    '''
    max : MAX LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_min(p):
    '''
    min : MIN LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_staddes(p):
    '''
    staddes : STADDES LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_boxplot(p):
    '''
    boxplot : BOXPLOT LEFT_PARENT variable RIGHT_PARENT SEMICOLON
    '''
    p[0] = None

def p_linreg(p):
    '''
    linreg : LINREG LEFT_PARENT variable RIGHT_PARENT SEMICOLON
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
    dirFunc.endScript(currentScript)
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

filename = 'testPropuesta.txt'
fp = codecs.open(filename, "r", "utf-8")
text = fp.read()
fp.close()

with open(filename) as fp:
    try:
        yacc.parse(text)
    except EOFError:
        pass

# printDir()