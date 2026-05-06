from cartas import Cartas
from jogador import Jogador
import random
class Mesa:
    def __init__(self):
        self.jogadores = []
        self.baralho = []
        self.fichas_na_mesa = []
        self.pote = 0
        self.cartas_na_mesa = []
        self.minima_aposta = 0
        self.dealer = -1
        self.small_blind = 0
        self.big_blind = 1

        self.etapa_atual = "pre_flop"
        self.inidice_jogador_atual = 0
    
    def proxima_etapa(self):
        etapas = ["pre_flop", "flop", "turn", "river", "showdown"]
        indice = etapas.index(self.etapa_atual)
        
        if self.etapas_encerradas():
            if self.etapa_atual == "pre_flop":
                self.flop()
                self.etapa_atual = "flop"
            elif self.etapa_atual == "flop":
                self.turn()
                self.etapa_atual = "turn"
            elif self.etapa_atual == "turn":
                self.river()
                self.etapa_atual = "showdown"
    
            self.resetar_apostas()

    def jogar(self):
        while True:
            self.resetar()
            self.iniciar_partida()
    
    def mostrar_mesa(self):
        print("Mesa:")

        for carta in self.cartas_na_mesa:
            print(carta.nome)

    def iniciar_partida(self):
        self.criar_baralho()
        
        self.embaralhar()

        self.distribuir_cartas()
        self.cobrar_blinds()
        self.rodada_apostas(pre_flop=True)
        self.resetar_apostas()
        self.flop()
        self.mostrar_mesa()
        self.rodada_apostas()
        self.resetar_apostas()
        self.turn()
        self.mostrar_mesa()
        self.rodada_apostas()
        self.resetar_apostas()
        self.river()
        self.mostrar_mesa()
        self.rodada_apostas()
        self.showdown()

    
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

    def rodada_apostas(self, pre_flop=False):
        while not self.apostas_encerradas():
            total = len(self.jogadores)
            if pre_flop:
                inicio = (self.big_blind + 1) % total
            else:
                inicio = (self.dealer + 1) % total
            for i in range(total):
                if self.jogadores_ativos() == 1:
                    self.showdown()
                    return
                indice = (inicio + i) % total
                jogador = self.jogadores[indice]
                if jogador._correu:
                    continue
                self.turno_jogador(jogador)

    def turno_jogador(self, acao, jogador, valor=0):
        if jogador.bot:
            acao = jogador.decidir_acao(self)

        jogador.acao = acao

        if acao == "fold":
            jogador.correu = True
        elif acao == "check":
            pass
        elif acao == "call":
            diferenca = jogador.pagar(self.minima_aposta - jogador.aposta_rodada)
            jogador.aposta_rodada += diferenca
            self.pote += diferenca 
        elif acao == "raise":
            #verificar se o valor é maior que a diferença pra mesa
            diferenca = self.minima_aposta - jogador.aposta_rodada
            total = diferenca + valor
            pago = jogador.pagar(total)
            jogador.aposta_rodada += pago
            self.pote += pago
            if not jogador.all_in:
                self.minima_aposta = jogador.aposta_rodada
            
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