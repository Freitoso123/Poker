import random
from fichas import Fichas
class Jogador:
    def __init__(self, nome, bot=False, q=0):
        self._nome = self.definirnome(nome, bot, q)
        self._cartas = []
        self._fichas = []
        self._bot = bot
        self._correu = False
        self._aposta_rodada = 0
        self._acao = None
        self._all_in = False
        self.estilo = random.choice([
                        "tight",
                        "aggressive",
                        "passive",
                        "bluffer"
                            ])

    def definirnome(self, nome, bot, q):
        if not bot:
            return nome
        else:
            return f"Bot {q}"

    def pagar(self, valor):
        pago_total = 0
        for v in [1000, 500, 100, 50, 20, 10]:
            while valor >= v:
                pago = False
                for ficha in self._fichas:
                    if ficha.valor == v:
                        pago = True
                        valor -= v
                        pago_total += v
                        self._fichas.remove(ficha)
                        break
                if not pago:
                    self.all_in = True
                    break
        return pago_total         

    def decidir_acao(self, mesa):
        if len(mesa.cartas_na_mesa) == 0:
            score = self.avaliar_preflop()
        else:
            score = self.avaliar_posflop(mesa)
        chance = random.randint(1,100)
        if mesa.minima_aposta > 200:
            chance_fold = random.randint(1,100)
            if chance_fold < 20:
                return "fold"
        if score < 30 and mesa.minima_aposta == 0:
            if chance < 10:
                return "raise"
        if score < 25:
            if self.estilo == "bluffer" and chance < 15:
                return "raise"
            return "fold"
        elif score < 60:
            if chance < 70:
                return "call"
            else:
                return "fold"
        elif score < 100:
            if chance < 50:
                return "call"
            else:
                return "raise"
        else:
            if chance < 80:
                return "raise"
            else:
                return "call"


    def avaliar_posflop(self, mesa):

        cartas = self._cartas + mesa.cartas_na_mesa

        score = 0

        valores = []

        for carta in cartas:
            valores.append(carta.valor)

        contagem = {}

        for valor in valores:
            if valor not in contagem:
                contagem[valor] = 1
            else:
                contagem[valor] += 1

        cartas_por_naipe = {}

        for carta in cartas:

            if carta.nipe not in cartas_por_naipe:
                cartas_por_naipe[carta.nipe] = []

            cartas_por_naipe[carta.nipe].append(carta.valor)

        if 4 in contagem.values():
            score += 130
        elif 3 in contagem.values() and 2 in contagem.values():
            score += 110

        elif 3 in contagem.values():
            score += 70

        pares = 0

        for qtd in contagem.values():
            if qtd == 2:
                pares += 1

        if pares >= 2:
            score += 50

        elif pares == 1:
            score += 30

        valores_unicos = list(set(valores))
        valores_unicos.sort()

        sequencia = 1

        for i in range(len(valores_unicos)-1):

            if valores_unicos[i+1] == valores_unicos[i] + 1:
                sequencia += 1
            else:
                sequencia = 1

            if sequencia >= 5:
                score += 85
                break

        for lista in cartas_por_naipe.values():

            if len(lista) >= 5:
                score += 90

                lista = list(set(lista))
                lista.sort()

                sequencia = 1

                for i in range(len(lista)-1):

                    if lista[i+1] == lista[i] + 1:
                        sequencia += 1
                    else:
                        sequencia = 1

                    if sequencia >= 5:
                        score += 160

                        royal = {1, 10, 11, 12, 13}

                        if royal.issubset(set(lista)):
                            score += 250

        return score

    def avaliar_preflop(self):
        c1 = self._cartas[0]
        c2 = self._cartas[1]
        score = 0
        if c1.valor == c2.valor:
            score += 40
        if c1.nipe == c2.nipe:
            score += 12
        if abs(c1.valor - c2.valor) == 1:
            score += 8
        if c1.valor >= 10 or c1.valor == 1:
            score += 10
        if c2.valor >= 10 or c2.valor == 1:
            score += 10
        return score
    
    def receber_pote(self, valor):

        valores_fichas = [200, 100, 50, 25]

        for ficha_valor in valores_fichas:

            while valor >= ficha_valor:

                self._fichas.append(Fichas(ficha_valor))
                valor -= ficha_valor
    
    def mostrar_mao(self):
        for carta in self._cartas:
            print(carta.nome)
            
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if isinstance(valor, str) or valor is None:
            self._nome = valor

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
        return self._fichas

    @fichas.setter
    def fichas(self, novas_fichas):
        if isinstance(novas_fichas, list):
            self._fichas = novas_fichas
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
    def all_in(self):
        return self._all_in

    @all_in.setter
    def all_in(self, valor):
        if isinstance(valor, bool):
            self._all_in = valor 
