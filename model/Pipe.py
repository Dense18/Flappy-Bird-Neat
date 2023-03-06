import pygame
import os
from settings import *
import random
from model.Bird import Bird

"""
    Class object handling Pipe positions and collisions
"""
class Pipe:
    def __init__(self, x, velocity = 50) -> None:
        self.x = x
        self.height = self.top = self.bottom = 0
        self.gap = 120

        self._loadImages()
        self.width = self.pipeImg.get_width()

        self.velocity = velocity
        self.setRandomHeight()

        self.passed = False

    def setRandomHeight(self):
        self.height = random.randrange(int(SCREEN_HEIGHT * 0.18), BACKGROUND_HEIGHT - self.gap - int(SCREEN_HEIGHT * 0.18))
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
    
    def collideBird(self, bird: Bird):
        birdMask = bird.getMask()

        pipeTopMask = pygame.mask.from_surface(self.topImg)
        pipeBottomMask = pygame.mask.from_surface(self.bottomImg)

        pipeTopOffset = (self.x - bird.x, int(self.top - round(bird.y)))
        pipeBottomOffset = (self.x - bird.x, int(self.bottom - round(bird.y)))

        bottomCollide = birdMask.overlap(pipeBottomMask, pipeBottomOffset)
        topCollide = birdMask.overlap(pipeTopMask, pipeTopOffset)

        return (bottomCollide or topCollide)