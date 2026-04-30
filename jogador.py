class Jogador:
    def __init__(self, nome, bot=False, q=0):
        self._nome = self.definirnome(nome, bot, q)
        self._cartas = []
        self._fichas = []
        self._bot = bot
        self._correu = False
        self._aposta_rodada = 0
        self._acao = None
        self._all_win = False

    def definirnome(self, nome, bot, q):
        if not bot:
            return nome
        else:
            return f"Bot {q}"

    def pagar(self, valor):
        for v in [200, 100, 50, 25]:
            while valor >= v:
                pago = False
                for ficha in self.fichas:
                    if ficha.valor == v:
                        pago = True
                        valor -= v
                        self.fichas.remove(ficha)
                        break
                if not pago:
                    self.all_win = True
                    break        

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
    
    @property
    def aposta_rodada(self):
        return self._aposta_rodada

    @aposta_rodada.setter
    def aposta_rodada(self, valor):
        if isinstance(valor, int):
            self._aposta_rodada = valor
    
    @property
    def correu(self):
        return self._correu

    @correu.setter
    def correu(self, valor):
        if isinstance(valor, bool):
            self._correu = valor

    @property
    def acao(self):
        return self._acao

    @acao.setter
    def acao(self, valor):
        if isinstance(valor, str) or valor is None:
            self._acao = valor

    @property
    def all_win(self):
        return self._all_win

    @all_win.setter
    def all_win(self, valor):
        if isinstance(valor, bool):
            self._all_win = valor 