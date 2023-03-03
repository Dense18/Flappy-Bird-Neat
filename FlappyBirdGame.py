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

        ## Create objects needed for Flappy bird
        self.bird = Bird(self.screen.get_width()//2, self.screen.get_height()//2)
        self.pipeList = [Pipe(self.screen.get_width())]

        ## Identify the number of tiles needed for the background and ground image
        self.backgroundTiles = math.ceil(self.screen.get_width()/ self.backgroundImg.get_width()) + 1
        self.groundTiles = math.ceil(self.screen.get_width()/ self.groundImg.get_width()) + 1

        ## Scroll speed, i.e the speed in which the screen moves 
        self.scroll = 0
        self.scrollSpeed = 4 #* 60

        ## Delta Time and clock Variables
        self.clock = pygame.time.Clock()
        self.now = time.time()
        self.prevTime = self.now
        self.dt = 0

        ## Use this variable if we want to add python pipe based on time passed
        self.pipeFrequency = 1.5 # seconds to add additional pipe
        self.prevPipeTime = time.time() - self.pipeFrequency

        ## Score
        self.score = 0
        self.scoreSize = 50
        self.scoreFont = pygame.font.Font(os.path.join(FONTS_FOLDER, "flappy-font.ttf"), self.scoreSize)

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start = True

        if self.start:
            self.scroll -= self.scrollSpeed * self.dt
            if abs(self.scroll) > self.backgroundImg.get_width():
                self.scroll = 0
            self.bird.update()
            self.updatePipes()

    def updatePipes(self):
        now = time.time()

        #Use this if we want to add pipe based on every time passed
        # if now - self.prevPipeTime >= self.pipeFrequency:
        #     self.pipeList.append(Pipe(self.screen.get_width()))
        #     self.prevPipeTime = now

        for pipe in self.pipeList:
            pipe.update(self.scrollSpeed * self.dt)

            if pipe.collideBird(self.bird):
                self.reset()
                return
            
            if not pipe.passed and self.bird.x + self.bird.width > pipe.x and self.bird.x + self.bird.width < pipe.x + pipe.width:
                pipe.passed = True
                self.pipeList.append(Pipe(self.screen.get_width()))
                self.score += 1
            
            # if pipe.x + pipe.width < self.screen.get_width() // 2:
            #     self.pipeList.append(Pipe(self.screen.get_width()))

            if pipe.x + pipe.width < 0:
                self.pipeList.remove(pipe)
            
    def draw(self):
        # Draw the background
        for i in range(self.backgroundTiles):
            self.screen.blit(self.backgroundImg, (i * self.backgroundImg.get_width() + self.scroll, 0))
        
        # Draw the objects
        self.bird.draw(self.screen)
        self.drawPipes(self.pipeList)

        # draw the ground
        for i in range(self.groundTiles):
            self.screen.blit(self.groundImg, 
                             (i * self.groundImg.get_width() + self.scroll,
                              self.backgroundImg.get_height()))
        



        scoreObj = self.scoreFont.render(str(self.score), 1, (255,255,255)).convert_alpha()       
        self.screen.blit(scoreObj, 
                         (self.screen.get_width()//2 - scoreObj.get_width()//2, SCREEN_HEIGHT*0.1 - scoreObj.get_height()//2),
                         )
        
        # mask = pygame.mask.from_surface(scoreObj)
        # self.screen.blit(mask.to_surface(unsetcolor=(255,255,255,255), setcolor=(0,0,0,0)), 
        #                  (self.screen.get_width()//2 - scoreObj.get_width()//2, SCREEN_HEIGHT*0.1 - scoreObj.get_height()//2))
                         
        pygame.display.update()
    
    def drawPipes(self, pipeList):
        for pipe in pipeList:
            pipe.draw(self.screen)
    
    def run(self):
        while self.isRunning:
            self.loop()
            self.clock.tick(60)

    def loadImages(self):
        self.backgroundImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "bg1.png")).convert_alpha()
        self.backgroundImg = pygame.transform.smoothscale(self.backgroundImg, (self.backgroundImg.get_width(), BACKGROUND_HEIGHT))

        self.groundImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "ground.png")).convert_alpha()
        self.groundImg = pygame.transform.smoothscale(self.groundImg, (self.groundImg.get_width(), GROUND_HEIGHT))
    
    def reset(self):
        self.__init__(self.screen)

    
    """
        Configure neat
    """