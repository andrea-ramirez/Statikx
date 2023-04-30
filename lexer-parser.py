import ply.lex as lex
import ply.yacc as yacc
import sys

#  LEXER
reserved = {
    'script' : 'SCRIPT',        # script
    'var' : 'VAR',
    'func' : 'FUNC',
    'DO' : 'DO',                # DO main function
    'if' : 'IF',
    'True{' : 'IF_TRUE',
    'False{' : 'IF_FALSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'returns' : 'RETURNS',
    'get' : 'READ',
    'put' : 'WRITE',
    'copy' : 'READ_FILE',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'void' : 'VOID',
    'mean' : 'MEAN',            # mean special function
    'mode' : 'MODE',            # mode special function
    'median' : 'MEDIAN',        # median special function
    'variance' : 'VARIANCE',    # variance special function
    'max' : 'MAX',              # max special function
    'min' : 'MIN',              # min special function
    'stadDes' : 'STADDES',      # stadDes special function standard deviation
    'boxplot' : 'BOXPLOT',      # boxPlot special function
    'linReg' : 'LINREG',        # linReg special function simple linear regression
}

tokens = [
    'ID',                   # id
    'LETRERO',              # "letreros"
    'DATAFRAME',            # dataframe
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

#  MISSING 
# dataframe
# checar character

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
  r'[a-zA-Z0-9!@#$%^&_]'
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

def test_lexer():
  lexer.input('''
                script example01;

                !!Variables globales
                var int -> x, y;
                var dataframe -> df1, df2;

                !!Funciones
                func float -> half(int -> x1){
                    returns x1/2;
                }

                func void -> leerVariable(){
                    var int -> x;
                get(x);
                    while(x < 3){
                    get(x);
                }
                }

                DO
                {

                df1 = copy("DatosEnero2023.csv");
                df2 = df1;

                var int -> jumpSize;
                jumpSize = leerVariable();

                i = 0;
                for(i = 0; jumpSize){
                    df1[0,i] = -1;
                }

                !! Draws boxplot of edited df1 and original df2 dataframes 
                put(boxplot(df1));
                put(boxplot(df2));
                    
                    if(mean(df1) > mean(df2))
                True{
                    put("El mayor promedio es el de dataframe df1 con ");
                    put(mean(df1));
                }False{
                    put("El mayor promedio es el de dataframe df2 con ");
                    put(mean(df2));
                }                      
                }
                      
              ''')

  while True:
    tok = lexer.token()
    if not tok:
      break;

    print(tok)

test_lexer()