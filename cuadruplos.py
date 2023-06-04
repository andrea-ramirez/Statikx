# Clase con lista de cuadruplos
class Cuadruplo:
    listaCuadruplos = []

    def _init_(self):
        self.listaCuadruplos = []

    # Función que regresa el tamaño de la lista de cuadruplos
    # Utilizado para guardar contador en pilaSaltos
    @classmethod
    def getCont(self):
        return len(self.listaCuadruplos) + 1
    
    # Función que rellena el espacio faltante para brincos
    @classmethod
    def fill(self,direccion,contador):
        self.listaCuadruplos[direccion-1][3] = contador

