import pygame
from settings import *
import os
import math
import time
from Pipe import Pipe
from Bird import Bird
"""
    Class to run Flappy bird
"""
class FlappyBirdGame:
    def __init__(self, screen) -> None:
        self.isRunning = True
        self.start = False
        self.gameOver = False

        self.screen = screen
        self.loadImages()

        self.backgroundTiles = math.ceil(self.screen.get_width()/ self.backgroundImg.get_width()) + 1
        self.groundTiles = math.ceil(self.screen.get_width()/ self.groundImg.get_width()) + 1
        self.scroll = 0
        self.scrollSpeed = 5 #* 60
        self.clock = pygame.time.Clock()

        self.now = time.time()
        self.prevTime = self.now
        self.dt = 0
        
        self.bird = Bird(self.screen.get_width()//2, self.screen.get_height()//2)
        self.pipeList = []
        self.pipeFrequency = 1.5 # seconds to add additional pipe
        self.prevPipeTime = time.time() - self.pipeFrequency

    def loop(self):
        self.getDt()
        self.update()
        self.draw()

    def getDt(self):
        currentTime = time.time()
        self.dt = currentTime - self.prevTime
        self.prevTime = currentTime
        
        self.dt = 1

    def update(self):
        self.scroll -= self.scrollSpeed * self.dt
        if abs(self.scroll) > self.backgroundImg.get_width():
            self.scroll = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start = True

        if self.start:
            self.bird.update()
            self.updatePipes()

    def draw(self):
        for i in range(self.backgroundTiles):
            self.screen.blit(self.backgroundImg, (i * self.backgroundImg.get_width() + self.scroll, 0))
        
        self.bird.draw(self.screen)
        self.drawPipes(self.pipeList)

        for i in range(self.groundTiles):
            self.screen.blit(self.groundImg, 
                             (i * self.groundImg.get_width() + self.scroll,
                              self.backgroundImg.get_height()))
        
        pygame.display.update()
    
    def drawPipes(self, pipeList):
        for pipe in pipeList:
            pipe.draw(self.screen)
    
    def updatePipes(self):
        now = time.time()
        if now - self.prevPipeTime >= self.pipeFrequency:
            self.pipeList.append(Pipe(self.screen.get_width()))
            self.prevPipeTime = now

        for pipe in self.pipeList:
            pipe.update(self.scrollSpeed * self.dt)

            # if pipe.x + pipe.width < self.screen.get_width() // 2:
            #     self.pipeList.append(Pipe(self.screen.get_width()))

            if pipe.x + pipe.width < 0:
                # pipe.x = self.screen.get_width()
                self.pipeList.remove(pipe)
            
    def loadImages(self):
        self.backgroundImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "bg1.png")).convert_alpha()
        self.backgroundImg = pygame.transform.smoothscale(self.backgroundImg, (self.backgroundImg.get_width(), BACKGROUND_HEIGHT))

        self.groundImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "ground.png")).convert_alpha()
        self.groundImg = pygame.transform.smoothscale(self.groundImg, (self.groundImg.get_width(), GROUND_HEIGHT))


    def run(self):
        while self.isRunning:
            self.loop()
            self.clock.tick(60)