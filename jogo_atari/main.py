# main.py — Ponto de entrada e loop principal do jogo Destruidor de Asteroides

# pyrefly: ignore [missing-import]
import pygame
import random
import sys

from config import (
    LARGURA_TELA, ALTURA_TELA, FPS,
    COR_FUNDO, COR_TEXTO, COR_ESTRELA,
    INTERVALO_ASTEROIDE, COOLDOWN_TIRO,
    NAVE_ALTURA, NUM_ESTRELAS
)
from nave import Nave
from projetil import Projetil
from asteroide import Asteroide


def gerar_estrelas():
    """
    Gera posições aleatórias para as estrelas do fundo.
    Cada estrela tem posição (x, y), brilho e tamanho aleatórios.
    """
    estrelas = []
    for _ in range(NUM_ESTRELAS):
        x = random.randint(0, LARGURA_TELA)
        y = random.randint(0, ALTURA_TELA)
        brilho = random.randint(100, 255)
        tamanho = random.choice([1, 1, 1, 2])  # Maioria das estrelas são pequenas
        estrelas.append((x, y, brilho, tamanho))
    return estrelas


def desenhar_estrelas(tela, estrelas):
    """Desenha o campo de estrelas no fundo da tela."""
    for x, y, brilho, tamanho in estrelas:
        cor = (brilho, brilho, min(255, brilho + 50))  # Tom levemente azulado
        if tamanho == 1:
            tela.set_at((x, y), cor)
        else:
            pygame.draw.circle(tela, cor, (x, y), tamanho)


def desenhar_pontuacao(tela, fonte, pontuacao):
    """Renderiza a pontuação no canto superior esquerdo da tela."""
    texto = fonte.render(f"Pontuação: {pontuacao}", True, COR_TEXTO)
    tela.blit(texto, (15, 15))


def tela_game_over(tela, fonte_grande, fonte_media, pontuacao):
    """
    Exibe a tela de Game Over com a pontuação final.
    Retorna True se o jogador quiser reiniciar, False se quiser sair.
    """
    # Fundo escurecido (overlay semitransparente)
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    tela.blit(overlay, (0, 0))

    # Texto "GAME OVER" em vermelho
    texto_game_over = fonte_grande.render("GAME OVER", True, (255, 50, 50))
    rect_go = texto_game_over.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 60))
    tela.blit(texto_game_over, rect_go)

    # Pontuação final
    texto_pontuacao = fonte_media.render(f"Pontuação Final: {pontuacao}", True, COR_TEXTO)
    rect_pont = texto_pontuacao.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 10))
    tela.blit(texto_pontuacao, rect_pont)

    # Instruções para reiniciar ou sair
    texto_reiniciar = fonte_media.render("Pressione R para reiniciar", True, (100, 255, 150))
    rect_r = texto_reiniciar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 60))
    tela.blit(texto_reiniciar, rect_r)

    texto_sair = fonte_media.render("Pressione ESC para sair", True, (200, 200, 200))
    rect_s = texto_sair.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 100))
    tela.blit(texto_sair, rect_s)

    pygame.display.flip()

    # Aguarda a decisão do jogador
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False


def jogo():
    """Função principal que executa o loop do jogo."""

    # ==================== INICIALIZAÇÃO ====================
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("🚀 Destruidor de Asteroides")
    clock = pygame.time.Clock()

    # Fontes para textos na tela
    fonte_pontuacao = pygame.font.SysFont("consolas", 24)
    fonte_grande = pygame.font.SysFont("consolas", 64, bold=True)
    fonte_media = pygame.font.SysFont("consolas", 28)

    # ==================== ESTADO INICIAL ====================
    nave = Nave()
    projeteis = []       # Lista de projéteis ativos na tela
    asteroides = []      # Lista de asteroides ativos na tela
    pontuacao = 0
    estrelas = gerar_estrelas()

    # Temporizadores (usam pygame.time.get_ticks para controlar intervalos)
    ultimo_asteroide = pygame.time.get_ticks()
    ultimo_tiro = 0

    rodando = True

    # ==================== LOOP PRINCIPAL ====================
    while rodando:

        # ---------- EVENTOS ----------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Captura as teclas pressionadas continuamente
        teclas = pygame.key.get_pressed()

        # Movimento da nave (setas esquerda/direita)
        if teclas[pygame.K_LEFT]:
            nave.mover(-1)
        if teclas[pygame.K_RIGHT]:
            nave.mover(1)

        # Disparo (barra de espaço com cooldown)
        agora = pygame.time.get_ticks()
        if teclas[pygame.K_SPACE] and agora - ultimo_tiro >= COOLDOWN_TIRO:
            # Cria projétil na ponta da nave
            projetil = Projetil(nave.x, nave.y - NAVE_ALTURA // 2)
            projeteis.append(projetil)
            ultimo_tiro = agora

        # ---------- SPAWN DE ASTEROIDES ----------
        if agora - ultimo_asteroide >= INTERVALO_ASTEROIDE:
            asteroides.append(Asteroide())
            ultimo_asteroide = agora

        # ---------- ATUALIZAÇÃO DAS ENTIDADES ----------
        # Atualiza projéteis e remove os que saíram da tela
        for projetil in projeteis:
            projetil.atualizar()
        projeteis = [p for p in projeteis if not p.fora_da_tela()]

        # Atualiza asteroides
        for asteroide in asteroides:
            asteroide.atualizar()

        # ---------- DETECÇÃO DE COLISÕES ----------
        # Colisão projétil ↔ asteroide
        projeteis_restantes = []
        for projetil in projeteis:
            acertou = False
            for asteroide in asteroides:
                if projetil.get_rect().colliderect(asteroide.get_rect()):
                    # Projétil acertou um asteroide: remove ambos e pontua
                    asteroides.remove(asteroide)
                    pontuacao += 10
                    acertou = True
                    break
            if not acertou:
                projeteis_restantes.append(projetil)
        projeteis = projeteis_restantes

        # Colisão asteroide ↔ nave OU asteroide passou do fundo
        game_over = False
        for asteroide in asteroides:
            if asteroide.get_rect().colliderect(nave.get_rect()):
                game_over = True
                break
            if asteroide.passou_da_tela():
                game_over = True
                break

        if game_over:
            # Exibe tela de game over e decide se reinicia ou encerra
            reiniciar = tela_game_over(tela, fonte_grande, fonte_media, pontuacao)
            if reiniciar:
                # Reinicia todas as variáveis do jogo
                nave = Nave()
                projeteis = []
                asteroides = []
                pontuacao = 0
                estrelas = gerar_estrelas()
                ultimo_asteroide = pygame.time.get_ticks()
                ultimo_tiro = 0
                continue
            else:
                rodando = False
                continue

        # ---------- RENDERIZAÇÃO ----------
        # Preenche o fundo com cor do espaço
        tela.fill(COR_FUNDO)

        # Desenha as estrelas
        desenhar_estrelas(tela, estrelas)

        # Desenha a nave
        nave.desenhar(tela)

        # Desenha todos os projéteis
        for projetil in projeteis:
            projetil.desenhar(tela)

        # Desenha todos os asteroides
        for asteroide in asteroides:
            asteroide.desenhar(tela)

        # Desenha a pontuação
        desenhar_pontuacao(tela, fonte_pontuacao, pontuacao)

        # Atualiza a tela
        pygame.display.flip()

        # Controla o framerate
        clock.tick(FPS)

    # ==================== ENCERRAMENTO ====================
    pygame.quit()
    sys.exit()


# Executa o jogo quando o script é rodado diretamente
if __name__ == "__main__":
    jogo()
