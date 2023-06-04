Andrea Alejandra Ramírez Fernández

A00825062

# Statikx

Statikx es un lenguaje de alto nivel que funciona como una herramienta de análisis estadístico. A continuación existen ejemplos de cómo se puede utilizar

## Tipos de datos

Statikx permite la declaración de variables de tipo:
- int 
- float
- char
- dataframes

```
var int -> miVariable;
var float -> resultado;
```


Para asignarle a un valor a las variables de tipo dataframe se necesita utilizar el estatuto 'copy' para cargar los valores de un archivo externo.

## Operaciones

### Aritméticas

- \+
- \-
- \*
- \/

### Relacionales

- \>
- \<
- \==
- \!=

#### Lógicas

- \&&
- \||

## Estatutos secuenciales
- **put** para imprimir
- **get** para leer
- **copy** para leer un archivo .csv y copiarlo a un dataframe
- **=** para asignaciones 

## Condicionales

```
if(<expresion booleana>)
True{
    <estatuto>
    .
    .
    .
}False{
    <estauto>
    .
    .
    .
}
```

## While Loop

```
while(<expresion booleana>){
    <estauto>
    .
    .
    .
}
```

## For loop

```
for(var = <expresion int>, <expresion int>){
    <estauto>
    .
    .
    .
}
```

## Variables dimensionadas

Se pueden declarar arreglos y matrices con las variables de tipo: int, float y char

### Declaración de arreglos

```
var int[5] -> miArreglo;
var int[2,3] -> miMatriz;
```

### Indexación de arreglos

La indexación de arreglo empiza en 0

```
miArreglo[3] = 10;
miMatriz[0,2] = x + y;
```

## Funciones

Puedes crear tus propias funciones. Estas pueden regresar int, float, char, o ser declaradas como void

```
func <return> -> <nombre funcion>(<tipo parametro> -> <nombre parametro>){
    <estatuto>
    .
    .
    .
}
```

## Funciones estadísticas

Puedes utilizar las siguientes funciones para el análisis estadístico:

- mean
- median
- variance
- max
- min
- stadDes

Se debe incluir dos parámetros: 
1. Nombre de la variable de tipo dataframe
2. Index de la columna del dataframe a la que se quiere aplicar la función

Al llamarlas, se regresa un valor de tipo flotante.


```
var float -> promedio;
var dataframe -> calificaciones;

!! Puedes agregar tus comentarios con dos signos exclamativos al principio
copy(calificaciones,"verano2022.csv");

promedio = mean(calificaciones,0);;
```

## Funciones estadísticas gráficas

### Caja de bigotes

Se debe incluir dos parámetros:
1. Nombre de la variable de tipo dataframe
2. Un letrero con título para la gráfica

```
var dataframe -> tempMonterrey;

boxplot(tempMonterrey, "Temperaturas de Monterrey, Nuevo Leon 2023");
```

### Regresión Lineal

Se debe incluir tres parámetros:
1. Nombre de la variable de tipo dataframe
2. Index de columna 1 del dataframe
3. Index de columna 2 del dataframe

```
var dataframe -> indices;

linReg(indices,0,2);
```

# Estructura de un script

```
script ejemplo;

!! Declaración de variables globales
var int[3] -> datosA;

!! Declaración de funciones
func void -> imprime(int -> n, char -> flag){
    put(n);
    put(flag);
}

func int -> fact(int -> n){
    if(n == 0)
    True{
        returns 1;
    }False{
        returns n * fact(n - 1);;
    }
}

DO
{
    !! Declaración de variables globales
    var dataframe -> califs;

    !! Estatutos
    copy(califs,"notasVerano.csv");
    put(mean(califs,2););
    
}
```

# Correr Statikx

