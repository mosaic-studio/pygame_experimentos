__author__ = "Marlon"

import os
import random
import time

import pygame
from pygame.locals import SRCALPHA

import pyganim

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640

METEORS_BROWN = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_big4.png",
                 "meteorBrown_med1.png", "meteorBrown_med3.png"]

LASERS = ["laserBlue01.png", "laserBlue02.png", "laserBlue03.png", "laserBlue04.png", "laserBlue05.png",
          "laserBlue06.png", "laserBlue07.png", "laserBlue08.png", "laserBlue09.png", "laserBlue10.png", ]


def load_image(name, colorkey=None, alpha=False):
    """loads an image into memory"""
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, SRCALPHA)
    return image, image.get_rect()


class Meteoros(pygame.sprite.Sprite):
    def __init__(self, meteor="meteorBrown_big1.png", alpha=True):
        super().__init__()
        self.image, self.rect = load_image(os.path.join('PNG', 'Meteors', meteor), alpha=alpha)
        self.mask = pygame.mask.from_surface(self.image, 0)

    def update(self):
        """ Called each frame. """

        # Move block down one pixel
        self.rect.y += 1

        # If block is too far down, reset to top of screen.
        if self.rect.y > SCREEN_HEIGHT:
            self.reset_pos()

    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-400, -70)
        x = random.randrange(0, SCREEN_WIDTH)
        if x + self.image.get_size()[0] > SCREEN_WIDTH:
            self.rect.x = x - self.image.get_size()[0]
        elif x - self.image.get_size()[0] < SCREEN_WIDTH:
            self.rect.x = x + self.image.get_size()[0]
        else:
            self.rect.x = x


class Nave(pygame.sprite.Sprite):
    last_shot = 0
    shot_delay = 0.1
    projectile_image = None

    def __init__(self, alpha=True, projectile_list=pygame.sprite.Group()):
        super().__init__()
        self.image, self.rect = load_image(os.path.join('PNG', 'playerShip1_blue.png'), alpha=alpha)
        self.rect.x = SCREEN_WIDTH / 2 - self.image.get_size()[1]
        self.rect.y = SCREEN_HEIGHT - self.image.get_size()[0]
        self.mask = pygame.mask.from_surface(self.image, 0)
        self.projectile_list = projectile_list

    def update(self):
        key = pygame.key.get_pressed()
        dist = 10  # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]:  # down key
            if self.rect.y < SCREEN_HEIGHT - self.image.get_size()[1]:
                self.rect.y += dist  # move down
        elif key[pygame.K_UP]:  # up key
            if self.rect.y > 0:
                self.rect.y -= dist  # move up
        if key[pygame.K_RIGHT]:  # right key
            if self.rect.x < SCREEN_WIDTH - self.image.get_size()[0]:
                self.rect.x += dist  # move right
                # self.speed_x = dist
        elif key[pygame.K_LEFT]:  # left key
            if self.rect.x > 0:
                self.rect.x -= dist  # move left
                # self.speed_x = dist

        if key[pygame.K_SPACE]:
            if time.time() - self.last_shot > self.shot_delay:
                projectile = Projectile(self.rect.center)
                self.projectile_list.add(projectile)
                self.last_shot = time.time()


class Missile(pygame.sprite.Sprite):
    speed_x = 0
    speed_y = -10

    def __init__(self, pos, img="laserBlue01.png", alpha=True):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(os.path.join('PNG', 'Lasers', img), alpha=alpha)
        self.rect.center = pos

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y < -5:
            self.kill()


class Projectile(Missile):
    def __init__(self, pos, img="laserBlue01.png", alpha=True):
        Missile.__init__(self, pos, img, alpha)
        self.mask = pygame.mask.from_surface(self.image)


class Background:
    def __init__(self):
        self.image, self.rect = load_image(os.path.join("PNG", "Backgrounds", "black_m.png"))
        self.background_size = self.image.get_size()


class Game:
    x = 0
    y = 0
    x1 = 0
    score = 0

    def __init__(self):
        self.background = Background()
        self.w, self.h = self.background.background_size
        self.y1 = -self.h
        self.meteor_list = pygame.sprite.Group()

        self.all_sprites_list = pygame.sprite.Group()

        self.projectile_list = pygame.sprite.Group()
        for i in range(10):
            # This represents a block
            name = random.choice(METEORS_BROWN)
            meteor = Meteoros(name)

            # Set a random location for the block
            x = random.randrange(SCREEN_WIDTH)
            if x + meteor.image.get_size()[0] > SCREEN_WIDTH:
                meteor.rect.x = x - meteor.image.get_size()[0]
            elif x - meteor.image.get_size()[0] < SCREEN_WIDTH:
                meteor.rect.x = x + meteor.image.get_size()[0]
            else:
                meteor.rect.x = x
            meteor.rect.y = -50

            # Add the block to the list of objects
            self.meteor_list.add(meteor)
            self.all_sprites_list.add(meteor)
            shoot_animation = pyganim.PygAnimation([(os.path.join('PNG', 'Lasers', 'laserBlue09.png'), 0.5),
                                                    (os.path.join('PNG', 'Lasers', 'laserBlue08.png'), 0.5)])

            self.explosion_shoot = shoot_animation.getCopy()
            self.explosion_shoot.rate = 0.5

        self.player = Nave(projectile_list=self.projectile_list)
        self.all_sprites_list.add(self.player)

    def run_game(self, screen):
        self.y1 += 5
        self.y += 5
        screen.blit(self.background.image, (self.x, self.y))
        screen.blit(self.background.image, (self.x1, self.y1))
        if self.y > self.h:
            self.y = -self.h
        if self.y1 > self.h:
            self.y1 = -self.h

        self.all_sprites_list.update()
        self.projectile_list.update()

        for projectile in self.projectile_list:
            if projectile.rect.x < 0 or projectile.rect.x > SCREEN_WIDTH:
                self.projectile_list.remove(projectile)
            elif projectile.rect.y < - 20 or projectile.rect.y > SCREEN_HEIGHT:
                self.projectile_list.remove(projectile)

        meteors_hit_list = pygame.sprite.spritecollide(self.player, self.meteor_list, False, pygame.sprite.collide_mask)
        shoot_laser_list = pygame.sprite.groupcollide(self.projectile_list, self.meteor_list, False, False,
                                                      pygame.sprite.collide_mask)

        for proj, meteor in shoot_laser_list.items():
            self.projectile_list.remove(proj)
            self.explosion_shoot.play()
            self.explosion_shoot.blit(screen, (proj.rect.x, proj.rect.y))
            proj.kill()
            for m in meteor:
                m.reset_pos()

            self.score += 1
            print(self.score)

        for block in meteors_hit_list:
            block.reset_pos()

        self.all_sprites_list.draw(screen)
        self.projectile_list.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("SPACE SHOOTER")

    done = False

    clock = pygame.time.Clock()
    game = Game()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        game.run_game(screen)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(40)

    pygame.quit()


if __name__ == '__main__':
    main()
