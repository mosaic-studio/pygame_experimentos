__author__ = "Marlon"

import os
import pygame
import random

from pygame.locals import RLEACCEL, SRCALPHA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

METEORS_BROWN = ["meteorBrown_big1.png","meteorBrown_big2.png","meteorBrown_big3.png","meteorBrown_big4.png",
            "meteorBrown_med1.png","meteorBrown_med3.png","meteorBrown_small1.png","meteorBrown_small2.png",
            "meteorBrown_tiny1.png","meteorBrown_tiny2.png"]


def load_image(name, colorkey=None, alpha=False):
    """loads an image into memory"""
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if alpha:image = image.convert_alpha()
    else:image=image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, SRCALPHA)
    return image, image.get_rect()


def check_col(obj1, obj2):
    if pygame.sprite.collide_mask(obj1,obj2) is not None:
        return True
    else:
        return False


class Nave(pygame.sprite.Sprite):
    def __init__(self, alpha=True):
        super().__init__()

        self.image, self.rect = load_image(os.path.join('PNG', 'playerShip1_blue.png'), alpha=alpha)

        self.mask = pygame.mask.from_surface(self.image, 0)

    def update(self):
        key = pygame.key.get_pressed()
        dist = 10  # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]:  # down key
            self.rect.y += dist  # move down
        elif key[pygame.K_UP]:  # up key
            self.rect.y -= dist  # move up
        if key[pygame.K_RIGHT]:  # right key
            self.rect.x += dist  # move right
        elif key[pygame.K_LEFT]:  # left key
            self.rect.x -= dist  # move left


class Meteoros(pygame.sprite.Sprite):
    def __init__(self, meteor, alpha=True):
        super().__init__()
        self.image, self.rect = load_image(os.path.join('PNG', 'Meteors', meteor), alpha=alpha)

        self.mask = pygame.mask.from_surface(self.image, 0)

    def update(self):
        """ Called each frame. """

        # Move block down one pixel
        self.rect.y += 1

        # If block is too far down, reset to top of screen.
        if self.rect.y > 410:
            self.reset_pos()

    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)


pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

meteor_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(10):
    # This represents a block
    name = random.choice(METEORS_BROWN)
    meteor = Meteoros(name)

    # Set a random location for the block
    meteor.rect.x = random.randrange(screen_width)
    meteor.rect.y = random.randrange(screen_height)

    # Add the block to the list of objects
    meteor_list.add(meteor)
    all_sprites_list.add(meteor)


player = Nave()
all_sprites_list.add(player)

done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(WHITE)

    # Calls update() method on every sprite in the list
    all_sprites_list.update()

    meteors_hit_list = pygame.sprite.spritecollide(player, meteor_list, False, collided=check_col)

    # Check the list of collisions.
    for block in meteors_hit_list:
        score += 1
        print(score)

        # Reset block to the top of the screen to fall again.
        block.reset_pos()

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 20 frames per second
    clock.tick(40)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()