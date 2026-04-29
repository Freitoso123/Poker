class Fichas:
    def __init__(self, valor):
        self._valor = valor
        self._cor = self.DefinirCor()
    
    def DefinirCor(self):
        if self.valor == 25:
            return "blue"
        elif self.valor == 50:
            return "green"
        elif self.valor == 100:
            return "yellow"
        else:
            return "red"

    @property
    def valor(self):
        return self._valor
    @valor.setter
    def valor(self, valor):
        try:
            valor = int(valor)
            if valor == 25 or valor == 50 or valor == 100 or valor == 200:
                self._valor = valor
            else:
                return
        except:
            return