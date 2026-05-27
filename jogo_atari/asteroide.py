# asteroide.py — Classe que representa os asteroides inimigos

# pyrefly: ignore [missing-import]
import pygame
import random
import math
from config import (
    LARGURA_TELA, ALTURA_TELA, COR_ASTEROIDE,
    VELOCIDADE_ASTEROIDE, ASTEROIDE_TAMANHO_MIN, ASTEROIDE_TAMANHO_MAX
)


class Asteroide:
    """
    Asteroide que desce pela tela. Possui forma irregular (polígono aleatório)
    para simular uma rocha espacial no estilo Atari.
    """

    def __init__(self):
        # Tamanho aleatório dentro da faixa configurada
        self.raio = random.randint(ASTEROIDE_TAMANHO_MIN, ASTEROIDE_TAMANHO_MAX)

        # Posição inicial: posição X aleatória no topo, logo acima da tela
        self.x = random.randint(self.raio, LARGURA_TELA - self.raio)
        self.y = -self.raio

        self.velocidade = VELOCIDADE_ASTEROIDE

        # Gera os vértices do polígono irregular (forma de rocha)
        self.vertices = self._gerar_vertices()

    def _gerar_vertices(self):
        """
        Gera vértices aleatórios em torno do centro para criar
        uma forma de rocha irregular. Usa ângulos uniformemente
        distribuídos com variação no raio de cada vértice.
        """
        num_vertices = random.randint(7, 12)
        vertices = []

        for i in range(num_vertices):
            # Distribui os ângulos uniformemente ao redor do círculo
            angulo = (2 * math.pi / num_vertices) * i

            # Variação aleatória no raio (entre 60% e 100% do raio base)
            variacao = random.uniform(0.6, 1.0)
            raio_vertice = self.raio * variacao

            # Calcula coordenadas do vértice relativas ao centro
            vx = raio_vertice * math.cos(angulo)
            vy = raio_vertice * math.sin(angulo)
            vertices.append((vx, vy))

        return vertices

    def atualizar(self):
        """Move o asteroide para baixo a cada frame."""
        self.y += self.velocidade

    def desenhar(self, tela):
        """
        Desenha o asteroide como um polígono irregular.
        Os vértices são transladados para a posição atual do asteroide.
        """
        # Calcula os pontos absolutos (centro + vértices relativos)
        pontos = [(self.x + vx, self.y + vy) for vx, vy in self.vertices]

        # Polígono preenchido (corpo do asteroide)
        pygame.draw.polygon(tela, COR_ASTEROIDE, pontos)

        # Contorno mais claro para dar profundidade
        cor_contorno = (220, 120, 120)
        pygame.draw.polygon(tela, cor_contorno, pontos, 2)

    def passou_da_tela(self):
        """Verifica se o asteroide passou pelo fundo da tela."""
        return self.y - self.raio > ALTURA_TELA

    def get_rect(self):
        """Retorna um pygame.Rect para detecção de colisão."""
        return pygame.Rect(
            self.x - self.raio,
            self.y - self.raio,
            self.raio * 2,
            self.raio * 2
        )
