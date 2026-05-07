from cartas import Cartas
from jogador import Jogador
import random
class Mesa:
    def __init__(self):
        self.estado = "INICIO"
        self.jogadores = []
        self.baralho = []
        self.fichas_na_mesa = []
        self.pote = 0
        self.cartas_na_mesa = []
        self.minima_aposta = 0
        self.dealer = -1
        self.small_blind = 0
        self.big_blind = 1
        self.jogador_atual = 0
        self.ultimo_que_aumentou = None
    
    def proximo_estado(self):
        if self.estado == "INICIO":
            self.criar_baralho()
            self.avancar_posicoes()
            self.embaralhar()
            self.limpar_mao()
            self.distribuir_cartas()
            self.cobrar_blinds()
            self.estado = "PRE_FLOP"
        elif self.estado == "PRE_FLOP":
            self.iniciar_apostas(pre_flop=True)
            self.estado = "TURNO"
        elif self.estado == "TURNO":

            if self.jogadores_ativos() == 1:
                self.estado = "SHOWDOWN"
                return

            jogador = self.jogadores[self.jogador_atual]

            if jogador.correu or jogador.all_in:
                self.proximo_jogador()
                return

            if jogador.bot:
                acao = jogador.decidir_acao(self)
                self.executar_acao(jogador, acao)
                self.proximo_jogador()
            else:
                self.estado = "AGUARDANDO_JOGADOR"

        elif self.estado == "AGUARDANDO_JOGADOR":
            #tem q sair depois (é aqui que vai o input)
            return

        elif self.estado == "FLOP":
            self.flop()
            self.iniciar_apostas()
            self.estado = "TURNO"
        elif self.estado == "TURN":
            self.turn()
            self.iniciar_apostas()
            self.estado = "TURNO"
        elif self.estado == "RIVER":
            self.river()
            self.iniciar_apostas()
            self.estado = "TURNO"
        elif self.estado == "SHOWDOWN":
            self.showdown()
            self.resetar()
            self.estado = "INICIO"

    def iniciar_apostas(self, pre_flop=False):
        self.ultimo_que_aumentou = None
        total = len(self.jogadores)

        if pre_flop:
            self.jogador_atual = (self.big_blind + 1) % total
        else:
            self.jogador_atual = (self.dealer + 1) % total
    
    def executar_acao(self, jogador, acao, valor=0):
        if acao == "fold":
            jogador. correu = True

        elif acao == "check":
            if jogador.aposta_rodada < self.minima_aposta:
                return  

        elif acao == "call":
            diferenca = self.minima_aposta - jogador.aposta_rodada
            pago = jogador.pagar(diferenca)
            jogador.aposta_rodada += pago
            self.pote += pago

        elif acao == "raise":
            diferenca = self.minima_aposta - jogador.aposta_rodada
            total = diferenca + valor

            pago = jogador.pagar(total)
            jogador.aposta_rodada += pago
            self.pote += pago

            if jogador.aposta_rodada > self.minima_aposta:
                self.minima_aposta = jogador.aposta_rodada
                self.ultimo_que_aumentou = jogador

    def criar_baralho(self):
        naipes = ["Paus", "Copa", "Espada", "Ouro"]
        for i in naipes:
            for j in range(1, 14):
                c = Cartas(j, i)
                self.baralho.append(c)
        self.avancar_posicoes()

    def embaralhar(self):
        random.shuffle(self.baralho)
    
    def limpar_mao(self):
        for jogador in self.jogadores:
            jogador.cartas = []
            jogador.correu = False
            jogador.aposta_rodada = 0
            jogador.acao = None
            jogador.all_in = False

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

    def proximo_jogador(self):
        total = len(self.jogadores)
        jogador_anterior = self.jogadores[self.jogador_atual]

        self.jogador_atual = (self.jogador_atual + 1) % total
        jogador_atual = self.jogadores[self.jogador_atual]

    
        if self.apostas_encerradas():
            if self.ultimo_que_aumentou is None:
                terminou = True
            elif jogador_atual == self.ultimo_que_aumentou:
                terminou = True
            else:
                terminou = False
        else:
            terminou = False

        if terminou:
            self.resetar_apostas()

            if len(self.cartas_na_mesa) == 0:
                self.estado = "FLOP"
            elif len(self.cartas_na_mesa) == 3:
                self.estado = "TURN"
            elif len(self.cartas_na_mesa) == 4:
                self.estado = "RIVER"
            else:
                self.estado = "SHOWDOWN"

    '''def rodada_apostas(self, pre_flop=False):

        if self.jogadores_ativos() == 1:
            self.estado = "SHOWDOWN"
            return

        total = len(self.jogadores)

        if pre_flop:
            inicio = (self.big_blind + 1) % total
        else:
            inicio = (self.dealer + 1) % total

        while True:
            mudou = False

            for i in range(total):
                indice = (inicio + i) % total
                jogador = self.jogadores[indice]

                if jogador.correu:
                    continue

                aposta_antes = self.minima_aposta

                self.turno_jogador(jogador)

                if self.minima_aposta > aposta_antes:
                    mudou = True

            if not mudou and self.apostas_encerradas():
                break'''

    '''def turno_jogador(self, jogador):
        print(f"Vez de {jogador._nome}")
        if jogador.bot:
            acao = jogador.decidir_acao(self)

        jogador.acao = acao

        if acao == "fold":
            jogador.correu = True
        elif acao == "check":
            if jogador.aposta_rodada < self.minima_aposta:
                return self.turno_jogador(jogador)
        elif acao == "call":
            diferenca = jogador.pagar(self.minima_aposta - jogador.aposta_rodada)
            jogador.aposta_rodada += diferenca
            self.pote += diferenca 
        elif acao == "raise":
            if jogador.bot:
                if jogador.estilo == "aggressive":
                    valor = max(25, self.minima_aposta // 2)
                else:
                    valor = random.randint(self.minima_aposta, self.minima_aposta + 75)
            else:
                valor = int(input("Quanto aumentar? "))
            diferenca = self.minima_aposta - jogador.aposta_rodada
            total = diferenca + valor
            pago = jogador.pagar(total)
            jogador.aposta_rodada += pago
            self.pote += pago
            if jogador.aposta_rodada > self.minima_aposta:
                self.minima_aposta = jogador.aposta_rodada'''
            
    def interagir_interfaca(acao):
        return acao
    
    def apostas_encerradas(self):
        for jogador in self.jogadores:
            if jogador.correu:
                continue
            if jogador.aposta_rodada != self.minima_aposta:
                return False
        return True
    
    def resetar_apostas(self):
        self.minima_aposta = 0
        for jogador in self.jogadores:
            jogador.aposta_rodada = 0
            jogador.acao = None

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

        jogadores_validos = []

        for jogador in self.jogadores:
            if not jogador.correu:
                jogadores_validos.append(jogador)

        melhor_score = -1
        vencedores = []

        for jogador in jogadores_validos:

            jogador.mostrar_mao()

            score = jogador.avaliar_posflop(self)

            if score > melhor_score:
                melhor_score = score
                vencedores = [jogador]

            elif score == melhor_score:
                vencedores.append(jogador)

        if len(vencedores) == 1:

            vencedor = vencedores[0]
            vencedor.receber_pote(self.pote)

            print(f"{vencedor._nome} venceu {self.pote}")

        else:

            valor = self.pote // len(vencedores)
            for jogador in vencedores:
                jogador.receber_pote(valor)

            print("Empate")

        self.pote = 0
            
    
    def resetar(self):
        self.baralho = []
        self.cartas_na_mesa = []
        self.pote = 0
        self.minima_aposta = 0
        self.limpar_mao()

    
    def cobrar_blinds(self):
        small = self.jogadores[self.small_blind]
        big = self.jogadores[self.big_blind]
        small.aposta_rodada = small.pagar(20)
        big.aposta_rodada = big.pagar(50)
        self.pote = (small.aposta_rodada+big.aposta_rodada)
        self.minima_aposta = big.aposta_rodada
    
    def jogadores_ativos(self):
        ativos = 0

        for jogador in self.jogadores:
            if not jogador.correu:
                ativos += 1

        return ativos