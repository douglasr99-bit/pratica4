# config.py — Constantes e configurações globais do jogo

# Dimensões da janela do jogo (em pixels)
LARGURA_TELA = 800
ALTURA_TELA = 600

# Frames por segundo — controla a velocidade do loop principal
FPS = 60

# ===================== CORES (RGB) =====================
# Fundo escuro simulando o espaço
COR_FUNDO = (10, 10, 30)

# Cor da nave do jogador (verde neon)
COR_NAVE = (0, 255, 100)

# Cor dos projéteis disparados (amarelo brilhante)
COR_PROJETIL = (255, 255, 0)

# Cor dos asteroides (vermelho escuro / marrom)
COR_ASTEROIDE = (180, 80, 80)

# Cor do texto de pontuação e mensagens
COR_TEXTO = (255, 255, 255)

# Cor das estrelas no fundo
COR_ESTRELA = (200, 200, 255)

# ===================== VELOCIDADES =====================
# Velocidade de movimento lateral da nave (pixels por frame)
VELOCIDADE_NAVE = 10

# Velocidade dos projéteis subindo (pixels por frame)
VELOCIDADE_PROJETIL = 8

# Velocidade dos asteroides descendo (pixels por frame)
VELOCIDADE_ASTEROIDE = 3

# ===================== TEMPORIZADORES =====================
# Intervalo entre o spawn de novos asteroides (milissegundos)
INTERVALO_ASTEROIDE = 1200

# Tempo mínimo entre tiros consecutivos (milissegundos)
COOLDOWN_TIRO = 300

# ===================== DIMENSÕES DAS ENTIDADES =====================
# Nave: largura e altura em pixels
NAVE_LARGURA = 40
NAVE_ALTURA = 50

# Projétil: raio em pixels
PROJETIL_RAIO = 4

# Asteroide: faixa de tamanho (raio mínimo e máximo)
ASTEROIDE_TAMANHO_MIN = 15
ASTEROIDE_TAMANHO_MAX = 35

# Número de estrelas no fundo
NUM_ESTRELAS = 100
