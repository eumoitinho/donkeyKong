# Importa as bibliotecas necessárias
import pygame
import random
from utils.constants import *  # Importa todas as constantes definidas
from game.player import Player  # Importa a classe Player do módulo player
from game.barrel import Barrel  # Importa a classe Barrel do módulo barrel
from game.flame import Flame  # Importa a classe Flame do módulo flame
from game.hammer import Hammer  # Importa a classe Hammer do módulo hammer
from map.level import Level  # Importa a classe Level do módulo level
# main.py
from database import initialize_db, register_user, login_user, update_score, get_score

initialize_db()


# Configura o título da janela do jogo
pygame.display.set_caption('Classic Donkey Kong Rebuild!')
# Define o tamanho da tela do jogo
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])

# Define os níveis do jogo
levels = [{'bridges': [(1, START_Y, 15), (16, START_Y - SLOPE, 3), (19, START_Y - 2 * SLOPE, 3), (22, START_Y - 3 * SLOPE, 3),
                       (25, START_Y - 4 * SLOPE, 3), (28, START_Y - 5 * SLOPE, 3), (25, ROW2_Y, 3), (22, ROW2_Y - SLOPE, 3),
                       (19, ROW2_Y - 2 * SLOPE, 3), (16, ROW2_Y - 3 * SLOPE, 3), (13, ROW2_Y - 4 * SLOPE, 3),
                       (10, ROW2_Y - 5 * SLOPE, 3), (7, ROW2_Y - 6 * SLOPE, 3), (4, ROW2_Y - 7 * SLOPE, 3),
                       (2, ROW2_Y - 8 * SLOPE, 2), (4, ROW3_Y, 3), (7, ROW3_Y - SLOPE, 3), (10, ROW3_Y - 2 * SLOPE, 3),
                       (13, ROW3_Y - 3 * SLOPE, 3), (16, ROW3_Y - 4 * SLOPE, 3), (19, ROW3_Y - 5 * SLOPE, 3),
                       (22, ROW3_Y - 6 * SLOPE, 3), (25, ROW3_Y - 7 * SLOPE, 3), (28, ROW3_Y - 8 * SLOPE, 2),
                       (25, ROW4_Y, 3), (22, ROW4_Y - SLOPE, 3), (19, ROW4_Y - 2 * SLOPE, 3), (16, ROW4_Y - 3 * SLOPE, 3),
                       (13, ROW4_Y - 4 * SLOPE, 3), (10, ROW4_Y - 5 * SLOPE, 3), (7, ROW4_Y - 6 * SLOPE, 3),
                       (4, ROW4_Y - 7 * SLOPE, 3), (2, ROW4_Y - 8 * SLOPE, 2), (4, ROW5_Y, 3), (7, ROW5_Y - SLOPE, 3),
                       (10, ROW5_Y - 2 * SLOPE, 3), (13, ROW5_Y - 3 * SLOPE, 3), (16, ROW5_Y - 4 * SLOPE, 3),
                       (19, ROW5_Y - 5 * SLOPE, 3), (22, ROW5_Y - 6 * SLOPE, 3), (25, ROW5_Y - 7 * SLOPE, 3),
                       (28, ROW5_Y - 8 * SLOPE, 2), (25, ROW6_Y, 3), (22, ROW6_Y - SLOPE, 3), (19, ROW6_Y - 2 * SLOPE, 3),
                       (16, ROW6_Y - 3 * SLOPE, 3), (2, ROW6_Y - 4 * SLOPE, 14), (13, ROW6_Y - 4 * SECTION_HEIGHT, 6),
                       (10, ROW6_Y - 3 * SECTION_HEIGHT, 3)],
           'ladders': [(12, ROW2_Y + 6 * SLOPE, 2), (12, ROW2_Y + 26 * SLOPE, 2), (25, ROW2_Y + 11 * SLOPE, 4),
                       (6, ROW3_Y + 11 * SLOPE, 3), (14, ROW3_Y + 8 * SLOPE, 4), (10, ROW4_Y + 6 * SLOPE, 1),
                       (10, ROW4_Y + 24 * SLOPE, 2), (16, ROW4_Y + 6 * SLOPE, 5), (25, ROW4_Y + 9 * SLOPE, 4),
                       (6, ROW5_Y + 11 * SLOPE, 3), (11, ROW5_Y + 8 * SLOPE, 4), (23, ROW5_Y + 4 * SLOPE, 1),
                       (23, ROW5_Y + 24 * SLOPE, 2), (25, ROW6_Y + 9 * SLOPE, 4), (13, ROW6_Y + 5 * SLOPE, 2),
                       (13, ROW6_Y + 25 * SLOPE, 2), (18, ROW6_Y - 27 * SLOPE, 4), (12, ROW6_Y - 17 * SLOPE, 2),
                       (10, ROW6_Y - 17 * SLOPE, 2), (12, -5, 13), (10, -5, 13)],
          'hammers': [(4, ROW6_TOP + SECTION_HEIGHT), (4, ROW4_TOP + SECTION_HEIGHT)],
           'target': (13, ROW6_Y - 4 * SECTION_HEIGHT, 3)}]

# Inicializa variáveis do jogo
barrel_spawn_time = BARREL_SPAWN_TIME
barrel_count = barrel_spawn_time / 2
barrel_time = 360
fireball_trigger = False
first_fireball_trigger = False
counter = 0
score = 0
high_score = 0
lives = 5
bonus = 6000
victory = False
reset_game = False
active_level = 0

# Desenha a tela do nível
def draw_screen(level_data, screen):
    level = Level(level_data)  # Cria um objeto Level com os dados do nível
    plats, lads = level.create_level(screen)  # Cria as plataformas e escadas no nível
    return plats, lads

# Desenha os elementos extras na tela (pontuação, vidas, etc.)
def draw_extras(screen):
    global counter
    screen.blit(FONT2.render(f'I { score}', True, 'white'), (3*SECTION_WIDTH, 2*SECTION_HEIGHT))
    screen.blit(FONT2.render(f'TOP {high_score}', True, 'white'), (14 * SECTION_WIDTH, 2 * SECTION_HEIGHT))
    screen.blit(FONT2.render(f'  M    BONUS     L ', True, 'white'), (20 * SECTION_WIDTH + 5, 4 * SECTION_HEIGHT))
    screen.blit(FONT2.render(f'  {lives}       {bonus}        {active_level + 1}  ', True, 'white'), (20 * SECTION_WIDTH + 5, 5 * SECTION_HEIGHT))
    
    if barrel_count < barrel_spawn_time / 2:
        screen.blit(PEACH1, (10 * SECTION_WIDTH, ROW6_Y - 6 * SECTION_HEIGHT))
    else:
        screen.blit(PEACH2, (10 * SECTION_WIDTH, ROW6_Y - 6 * SECTION_HEIGHT))
    oil = draw_oil(screen)
    draw_barrels(screen)
    draw_kong(screen)
    return oil

# Desenha o barril de óleo na tela
def draw_oil(screen):
    x_coord, y_coord = 4 * SECTION_WIDTH, WINDOW_HEIGHT - 4.5 * SECTION_HEIGHT
    oil = pygame.draw.rect(screen, 'blue', [x_coord, y_coord, 2 * SECTION_WIDTH, 2.5 * SECTION_HEIGHT])
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 * SECTION_WIDTH, y_coord, 2.2 * SECTION_WIDTH, .2 * SECTION_HEIGHT])
    pygame.draw.rect(screen, 'blue', [x_coord - 0.1 * SECTION_WIDTH, y_coord + 2.3 * SECTION_HEIGHT, 2.2 * SECTION_WIDTH, .2 * SECTION_HEIGHT])
    pygame.draw.rect(screen, 'light blue', [x_coord + 0.1 * SECTION_WIDTH, y_coord + .2 * SECTION_HEIGHT, .2 * SECTION_WIDTH, 2 * SECTION_HEIGHT])
    pygame.draw.rect(screen, 'light blue', [x_coord, y_coord + 0.5 * SECTION_HEIGHT, 2 * SECTION_WIDTH, .2 * SECTION_HEIGHT])
    pygame.draw.rect(screen, 'light blue', [x_coord, y_coord + 1.7 * SECTION_HEIGHT, 2 * SECTION_WIDTH, .2 * SECTION_HEIGHT])
    screen.blit(FONT2.render('OIL', True, 'light blue'), (x_coord + .4 * SECTION_WIDTH, y_coord + 0.7 * SECTION_HEIGHT))
    for i in range(4):
        pygame.draw.circle(screen, 'red', (x_coord + 0.5 * SECTION_WIDTH + i * 0.4 * SECTION_WIDTH, y_coord + 2.1 * SECTION_HEIGHT), 3)
    if counter < 15 or 30 < counter < 45:
        screen.blit(FLAMES_IMG, (x_coord, y_coord - SECTION_HEIGHT))
    else:
        screen.blit(pygame.transform.flip(FLAMES_IMG, True, False), (x_coord, y_coord - SECTION_HEIGHT))
    return oil

# Desenha os barris na tela
def draw_barrels(screen):
    screen.blit(pygame.transform.rotate(BARREL_SIDE, 90), (SECTION_WIDTH * 1.2, 5.4 * SECTION_HEIGHT))
    screen.blit(pygame.transform.rotate(BARREL_SIDE, 90), (SECTION_WIDTH * 2.5, 5.4 * SECTION_HEIGHT))
    screen.blit(pygame.transform.rotate(BARREL_SIDE, 90), (SECTION_WIDTH * 2.5, 7.7 * SECTION_HEIGHT))
    screen.blit(pygame.transform.rotate(BARREL_SIDE, 90), (SECTION_WIDTH * 1.2, 7.7 * SECTION_HEIGHT))

# Desenha o Donkey Kong na tela
def draw_kong(screen):
    global barrel_count, barrel_time
    phase_time = barrel_time // 4
    if barrel_spawn_time - barrel_count > 3 * phase_time:
        dk_img = DK2
    elif barrel_spawn_time - barrel_count > 2 * phase_time:
        dk_img = DK1
    elif barrel_spawn_time - barrel_count > phase_time:
        dk_img = DK3
    else:
        dk_img = pygame.transform.flip(DK1, True, False)
        screen.blit(BARREL_IMG, (250, 250))
    screen.blit(dk_img, (3.5 * SECTION_WIDTH, ROW6_Y - 5.5 * SECTION_HEIGHT))

# Verifica se o jogador pode subir ou descer uma escada
def check_climb(player, lads):
    can_climb = False
    climb_down = False
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * SECTION_HEIGHT), (player.rect[2], player.rect[3]))
    for lad in lads:
        if player.hitbox.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    if (not can_climb and (not climb_down or player.y_change < 0)) or \
            (player.landed and can_climb and player.y_change > 0 and not climb_down):
        player.climbing = False
    return can_climb, climb_down

# Verifica colisões entre o jogador e os barris
def barrel_collide(player, barrels, reset):
    global score
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * SECTION_HEIGHT), (player.rect[2], player.rect[3]))
    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True
        elif not player.landed and not player.over_barrel and under.colliderect(brl):
            player.over_barrel = True
            score += 100
    if player.landed:
        player.over_barrel = False

    return reset

# Reseta o jogo após o jogador perder uma vida
def reset(player, barrels, flames, hammers, hammers_list):
    global first_fireball_trigger, victory, lives, bonus, barrel_spawn_time, barrel_count
    pygame.time.delay(1000)
    for bar in barrels:
        bar.kill()
    for flam in flames:
        flam.kill()
    for hams in hammers:
        hams.kill()
    for hams in hammers_list:
        hammers.add(Hammer(*hams))
    lives -= 1
    bonus = 6000
    player.kill()
    player = Player(250, WINDOW_HEIGHT - 130)
    first_fireball_trigger = False
    barrel_spawn_time = 360
    barrel_count = barrel_spawn_time / 2
    victory = False
    return player

# Verifica se o jogador alcançou o objetivo
def check_victory(player, level_data):
    target = level_data['target']
    target_rect = pygame.rect.Rect((target[0] * SECTION_WIDTH, target[1]), (SECTION_WIDTH * target[2], 1))
    return player.bottom.colliderect(target_rect)

# Função principal do jogo
def main(screen, username):
    # Declaração de variáveis globais
    global barrel_spawn_time, barrel_count, fireball_trigger, first_fireball_trigger, counter, score, high_score, lives, bonus, victory, reset_game, active_level

    # No início da função principal do jogo
    score = get_score(username)


    # Grupos de sprites para barris, chamas e martelos
    barrels = pygame.sprite.Group()
    flames = pygame.sprite.Group()
    hammers = pygame.sprite.Group()
    hammers_list = levels[active_level]['hammers']
    for ham in hammers_list:
        hammers.add(Hammer(*ham))
    # Criação do jogador na posição inicial
    player = Player(250, WINDOW_HEIGHT - 130)

    run = True
    while run:
        # Preenche a tela com a cor preta
        screen.fill('black')
        pygame.time.Clock().tick(FPS)
        
        # Atualiza o contador e o bônus
        if counter < 60:
            counter += 1
        else:
            counter = 0
            if bonus > 0:
                bonus -= 100

        # Desenha o nível e elementos extras na tela
        plats, lads = draw_screen(levels[active_level], screen)
        oil_drum = draw_extras(screen)
        climb, down = check_climb(player, lads)
        victory = check_victory(player, levels[active_level])
        
        # Lógica de spawn dos barris
        if barrel_count < barrel_spawn_time:
            barrel_count += 1
        else:
            barrel_count = random.randint(0, 120)
            barrel_time = barrel_spawn_time - barrel_count
            barrel = Barrel(270, 270)
            barrels.add(barrel)
            if not first_fireball_trigger:
                flame = Flame(5 * SECTION_WIDTH, WINDOW_HEIGHT - 4 * SECTION_HEIGHT)
                flames.add(flame)
                first_fireball_trigger = True
        
        # Atualiza e desenha os barris
        for barrel in barrels:
            barrel.draw(screen)
            barrel.check_fall(lads)
            fireball_trigger = barrel.update(fireball_trigger, plats, oil_drum)
            if barrel.rect.colliderect(player.hammer_box) and player.hammer:
                barrel.kill()
                score += 500

        # Lógica de spawn das chamas
        if fireball_trigger:
            flame = Flame(5 * SECTION_WIDTH, WINDOW_HEIGHT - 4 * SECTION_HEIGHT)
            flames.add(flame)
            fireball_trigger = False

        # Atualiza e desenha as chamas
        for flame in flames:
            flame.check_climb(lads)
            if flame.rect.colliderect(player.hitbox):
                reset_game = True
        flames.draw(screen)
        flames.update(plats)
        
        # Atualiza e desenha o jogador
        player.update(plats)
        player.draw(screen)
        
        # Desenha os martelos e verifica a colisão com o jogador
        for ham in hammers:
            ham.draw(screen, player)

        # Verifica colisões com barris e reseta o jogo se necessário
        reset_game = barrel_collide(player, barrels, reset_game)
        if reset_game:
            if lives > 0:
                player = reset(player, barrels, flames, hammers, hammers_list)
                reset_game = False
            else:
                run = False

        # Gerencia eventos de entrada do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not player.climbing:
                    player.x_change = 1
                    player.dir = 1
                if event.key == pygame.K_LEFT and not player.climbing:
                    player.x_change = -1
                    player.dir = -1
                if event.key == pygame.K_SPACE and player.landed:
                    player.landed = False
                    player.y_change = -6
                if event.key == pygame.K_UP:
                    if climb:
                        player.y_change = -2
                        player.x_change = 0
                        player.climbing = True
                if event.key == pygame.K_DOWN:
                    if down:
                        player.y_change = 2
                        player.x_change = 0
                        player.climbing = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_LEFT:
                    player.x_change = 0
                if event.key == pygame.K_UP:
                    if climb:
                        player.y_change = 0
                    if player.climbing and player.landed:
                        player.climbing = False
                if event.key == pygame.K_DOWN:
                    if climb:
                        player.y_change = 0
                    if player.climbing and player.landed:
                        player.climbing = False
        
        # Verifica se o jogador venceu o nível
        if victory:
            screen.blit(FONT.render('VICTORY!', True, 'white'), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            reset_game = True
            lives += 1
            score += bonus
            if score > high_score:
                high_score = score
            score = 0
            player.climbing = False

        # Atualiza a tela
        pygame.display.flip()

        # No final da função principal do jogo, onde a pontuação é registrada
        update_score(username, score)

    
    # Encerra o jogo
    pygame.quit()
