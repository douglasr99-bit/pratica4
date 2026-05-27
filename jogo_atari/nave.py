# nave.py — Classe que representa a nave do jogador

# pyrefly: ignore [missing-import]
import pygame
from config import (
    LARGURA_TELA, ALTURA_TELA, COR_NAVE,
    VELOCIDADE_NAVE, NAVE_LARGURA, NAVE_ALTURA
)


class Nave:
    """Nave controlada pelo jogador. Move-se horizontalmente e atira projéteis."""

    def __init__(self):
        # Posição inicial: centralizada na parte inferior da tela
        self.largura = NAVE_LARGURA
        self.altura = NAVE_ALTURA
        self.x = LARGURA_TELA // 2
        self.y = ALTURA_TELA - 60
        self.velocidade = VELOCIDADE_NAVE

    def mover(self, direcao):
        """
        Move a nave horizontalmente.
        direcao: -1 para esquerda, +1 para direita.
        Impede que a nave saia dos limites da tela.
        """
        self.x += direcao * self.velocidade

        # Limitar dentro da tela (metade da largura de margem)
        if self.x - self.largura // 2 < 0:
            self.x = self.largura // 2
        if self.x + self.largura // 2 > LARGURA_TELA:
            self.x = LARGURA_TELA - self.largura // 2

    def desenhar(self, tela):
        """
        Desenha a nave como um triângulo (estilo Atari).
        O vértice superior é a ponta, e a base fica na parte inferior.
        """
        # Calcula os 3 vértices do triângulo
        ponta = (self.x, self.y - self.altura // 2)
        esquerda = (self.x - self.largura // 2, self.y + self.altura // 2)
        direita = (self.x + self.largura // 2, self.y + self.altura // 2)

        # Desenha o triângulo preenchido
        pygame.draw.polygon(tela, COR_NAVE, [ponta, esquerda, direita])

        # Brilho na ponta da nave (efeito visual)
        pygame.draw.circle(tela, (150, 255, 200), ponta, 3)

    def get_rect(self):
        """Retorna um pygame.Rect para detecção de colisão."""
        return pygame.Rect(
            self.x - self.largura // 2,
            self.y - self.altura // 2,
            self.largura,
            self.altura
        )
