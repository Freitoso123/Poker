from cartas import Cartas
from jogador import Jogador
import random
class Mesa:
    def __init__(self):
        self.jogadores = []
        self.baralho = []
        self.pote = 0
        self.cartas_na_mesa = []
        self.aposta_rodada = 0
        self.dealer = -1
        self.small_blind = 0
        self.big_blind = 1
    
    def jogar(self):
        while True:
            self.resetar()
            self.iniciar_partida()
            continuar = input("Nova mão (s/n): ")
            if continuar.lower() != "s":
                break
    
    def iniciar_partida(self):
        self.baralho = []
        self.pote = 0
        self.cartas_na_mesa = []
        self.avancar_posicoes()
        self.criar_baralho()
        self.embaralhar()
        self.limpar_mao()
        self.distribuir_cartas()
        self.cobrar_blinds()
        self.rodada_apostas(pre_flop=True)
        self.resetar_apostas()
        self.flop()
        self.rodada_apostas()
        self.resetar_apostas()
        self.turn()
        self.rodada_apostas()
        self.resetar_apostas()
        self.river()
        self.rodada_apostas()
        self.showdown()



    def criar_baralho(self):
        naipes = ["Paus", "Copa", "Espada", "Ouro"]
        for i in naipes:
            for j in range(1, 14):
                c = Cartas(j, i)
                self.baralho.append(c)

    def embaralhar(self):
        random.shuffle(self.baralho)
    
    def limpar_mao(self):
        for jogador in self.jogadores:
            jogador._cartas = []
            jogador._correu = False
            jogador._aposta_rodada = 0
            jogador._acao = None

    def avancar_posicoes(self):
        total = len(self.jogadores)
        self.dealer = (self.dealer + 1) % total
        self.small_blind = (self.dealer + 1) % total
        self.big_blind = (self.dealer + 2) % total

    
    def distribuir_cartas(self):
        total = len(self.jogadores)
        inicio = (self.dealer + 1) % total
        for _ in range(2):
            for i in range(total):
                indice = (inicio + i) % total
                jogador = self.jogadores[indice]
                carta = self.baralho.pop()
                jogador._cartas.append(carta)
    
    def turno_jogador(self, jogador):
        print(f"Vez de {jogador._nome}")
        if jogador.bot:
            acao = "a definir"
            #algoritmo do bot
        else:
            acao = input("fold / check / call / raise: ")
        jogador._acao = acao
        if acao == "fold":
            jogador._correu = True
        elif acao == "check":
            pass
        elif acao == "call":
            diferenca = self.aposta_rodada - jogador._aposta_rodada
            jogador._aposta_rodada += diferenca
            self.pote += diferenca
        elif acao == "raise":
            valor = int(input("Quanto aumentar? "))
            diferenca = self.aposta_rodada - jogador._aposta_rodada
            total = diferenca + valor
            jogador._aposta_rodada += total
            self.pote += total
            self.aposta_rodada += valor

    def rodada_apostas(self, pre_flop=False):
        while not self.apostas_encerradas():
            total = len(self.jogadores)
            if pre_flop:
                inicio = (self.big_blind + 1) % total
            else:
                inicio = (self.dealer + 1) % total
            for i in range(total):
                indice = (inicio + i) % total
                jogador = self.jogadores[indice]
                if jogador._correu:
                    continue
                self.turno_jogador(jogador)
    
    def apostas_encerradas(self):
        for jogador in self.jogadores:
            if jogador._correu:
                continue
            if jogador._aposta_rodada != self.aposta_rodada:
                return False
        return True
    
    def resetar_apostas(self):
        self.aposta_rodada = 0
        for jogador in self.jogadores:
            jogador._aposta_rodada = 0
            jogador._acao = None

    def flop(self):
        for _ in range(3):
            carta = self.baralho.pop()
            self.cartas_na_mesa.append(carta)

    def turn(self):
        carta = self.baralho.pop()
        self.cartas_na_mesa.append(carta)
    
    def river(self):
        carta = self.baralho.pop()
        self.cartas_na_mesa.append(carta)

    def showdown(self):
        pass
        #algoritmo do ganhador
    
    def resetar(self):
        self.baralho = []
        self.cartas_na_mesa = []
        self.pote = 0
        self.aposta_rodada = 0
        self.limpar_mao()
    
    def cobrar_blinds(self):

        small = self.jogadores[self.small_blind]
        big = self.jogadores[self.big_blind]
        small._aposta_rodada = 10
        big._aposta_rodada = 20
        self.pote += 30
        self.aposta_rodada = 20