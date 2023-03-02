import pygame
import os
from settings import *
import random

"""
    Class object handling Pipe positions and collisions
"""
class Pipe:
    def __init__(self, x, velocity = 50) -> None:
        self.x = x
        self.height = self.top = self.bottom = 0
        self.gap = 130

        self._loadImages()
        self.width = self.pipeImg.get_width()

        self.velocity = velocity
        self.setRandomHeight()

    def setRandomHeight(self):
        self.height = random.randrange(int(SCREEN_HEIGHT * 0.05), BACKGROUND_HEIGHT - self.gap - int(SCREEN_HEIGHT * 0.05))
        self.top = self.height - self.topImg.get_height()
        self.bottom = self.height + self.gap

    def draw(self, screen):
        screen.blit(self.bottomImg, (self.x, self.bottom))
        screen.blit(self.topImg, (self.x, self.top))
    
    def update(self, velocity):
        self.x -= velocity

    def _loadImages(self):
        self.pipeImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "pipe.png"))
        self.bottomImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "pipe.png"))
        self.topImg = pygame.transform.flip(self.pipeImg, False, True)