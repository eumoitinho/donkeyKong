# main.py
from game.main import main  # Importa a função principal do jogo
import pygame
from utils.constants import *  # Importa todas as constantes definidas no módulo constants
from menu import main_menu  # Importa a função do menu principal
from database import initialize_db  # Importa a função para inicializar o banco de dados

# Configurações iniciais da janela do jogo
pygame.display.set_caption('Classic Donkey Kong Rebuild!')  # Define o título da janela
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])  # Define o tamanho da janela do jogo

# Bloco principal
if __name__ == "__main__":
    pygame.init()  # Inicializa o Pygame aqui
    initialize_db()  # Inicializa o banco de dados aqui
    action, username = main_menu(screen)
    if action == "start" and username:  # Verifica se a ação é "start" e se há um username válido
        main(screen, username)
