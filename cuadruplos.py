class Cuadruplo:
    listaCuadruplos = []

    def _init_(self):
        self.listaCuadruplos = []

    @classmethod
    def getCont(self):
        return len(self.listaCuadruplos) + 1
    
    @classmethod
    def fill(self,direccion,contador):
        # Restas uno porque lista de contadores empieza en 1
        self.listaCuadruplos[direccion-1][3] = contador