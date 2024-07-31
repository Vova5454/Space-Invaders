import pygame as pg
from settings import *
import sprites
import os
import random
import pygame.freetype as pgft


def draw_game():
    """Отрисовка объектов на экране во время игрового процесса."""
    screen.blit(bg_image, (0, 0))
    player.draw(screen)
    meteor_group.draw(screen)
    laser_group.draw(screen)
    screen.blit(playerlife, (20, 20))
    screen.blit(numeral_x, (60, 28))
    font.render_to(screen, (WIDTH-100, 23), str(player.score).zfill(3), WHITE)
    font.render_to(screen, (85, 23), str(player.hp), WHITE)
    buff_group.draw(screen)

def draw_menu():
    """Отрисовка меню перезапуска игры."""
    screen.fill(PURPLE)
    menu_font.render_to(screen, (WIDTH//2-211, 70), 'GAME OVER',  RED)
    button.draw(screen)
    screen.blit(playerlife, (20, 20))
    screen.blit(numeral_x, (60, 28))
    font.render_to(screen, (WIDTH-100, 23), str(player.score).zfill(3), WHITE)
    font.render_to(screen, (85, 23), str(player.hp), WHITE)

def stop_game():
    """Завершение игры."""
    pg.mouse.set_visible(True)
    space_ambiance.fadeout(5000)
    meteor_group.empty()
    laser_group.empty()

def restart_game():
    """Перезапуск игры."""
    pg.mouse.set_visible(False)
    sfx_twoTone.play()
    space_ambiance.play(-1)
    player.reset()

def check_player_collision():
    """Проверка столкновения игрока с метеоритом."""
    if pg.sprite.spritecollide(player, meteor_group, True):
        hit.play()
        player.damage(1)

def check_laser_collision():
    """Проверка столкновения ласера с метеором"""
    for laser in laser_group:
        if pg.sprite.spritecollide(laser, meteor_group, True):
            meteor_hit.play()
            laser.kill()
            player.score += 1
            if player.bolt_exists:
                player.bolt_score += 1
                if player.bolt_score > 25:
                    player.bolt_exists = False
                    player.bolt_score = 0
        
def update(buff_start_tick_exists):
    """Обновление спрайтов."""
    meteor_group.update()
    player.update()
    laser_group.update(player)
    check_player_collision()
    check_laser_collision()
    buff_group.update()
    check_buff_collision(buff_start_tick_exists)

def create_meteor():
    """Создание метеора."""
    meteor_image = random.choice(meteors_images)
    meteor = sprites.Meteorite((random.randint(0, WIDTH), -20), meteor_image)
    meteor_group.add(meteor)

def create_laser():
    "Создание ласера."
    sfx_laser.play()
    laser_group.add(sprites.Laser(player.rect.center, laser_images))
    sfx_laser.play()

def hide_cursor():
    """Спрятать курсор."""
    pg.mouse.set_visible(False)

def create_buff():
    """Создание баффа."""
    pos = (random.randint(0, WIDTH), -20)
    buff_type = random.choice(list(buff_images.keys()))
    buff = sprites.Buff(buff_images[buff_type], buff_type, pos)
    buff_group.add(buff)

def check_buff_collision(buff_start_tick_exists):
    """Проверка столкновения игрока с баффом."""
    buff = pg.sprite.spritecollideany(player, buff_group)
    if buff == None:
        return
    if buff.type_ == 'shield':
        player.apply_shield()
        buff.kill()
    if buff.type_ == 'laser_speed_boost':
        buff.kill()
        player.bolt_exists = True
    if buff.type_ == 'medkit':
        player.hp += 1
        buff.kill()

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Space-Invaders')

meteors_images = [pg.image.load('res/PNG/Meteors/' + name) for name in os.listdir('res/PNG/Meteors')] 
damage_images = [pg.image.load(f'res/PNG/Damage/playerShip1_damage{name}.png') for name in range(1, 4)]
bg_image = pg.image.load('res/Backgrounds/darkPurple.png')
bg_image = pg.transform.scale(bg_image, (WIDTH, HEIGHT))
numeral_x = pg.image.load('res/PNG/UI/numeralX.png')
playerlife = pg.image.load('res/PNG/UI/playerLife1_orange.png')
laser_images = [pg.image.load(f'res/PNG/Lasers/laserBlue{i}.png') for i in range(12, 17)]
damage_images.insert(0, pg.image.load('res/PNG/playerShip1_orange.png'))
throster_images = [pg.image.load(f'res/PNG/Effects/fire{name}.png') for name in range(11, 18)]
medkit_image = pg.image.load('res/PNG/Power-ups/medkit.png')
medkit_image = pg.transform.scale(medkit_image, (75, 45))
buff_images = {'shield': pg.image.load('res/PNG/Power-ups/shield_silver.png'), 'laser_speed_boost' : pg.image.load('res/PNG/Power-ups/bolt_silver.png'), 'medkit' : medkit_image}
shield_images = [pg.image.load(f'res/PNG/Effects/shield{name}.png') for name in range(1, 4)]
hit = pg.mixer.Sound('res/Bonus/hit.wav')
meteor_hit = pg.mixer.Sound('res/Bonus/meteor_hit.wav')
sfx_lose = pg.mixer.Sound('res/Bonus/sfx_lose.ogg')
sfx_laser = pg.mixer.Sound('res/Bonus/sfx_laser1.ogg')
sfx_twoTone = pg.mixer.Sound('res/Bonus/sfx_twoTone.ogg')
space_ambiance = pg.mixer.Sound('res/Bonus/space_ambiance.wav')
speed_y = -15
buff_start_tick_exists = False
timer = 0
laser_boost_activated = False

button_font = pgft.Font('res/Bonus/kenvector_future.ttf', 42)
font = pgft.Font('res/Bonus/kenvector_future.ttf', 40)
menu_font = pgft.Font('res/Bonus/kenvector_future.ttf', 60)

player = sprites.Player((WIDTH//2, HEIGHT-50), damage_images, throster_images, shield_images)
meteor_group = pg.sprite.Group()
laser_group = pg.sprite.GroupSingle()
button = sprites.Button((WIDTH//2, HEIGHT//2), 'Restart', button_font)
buff_group = pg.sprite.Group()
 
SPAWN_METEOR = pg.USEREVENT
pg.time.set_timer(SPAWN_METEOR, 400)
SPAWN_BUFF = pg.USEREVENT + 2
pg.time.set_timer(SPAWN_BUFF, 5000) 

space_ambiance.play(-1)

status = 'Game'
hide_cursor()
run = True
while run:
    pg.display.set_caption(f'Space-Invaders FPS:{round(clock.get_fps(), 1)}')
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False
        if status == 'Game':
            if event.type == SPAWN_METEOR:
                create_meteor()
            if event.type == pg.MOUSEBUTTONDOWN:
                if len(laser_group) == 0:
                    create_laser()
            if event.type == SPAWN_BUFF:
                create_buff()
            if event.type == player.DESTROY:
                status = 'Menu'
                stop_game()
        else:
            if button.rect.collidepoint(pg.mouse.get_pos()) and event.type == pg.MOUSEBUTTONDOWN:
                status = 'Game'
                restart_game()
    if status == 'Game':
        draw_game()
        update(buff_start_tick_exists)
    else:
        draw_menu()

    clock.tick(60)
    pg.display.flip()