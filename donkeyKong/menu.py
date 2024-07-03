# menu.py
import pygame
import sys
from utils.constants import *
from database import register_user, login_user

def main_menu(screen):
    selected = "start"  # Inicializa a opção selecionada como "start"

    while True:
        # Loop para eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o evento for de sair
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if event.key == pygame.K_UP:  # Se a tecla for para cima
                    selected = "start"
                elif event.key == pygame.K_DOWN:  # Se a tecla for para baixo
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        username = user_auth_menu(screen)  # Chama o menu de login/registro
                        if username:  # Se o login/registro for bem-sucedido
                            return "start", username  # Retorna a ação e o nome de usuário
            if selected == "quit":
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Preenche a tela com a cor preta

        # Renderiza o título do menu
        title = FONT2.render("Donkey Kong", True, (255, 255, 255))
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 150))

        # Renderiza a opção "Start Game" com cor amarela se selecionada, branca se não
        if selected == "start":
            start = FONT2.render("Start Game", True, (255, 255, 0))
        else:
            start = FONT2.render("Start Game", True, (255, 255, 255))
        screen.blit(start, (WINDOW_WIDTH // 2 - start.get_width() // 2, 300))

        # Renderiza a opção "Quit" com cor amarela se selecionada, branca se não
        if selected == "quit":
            quit = FONT2.render("Quit", True, (255, 255, 0))
        else:
            quit = FONT2.render("Quit", True, (255, 255, 255))
        screen.blit(quit, (WINDOW_WIDTH // 2 - quit.get_width() // 2, 400))

        pygame.display.flip()  # Atualiza a tela para mostrar as mudanças

def user_auth_menu(screen):
    font = pygame.font.Font(None, 36)
    username = ""
    password = ""
    mode = "login"  
    active = "username"  
    message = ""  # Mensagem de erro ou sucesso

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    mode = "register" if mode == "login" else "login"
                    username = ""
                    password = ""
                    active = "username"
                    message = ""
                elif active == "username":
                    if event.key == pygame.K_RETURN:
                        active = "password"
                    else:
                        username += event.unicode
                elif active == "password":
                    if event.key == pygame.K_RETURN:
                        if mode == "login":
                            user = login_user(username, password)
                            if user:
                                return user[1]  # Retorna o nome de usuário
                            else:
                                message = "Login failed"
                        elif mode == "register":
                            success = register_user(username, password)
                            if success:
                                message = "Registration successful"
                            else:
                                message = "Registration failed"
                        username = ""
                        password = ""
                        active = "username"
                    else:
                        password += event.unicode

        screen.fill((0, 0, 0))
        mode_text = font.render(f"Mode: {'Login' if mode == 'login' else 'Register'}", True, (255, 255, 255))
        username_text = font.render(f"Username: {username}", True, (255, 255, 255))
        password_text = font.render(f"Password: {'*' * len(password)}", True, (255, 255, 255))
        message_text = font.render(message, True, (255, 0, 0))

        screen.blit(mode_text, (100, 100))
        screen.blit(username_text, (100, 150))
        screen.blit(password_text, (100, 200))
        screen.blit(message_text, (100, 250))

        pygame.display.flip()
