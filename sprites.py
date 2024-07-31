import pygame as pg
from settings import *
import random

class Player():
    """Класс для анимации и движения игрока."""
    def __init__(self, pos, images, throster_images, shield_images):
        """Инициализировать атрибуты игрока."""
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hp = 4
        self.score = 0
        self.start_pos = pos
        self.DESTROY = pg.USEREVENT+1
        self.throster_images = throster_images
        self.frame = 0
        self.animation_len = len(throster_images)
        self.shield_images = shield_images
        self.shield_strength = 0
        self.shield_rect = self.shield_images[0].get_rect()
        self.bolt_score = 0
        self.bolt_exists = False
    
    def draw(self, target_surf):
        """Отрисовка игрока."""
        if self.hp > 0:
            target_surf.blit(self.image, self.rect)
            if self.hp < 4:
                target_surf.blit(self.images[-self.hp], self.rect)
        self.animate(target_surf)
        self.draw_shield(target_surf)

    def animate(self, target_surf):
        """Анимация игрока."""
        self.frame += 0.25
        if int(self.frame) == self.animation_len:
            self.frame = 0 
        image = self.throster_images[int(self.frame)]
        left_throster_pos = (self.rect.centerx-35, self.rect.bottom-18)
        right_throster_pos = (self.rect.centerx+21, self.rect.bottom-18)
        target_surf.blit(image, left_throster_pos)
        target_surf.blit(image, right_throster_pos)


    def move(self):
        """Движение игрока."""
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= 5
        if keys[pg.K_d]:
            self.rect.x += 5
        if keys[pg.K_w]:
            self.rect.y -= 5
        if keys[pg.K_s]:
            self.rect.y += 5
        
    def restrain(self):
        """Не дать игроку улететь за приделы карты."""
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def update(self):
        """Обновление игрока."""
        self.move()
        self.restrain()
        
    def damage(self, damage):
        """Получение урона и post события поражения."""
        if self.shield_strength > 0:
            self.shield_strength -= damage
        else:
            self.hp -= damage
            if self.hp == 0:
                pg.event.post(pg.event.Event(self.DESTROY))

    def reset(self):
        """Востоновление игрока."""
        self.rect.center = self.start_pos
        self.hp = 4
        self.score = 0

    def draw_shield(self, target_surf):
        """Отрисовка щита."""
        if self.shield_strength > 0:
            self.shield_rect.center = self.rect.center
            if self.shield_strength != 1:
                self.shield_rect.move_ip((-5, -5))
            target_surf.blit(self.shield_images[self.shield_strength-1], self.shield_rect)

    def apply_shield(self):
        """Добавить на игрока щит."""
        self.shield_strength = 3


class Meteorite(pg.sprite.Sprite):
    """Класс для движение и обновления метеоритов."""
    def  __init__(self, pos, image):
        """Инициализировать атрибуты метеорита."""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(3, 9)
        self.original_image = image
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)

    def rotate(self):
        """Вращение метеоритов."""
        self.angle += self.rotation_speed
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """Движение и обновление метеоритов."""
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.y > HEIGHT:
            self.kill()
        self.rotate()

class Laser(pg.sprite.Sprite):
    """Класс для создания и обновление лазера."""
    def __init__(self, pos, images):
        """Создание атрибутов лазера."""
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.frame = 0
        self.animation_len = len(self.images)
        self.speed_y = -15

    def update(self, player):
        """Меняет скорость лазера и убивает, если уйдёт за пределы карты."""
        if player.bolt_exists:
            self.speed_y = -100
        else:
            self.speed_y = -15
        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.kill()
        self.animate()
    
    def animate(self):
        """Анимирует лазер."""
        self.frame += 0.25
        if int(self.frame) == self.animation_len:
            self.frame = 0 
        self.image = self.images[int(self.frame)]

class Button():
    """Класс кнопки."""
    def __init__(self, pos, text, font):
        """Сделать атрибуты кнопки."""
        super().__init__()
        self.image = pg.Surface((450, 80))
        self.image.fill((53, 135, 3))
        self.rect = self.image.get_rect(center=pos)
        self.text_surf, self.text_rect = font.render(text, size=42)
        self.text_rect.center = self.rect.center

    def draw(self, target_surf):
        """Отрисовать кнопку."""
        target_surf.blit(self.image, self.rect)
        target_surf.blit(self.text_surf, self.text_rect)

class Buff(pg.sprite.Sprite):
    """Класс баффа."""
    def __init__(self, image, type, pos):
        """Создание атрибутов баффа."""
        super().__init__()
        self.image = image
        self.type_ = type
        self.rect = self.image.get_rect(center=pos)
        self.speed = random.randint(1, 6)

    def update(self):
        """Двигает бафф и убивает, если уйдёт за пределы карты."""
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.kill()