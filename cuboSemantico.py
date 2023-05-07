# Las constantes se redireccionan se buscan como de tipo simple que le corresponde
# false     -> 0
# true      -> 1
# int       -> 2
# float     -> 3
# char      -> 4

#Hashmap of hashmaps anidados
class CuboSemantico:
    tablaSimbolos = {
        0 : {
            0 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 1,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            1 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 1,
                '&&' : 0,
                '||' : 1,
                },
            2 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            3 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            4 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            },
        1 : {
            0 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 1,
                '&&' : 0,
                '||' : 1,
                },
            1 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 1,
                '!=' : 0,
                '&&' : 1,
                '||' : 1,
                },
            2 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            3 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            4 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            },
        2 : {
            0 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            1 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            2 : {'+' : 2,
                '-' : 2,
                '*' : 2,
                '/' : 3,
                '>' : 1,
                '<' : 1,
                '==' : 1,
                '!=' : 1,
                '&&' : 0,
                '||' : 0,
                },
            3 : {'+' : 3,
                '-' : 3,
                '*' : 3,
                '/' : 3,
                '>' : 1,
                '<' : 1,
                '==' : 1,
                '!=' : 1,
                '&&' : 0,
                '||' : 0,
                },
            4 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            },
        3 : {
            0 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            1 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            2 : {'+' : 3,
                '-' : 3,
                '*' : 3,
                '/' : 3,
                '>' : 1,
                '<' : 1,
                '==' : 1,
                '!=' : 1,
                '&&' : 0,
                '||' : 0,
                },
            3 : {'+' : 3,
                '-' : 3,
                '*' : 3,
                '/' : 3,
                '>' : 1,
                '<' : 1,
                '==' : 1,
                '!=' : 1,
                '&&' : 0,
                '||' : 0,
                },
            4 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            },
        4 : {
            0 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            1 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            2 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            3 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' :0,
                '==' : 0,
                '!=' : 0,
                '&&' : 0,
                '||' : 0,
                },
            4 : {'+' : 0,
                '-' : 0,
                '*' : 0,
                '/' : 0,
                '>' : 0,
                '<' : 0,
                '==' : 1,
                '!=' : 1,
                '&&' : 0,
                '||' : 0,
                },
            },
    }
    convertion = {
        'int' : 2,
        'float' : 3,
        'char' : 4,
    }
    
    def _init_(self,tablaSimbolos):
        self.tablaSi = tablaSimbolos

# prueba = CuboSemantico()
# print(prueba.tablaSimbolos[1][2]['+'])