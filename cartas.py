class Cartas():
    def __init__(self, valor, nipe):
        self._valor = valor
        self._nipe = nipe
        self._nome = self.DefinirNome()
    
    def DefinirNome(self):
        if self.nipe == "Paus":
            if self.valor == 1:
                return "A ♣️"
            elif self.valor == 11:
                return "J ♣️"
            elif self.valor == 12:
                return "Q ♣️"
            elif self.valor == 13:
                return "K ♣️"
            else:
                return f"{self.valor} ♣️"
            
        if self.nipe == "Copa":
            if self.valor == 1:
                return "A ♥️"
            elif self.valor == 11:
                return "J ♥️"
            elif self.valor == 12:
                return "Q ♥️"
            elif self.valor == 13:
                return "K ♥️"
            else:
                return f"{self.valor} ♥️"

        if self.nipe == "Espada":
            if self.valor == 1:
                return "A ♠️"
            elif self.valor == 11:
                return "J ♠️"
            elif self.valor == 12:
                return "Q ♠️"
            elif self.valor == 13:
                return "K ♠️"
            else:
                return f"{self.valor} ♠️"
        
        if self.nipe == "Ouro":
            if self.valor == 1:
                return "A ♦️"
            elif self.valor == 11:
                return "J ♦️"
            elif self.valor == 12:
                return "Q ♦️"
            elif self.valor == 13:
                return "K ♦️"
            else:
                return f"{self.valor} ♦️"
    
    @property
    def valor(self):
        return self._valor
    @valor.setter
    def valor(self, valor):
        if isinstance(valor, int):
            self._valor = valor
    
    @property
    def nipe(self):
        return self._nipe
    @nipe.setter
    def nipe(self, valor):
        if isinstance(valor, str):
            if valor == "Paus" or valor == "Copa" or valor == "Espada" or valor == "Ouro":
                self._nipe = valor
            else:
                return
