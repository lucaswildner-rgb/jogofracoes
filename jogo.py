pip install pygame
import pygame
import random
import sys

# 1. Configurações Iniciais do Pygame
pygame.init()

# Cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (50, 200, 50)
VERMELHO = (200, 50, 50)
AZUL_CLARO = (173, 216, 230)

# Configurações da Tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("A Aventura dos Chefs de Fração (7º Ano)")

# Fontes
FONTE_GRANDE = pygame.font.Font(None, 48)
FONTE_MEDIA = pygame.font.Font(None, 36)
FONTE_PEQUENA = pygame.font.Font(None, 24)

# 2. Definição das Perguntas
def gerar_pergunta():
    """Gera uma nova pergunta (fração principal) e três opções."""
    
    # Frações simples para a "Receita"
    fracoes_base = ["1/2", "1/3", "2/3", "1/4", "3/4", "1/5", "2/5"]
    receita_base = random.choice(fracoes_base)
    
    num_base, den_base = map(int, receita_base.split('/'))
    
    # 2.1. Opção Correta (Equivalente)
    # Multiplica por um fator aleatório (entre 2 e 5)
    fator = random.randint(2, 5)
    num_correto = num_base * fator
    den_correto = den_base * fator
    
    op_correta = f"{num_correto}/{den_correto}"
    
    # 2.2. Opções Incorretas (Distratoras)
    opcoes_incorretas = []
    
    # Distrator 1: Troca a parte de cima/baixo
    op1_inc = f"{den_base}/{num_base}"
    opcoes_incorretas.append(op1_inc)
    
    # Distrator 2: Equivalente incorreta ou simplificação errada
    fator_inc = random.randint(2, 5)
    num2_inc = num_base * fator_inc
    den2_inc = den_base * (fator_inc + 1) # Denominador diferente
    op2_inc = f"{num2_inc}/{den2_inc}"
    opcoes_incorretas.append(op2_inc)

    # Garante que todas as opções sejam únicas (caso raro)
    opcoes_incorretas = list(set(opcoes_incorretas))
    
    # Monta a lista final de opções (1 correta + 2 incorretas)
    opcoes_finais = [op_correta] + random.sample(opcoes_incorretas, 2)
    random.shuffle(opcoes_finais)
    
    return receita_base, opcoes_finais, op_correta

# 3. Funções de Desenho
def desenhar_texto(texto, fonte, cor, x, y):
    """Desenha um texto na tela."""
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect(center=(x, y))
    TELA.blit(superficie_texto, retangulo_texto)

def desenhar_botao(texto, fonte, cor_fundo, cor_texto, retangulo):
    """Desenha um retângulo (botão) e o texto dentro dele."""
    pygame.draw.rect(TELA, cor_fundo, retangulo, border_radius=10)
    desenhar_texto(texto, fonte, cor_texto, retangulo.centerx, retangulo.centery)

# 4. Estado do Jogo
receita_atual = ""
opcoes_fracoes = []
resposta_correta = ""
pontuacao = 0
rodada = 1
max_rodadas = 5
mensagem = "Escolha o ingrediente correto!"
cor_mensagem = PRETO

# 5. Inicialização da Rodada
def nova_rodada():
    """Prepara o estado para a próxima pergunta."""
    global receita_atual, opcoes_fracoes, resposta_correta, rodada, mensagem, cor_mensagem
    
    if rodada > max_rodadas:
        return False # Fim do jogo
        
    receita_atual, opcoes_fracoes, resposta_correta = gerar_pergunta()
    mensagem = f"Rodada {rodada}: Escolha a fração equivalente a **{receita_atual}**"
    cor_mensagem = PRETO
    rodada += 1
    return True

# 6. Lógica de Clique
def checar_clique(posicao_mouse, retangulos_opcoes):
    """Verifica se o usuário clicou em uma das opções."""
    global pontuacao, mensagem, cor_mensagem
    
    for i, ret in enumerate(retangulos_opcoes):
        if ret.collidepoint(posicao_mouse):
            fracao_selecionada = opcoes_fracoes[i]
            
            if fracao_selecionada == resposta_correta:
                pontuacao += 1
                mensagem = "🎉 Acertou! Ingrediente Correto!"
                cor_mensagem = VERDE
            else:
                mensagem = f"❌ Errado! A resposta era **{resposta_correta}**."
                cor_mensagem = VERMELHO
            
            # Pequeno atraso para o jogador ver o resultado
            pygame.time.delay(1000) 
            
            # Inicia a próxima rodada após o clique
            nova_rodada()
            break

# Inicia o jogo
if not nova_rodada():
    # Isso não deve acontecer na primeira execução, mas garante a segurança
    pygame.quit()
    sys.exit()

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Lógica de clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and rodada <= max_rodadas:
            checar_clique(evento.pos, retangulos_opcoes)
            
    # 7. Desenho
    TELA.fill(AZUL_CLARO) # Cor de fundo (balcão ou céu)
    
    # Desenhar Título/Pontuação
    desenhar_texto("A AVENTURA DOS CHEFS DE FRAÇÃO", FONTE_GRANDE, PRETO, LARGURA // 2, 50)
    desenhar_texto(f"Pontuação: {pontuacao}", FONTE_MEDIA, PRETO, LARGURA - 100, 30)

    # Desenhar a Receita (Fração Base)
    desenhar_texto("REQUISITO DA RECEITA:", FONTE_MEDIA, PRETO, LARGURA // 2, 150)
    desenhar_texto(receita_atual, FONTE_GRANDE, VERMELHO, LARGURA // 2, 200)

    # Desenhar a Mensagem de Feedback
    desenhar_texto(mensagem.replace('**',''), FONTE_MEDIA, cor_mensagem, LARGURA // 2, 270) # Remove a formatação markdown para o Pygame

    # Desenhar Opções (Ingredientes) - 3 botões na parte inferior
    posicoes_x = [LARGURA // 4, LARGURA // 2, LARGURA * 3 // 4]
    retangulos_opcoes = []
    
    for i, fracao in enumerate(opcoes_fracoes):
        x = posicoes_x[i]
        y = 450
        largura_botao = 150
        altura_botao = 80
        
        ret = pygame.Rect(x - largura_botao // 2, y - altura_botao // 2, largura_botao, altura_botao)
        
        # Cor dos botões (temporariamente cinza claro)
        cor_botao = (220, 220, 220)
        
        desenhar_botao(fracao, FONTE_MEDIA, cor_botao, PRETO, ret)
        retangulos_opcoes.append(ret)

    # 8. Tela de Fim de Jogo
    if rodada > max_rodadas:
        TELA.fill(BRANCO)
        desenhar_texto("FIM DO JOGO!", FONTE_GRANDE, PRETO, LARGURA // 2, 200)
        desenhar_texto(f"Sua Pontuação Final: {pontuacao} de {max_rodadas}", FONTE_MEDIA, PRETO, LARGURA // 2, 300)
        desenhar_texto("Pressione ESC para Sair", FONTE_PEQUENA, PRETO, LARGURA // 2, 400)
        
        # Permite sair com ESC no fim do jogo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            rodando = False

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
sys.exit()