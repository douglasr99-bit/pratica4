# projetil.py — Classe que representa os projéteis disparados pela nave

# pyrefly: ignore [missing-import]
import pygame
from jogo_atari.config import VELOCIDADE_PROJETIL, PROJETIL_RAIO, COR_PROJETIL


class Projetil:
    """Projétil disparado pela nave. Move-se para cima até sair da tela."""

    def __init__(self, x, y):
        # Posição inicial: onde a nave está no momento do disparo
        self.x = x
        self.y = y
        self.raio = PROJETIL_RAIO
        self.velocidade = VELOCIDADE_PROJETIL

    def atualizar(self):
        """Move o projétil para cima a cada frame."""
        self.y -= self.velocidade

    def desenhar(self, tela):
        """
        Desenha o projétil como um círculo brilhante.
        Inclui um efeito de brilho ao redor.
        """
        # Brilho externo (círculo maior e semitransparente)
        superficie_brilho = pygame.Surface((self.raio * 6, self.raio * 6), pygame.SRCALPHA)
        pygame.draw.circle(
            superficie_brilho,
            (255, 255, 100, 80),  # Amarelo com transparência
            (self.raio * 3, self.raio * 3),
            self.raio * 3
        )
        tela.blit(superficie_brilho, (self.x - self.raio * 3, self.y - self.raio * 3))

        # Projétil principal (círculo sólido)
        pygame.draw.circle(tela, COR_PROJETIL, (self.x, self.y), self.raio)

    def fora_da_tela(self):
        """Verifica se o projétil saiu pelo topo da tela."""
        return self.y + self.raio < 0

    def get_rect(self):
        """Retorna um pygame.Rect para detecção de colisão."""
        return pygame.Rect(
            self.x - self.raio,
            self.y - self.raio,
            self.raio * 2,
            self.raio * 2
        )
