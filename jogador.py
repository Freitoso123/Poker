class Jogador:
    def __init__(self, nome, bot=False, q=0):
        self._nome = self.DefinirNome(nome, bot, q)
        self._cartas = []
        self._fichas = []
        self._bot = bot

    def DefinirNome(self, nome, bot, q):
        if not bot:
            return nome
        else:
            return f"Bot {q}"

    def AumentarAposta(self, fichas):
        aumento = 0
        for i in range(len(fichas)):
            if fichas[i] in self.fichas:
                aumento += fichas[i].valor
        return aumento

    def Mesa():
        return True

    def Correr():
        return True

    @property
    def bot(self):
        return self._bot
    @bot.setter
    def bot(self, bot):
        if isinstance(bot, bool):
            self._bot = bot
        else:
            return
    
    @property
    def cartas(self):
        return self._cartas.copy()

    @cartas.setter
    def cartas(self, novas_cartas):
        if isinstance(novas_cartas, list):
            self._cartas = novas_cartas.copy()
        else:
            return

    @property
    def fichas(self):
        return self._fichas.copy()

    @fichas.setter
    def fichas(self, novas_fichas):
        if isinstance(novas_fichas, list):
            self._fichas = novas_fichas.copy()
        else:
            return