from PIL import Image, ImageTk

class Fichas:
    def __init__(self, valor):
        self._valor = valor
        self.img = self.definir_imagem()
        
    def definir_imagem(self):
        if self.valor == 10:
            img = Image.open("ficha_10.png")
        elif self.valor == 20:
            img = Image.open("ficha_20.png")
        elif self.valor == 50:
            img = Image.open("ficha_50.png")
        elif self.valor == 100:
            img = Image.open("ficha_100.png")
        elif self.valor == 500:
            img = Image.open("ficha_500.png")
        elif self.valor == 1000:
            img = Image.open("ficha_1000.png")
        else:
            return None

        img = img.resize((20, 20))
        return ImageTk.PhotoImage(img)
        
    @property
    def valor(self):
        return self._valor
    @valor.setter
    def valor(self, valor):
        try:
            valor = int(valor)
            if valor == 10 or valor == 20 or valor == 50 or valor == 100 or valor == 500 or valor == 1000:
                self._valor = valor
            else:
                return
        except:
            return