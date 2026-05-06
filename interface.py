import tkinter as tk
from PIL import Image, ImageTk
import math
from jogador import Jogador
from mesa import Mesa
from fichas import Fichas

class App:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Menu")

        self.container = tk.Frame(self.janela)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.container, width=1200, height=800)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        img = Image.open("mesa_imagem.png")
        img = img.resize((1200, 800))
        self.bg = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        frame_centro = tk.Frame(self.container)
        frame_centro.grid(row=0, column=0)

        self.qtd_jogadores = 0

        self.Bjogar = tk.Button(
            frame_centro,
            text="Jogar",
            command=lambda : [self.Bjogar.grid_forget(),
                                self.Bsair.grid_forget(),
                                self.t.grid_forget(),
                                self.nome.grid_forget(),
                                self.Bvoltar_nome.grid_forget(),
                                self.B4.grid(row=0, column=0),
                                self.B6.grid(row=1, column=0),
                                self.B9.grid(row=2, column=0),
                                self.Bvoltar_jogar.grid(row=3, column=0)]
        )
        self.Bjogar.grid(row=0, column=0)

        self.Bsair = tk.Button(
            frame_centro,
            text="Sair",
            command=lambda : self.janela.destroy()
        )
        self.Bsair.grid(row=1, column=0)

        self.B4 = tk.Button(
            frame_centro,
            text="4 jogadores",
            command=lambda : (self.insira_seu_nome(), self.quantidade_jogadores(4))
        )
        self.B4.grid(row=0, column=0)
        self.B4.grid_forget()
        self.B6 = tk.Button(
            frame_centro,
            text="6 jogadores",
            command=lambda : (self.insira_seu_nome(), self.quantidade_jogadores(6))
        )
        self.B6.grid(row=1, column=0)
        self.B6.grid_forget()
        self.B9 = tk.Button(
            frame_centro,
            text="9 jogadores",
            command=lambda : (self.insira_seu_nome(), self.quantidade_jogadores(9))
        )
        self.B9.grid(row=2, column=0)
        self.B9.grid_forget()

        self.Bvoltar_jogar = tk.Button(
            frame_centro,
            text="Voltar",
            command=lambda : [  self.Bjogar.grid(row=0, column=0),
                                self.Bsair.grid(row=1, column=0),
                                self.B4.grid_forget(),
                                self.B6.grid_forget(),
                                self.B9.grid_forget(),
                                self.Bvoltar_jogar.grid_forget(),
                                self.nome.grid_forget(),
                                self.t.grid_forget(),
                                self.Bvoltar_nome.grid_forget()]
        )
        self.Bvoltar_jogar.grid(row=3, column=0)
        self.Bvoltar_jogar.grid_forget()

        self.t = tk.Label(frame_centro,
                     text="Insira seu Nome"
                     )
        self.t.grid(row=0, column=0)
        self.t.grid_forget()
        self.nome = tk.Entry(frame_centro
                             )
        self.nome.grid(row=1, column=0)
        self.nome.grid_forget()
        self.Bok = tk.Button(frame_centro,
                             text="Ok",
                             command=lambda : self.trocar_tela(Tela_jogo)
                             )
        self.Bok.grid(row=2, column=0)
        self.Bok.grid_forget()
        self.Bvoltar_nome = tk.Button(frame_centro,
                                      text="Voltar",
                                      command=lambda : [self.Bjogar.grid_forget(),
                                                        self.Bsair.grid_forget(),
                                                        self.B4.grid(row=0, column=0),
                                                        self.B6.grid(row=1, column=0),
                                                        self.B9.grid(row=2, column=0),
                                                        self.Bvoltar_jogar.grid(row=3, column=0),
                                                        self.nome.delete(0, tk.END), 
                                                        self.nome.grid_forget(),
                                                        self.Bok.grid_forget(),
                                                        self.t.grid_forget(),
                                                        self.Bvoltar_nome.grid_forget()]
                                      )
        self.Bvoltar_nome.grid(row=2, column=1)
        self.Bvoltar_nome.grid_forget() 

    def trocar_tela(self, tela):
        frame = Tela_jogo(self.container, self)
        frame.tkraise() 
    
    def insira_seu_nome(self):  
        self.Bjogar.grid_forget()
        self.Bsair.grid_forget()
        self.B4.grid_forget()
        self.B6.grid_forget()
        self.B9.grid_forget()
        self.Bvoltar_jogar.grid_forget()
        self.t.grid(row=0, column=0)
        self.nome.grid(row=1, column=0)
        self.Bok.grid(row=2, column=0)
        self.Bvoltar_nome.grid(row=2, column=1)

    def quantidade_jogadores(self, q):
        self.qtd_jogadores = q

class Tela_jogo(tk.Frame):
    def __init__(self, janela, app):
        super().__init__(janela)

        self.mesa = Mesa()
        self.app = app

        self.grid(row=0, column=0)
        self.canvas = tk.Canvas(self, width=1200, height=800, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        img = Image.open("mesa_imagem.png")
        img = img.resize((1200, 800))
        self.bg = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw") 

        self.x_jogador = 0
        self.y_jogador = 0

        self.jogadores = {}
        self.fichas_iniciais = []
        config = [
            (1000, 1),
            (500, 1),
            (100, 5),
            (50, 4),
            (20, 10),
            (10, 10)
        ]
        for valor, qtd in config:
            for _ in range(qtd):
                self.fichas_iniciais.append(Fichas(valor))

        self.player = Jogador(self.app.nome.get())
        self.jogadores[self.player.nome] = self.player

        for b in range(self.app.qtd_jogadores-1):
            bot = Jogador("", True, b+1)
            self.jogadores[bot.nome] = bot

        for jogador in self.jogadores.values():
            jogador.fichas = [Fichas(f.valor) for f in self.fichas_iniciais]

        imagens = [
        (10, ImageTk.PhotoImage(Image.open("ficha_10.png").resize((40, 40)))),
        (20, ImageTk.PhotoImage(Image.open("ficha_20.png").resize((40, 40)))),
        (50, ImageTk.PhotoImage(Image.open("ficha_50.png").resize((40, 40)))),
        (100, ImageTk.PhotoImage(Image.open("ficha_100.png").resize((40, 40)))),
        (500, ImageTk.PhotoImage(Image.open("ficha_500.png").resize((40, 40)))),
        (1000, ImageTk.PhotoImage(Image.open("ficha_1000.png").resize((40, 40))))
        ]

        self.imagens_fichas = imagens


        self.desenhar_mesa()
        self.desenhar_jogadores( list(self.jogadores.values()))

        self.atualizar_fichas_jogador()
        self.atualizar_fichas_mesa()

    def desenhar_jogadores(self, jogadores):
        self.canvas.delete("jogadores")
        self.canvas.delete("botao")

        cx, cy = 600, 400 
        raio = 300

        largura = 60
        altura = 90

        for i, jogador in enumerate(jogadores):
            angulo = 2 * math.pi * i / len(jogadores) + math.pi/2

            x = cx + raio * math.cos(angulo)
            y = cy + raio * math.sin(angulo)

            x1 = x - largura/2
            y1 = y - altura/2
            x2 = x + largura/2
            y2 = y + altura/2

            for j in range(2):
                offset = (j - 0.5) * (largura + 10)

                self.canvas.create_rectangle(
                    x1 + offset, y1,
                    x2 + offset, y2,
                    outline="white",
                    tags="jogadores"
                )
            self.canvas.create_text(
            x,
            y + altura/2 + 15,
            text= jogador.nome,
            fill="white",
            font=("Arial", 12, "bold"),
            tags="jogadores"
            )

            if not jogador.bot:
                Bfold = tk.Button(self,
                                  text="Fold",
                                  command=lambda : self.executar_acao("fold"),
                                  bg="red")
                Bcheck = tk.Button(self,
                                  text="Check",
                                  command=lambda : self.executar_acao("check",),
                                  bg="yellow")
                Bcall = tk.Button(self,
                                  text="Call",
                                  command=lambda : self.executar_acao("call"),
                                  bg="green")
                Braise = tk.Button(self,
                                  text="Raise",
                                  command=lambda : self.mostrar_fichas(),
                                  bg="blue")

                self.canvas.create_window(x-80, y-85, window=Bfold, tags="botao")
                self.canvas.create_window(x-30, y-85, window=Bcheck, tags="botao")
                self.canvas.create_window(x+20, y-85, window=Bcall, tags="botao")
                self.canvas.create_window(x+70, y-85, window=Braise, tags="botao")

                self.x_jogador = x
                self.y_jogador = y
    
    def desenhar_mesa(self):
        largura = 60
        altura = 90
        espaco = 15

        cx, cy = 600, 400

        total_largura = 5 * largura + 4 * espaco
        inicio_x = cx - total_largura / 2

        for i in range(5):
            x1 = inicio_x + i * (largura + espaco)
            y1 = cy - altura / 2

            self.canvas.create_rectangle(
                x1, y1,
                x1 + largura, y1 + altura,
                outline="yellow"
            )

    def mostrar_fichas(self):
        self.canvas.delete("fichas_clicar")
        self.canvas.delete("botao_ok")
        self.canvas.delete("botao_voltar")

        for i, (valor, img) in enumerate(self.imagens_fichas):
            offset_x = i*45

            btn_fichas = tk.Button(
                self,
                image=img,
                highlightthickness=0,
                command=lambda v=valor: self.selecionar_ficha(v)
            )
            self.canvas.create_window(
                self.x_jogador+100+offset_x, self.y_jogador+30,
                window=btn_fichas,
                tags="fichas_clicar"
            )
        btn_ok = tk.Button(
            self,
            text="Ok",
            bg="lightgreen",
            command= lambda v = self.player.aposta_rodada : self.mandar_valor_para_mesa(v)
        )

        btn_voltar = tk.Button(
            self,
            text="Voltar",
            bg="orange",
            command=lambda : self.voltar_ficha_para_o_jogador()
        )
        
        self.canvas.create_window(
            self.x_jogador+100, self.y_jogador+60,
            window=btn_ok,
            tags="botao_ok" 
        )

        self.canvas.create_window(
            self.x_jogador+150, self.y_jogador+60,
            window=btn_voltar,
            tags="botao_voltar" 
        )
    def selecionar_ficha(self, valor):
        ficha_encontrada = None
        for f in self.player.fichas:
            if f.valor == valor:
                ficha_encontrada = f
                break

        if ficha_encontrada:
            self.player.fichas.remove(ficha_encontrada)
            print(len(self.player.fichas))
            self.mesa.fichas_na_mesa.append(ficha_encontrada)
            self.player.aposta_rodada += valor

            self.atualizar_fichas_jogador()
            self.atualizar_fichas_mesa()

    def atualizar_fichas_jogador(self):
        self.canvas.delete("fichas_jogador")
        
        fichas_por_coluna = 5
        colunas_por_bloco = 5  
        
        espacamento_x = 25
        espacamento_y_camada = 32
        altura_ficha = 4    
        
        for i, ficha in enumerate(self.player.fichas):
            indice_coluna = i // fichas_por_coluna
            
            num_bloco = indice_coluna // colunas_por_bloco
            
            pos_coluna_no_bloco = indice_coluna % colunas_por_bloco
            
            pos_vertical = i % fichas_por_coluna
            
            x = self.x_jogador - (pos_coluna_no_bloco * espacamento_x) - 100
            
            y = self.y_jogador - (pos_vertical * altura_ficha) - (num_bloco * espacamento_y_camada) + 50
            
            self.canvas.create_image(
                x, y,
                image=ficha.img,
                tags="fichas_jogador"
            )

    def atualizar_fichas_mesa(self):
        self.canvas.delete("fichas_mesa")
        
        cx, cy = 600, 400
        fichas_por_pilha = 5
        pilhas_por_fileira = 10 
        
        espacamento_x = 25
        espacamento_z = 32     #profundidade
        altura_ficha = 4
        
        for i, ficha in enumerate(self.mesa.fichas_na_mesa):
            # pilha
            indice_pilha = i // fichas_por_pilha
            
            # fileira
            num_fileira = indice_pilha // pilhas_por_fileira
            
            # posição horizontal (0 a 4)
            pos_horizontal = indice_pilha % pilhas_por_fileira
            
            # Altura na pilha
            pos_vertical = i % fichas_por_pilha
            
            # X reseta a cada 5 pilhas
            x_final = cx - 100 + (pos_horizontal * espacamento_x)
            
            # Y sobe para cada nova fileira e sobe para cada ficha na pilha
            y_final = cy + 150 - (num_fileira * espacamento_z) - (pos_vertical * altura_ficha)
            
            self.canvas.create_image(
                x_final, 
                y_final, 
                image=ficha.img, 
                tags="fichas_mesa"
            )

    def executar_acao(self, acao, valor=0):
        self.mesa.turno_jogador(acao, self.player, valor)
        self.atualizar_fichas_jogador()
        self.atualizar_fichas_mesa()    
    
    def mandar_valor_para_mesa(self, valor):
        if valor <=0:
            return
        self.mesa.pote += valor
        self.executar_acao("raise", valor)
        self.player.aposta_rodada = 0

        self.canvas.delete("fichas_clicar")
        self.canvas.delete("botao_ok")
        self.canvas.delete("botao_voltar")

    def voltar_ficha_para_o_jogador(self):
        if self.mesa.fichas_na_mesa:
            ultima_ficha = self.mesa.fichas_na_mesa.pop()
            self.player.fichas.append(ultima_ficha)
            self.player.aposta_rodada -= ultima_ficha.valor

            self.atualizar_fichas_jogador()
            self.atualizar_fichas_mesa()    