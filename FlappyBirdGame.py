import pygame
from settings import *
import os
import math
import time
from model.Pipe import Pipe
from model.Bird import Bird
from FlappyBirdUI import FlappyBirdUI

class FlappyBirdGame:
    """
        Class to run Flappy bird game
    """
    def __init__(self, screen) -> None:
        self.isRunning = True
        self.start = False
        self.gameOver = False

        self.screen = screen
        self.UI = FlappyBirdUI(self)

        ## Create objects needed for Flappy bird
        self.bird = Bird(self.screen.get_width()//2, self.screen.get_height()//2)
        self.pipeList = [Pipe(self.screen.get_width())]

        ## Scroll speed, i.e the speed in which the screen moves 
        self.scroll = 0
        self.scrollSpeed = 4 #* 60

        ## Clock Variables
        self.clock = pygame.time.Clock()

        ## Score
        self.score = 0

    def loop(self):
        self.getEvent()
        self.update(self.events)
        self.draw()

    def getEvent(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start = True
                self.bird.jump()

    def update(self, events):
        if self.start:
            self.updateScroll()
            self.bird.update()
            self.updatePipes()

            if self.bird.y + self.bird.height > BACKGROUND_HEIGHT or self.bird.y < 0:
                self.reset()

    def updateScroll(self):
        self.scroll -= self.scrollSpeed 
        if abs(self.scroll) > self.UI.backgroundImg.get_width():
            self.scroll = 0

    def updatePipes(self):
        for pipe in self.pipeList:
            pipe.update(self.scrollSpeed)

            if pipe.collideBird(self.bird):
                self.reset()
                return
            
            if not pipe.passed and self.bird.x + self.bird.width > pipe.x and self.bird.x + self.bird.width < pipe.x + pipe.width:
                pipe.passed = True
                self.pipeList.append(Pipe(self.screen.get_width()))
                self.score += 1
            
            if pipe.x + pipe.width < 0:
                self.pipeList.remove(pipe)
            
    def draw(self):
        self.UI.draw()
    
    def run(self):
        while self.isRunning:
            self.loop()
            self.clock.tick(60)
    
    def reset(self):
        # self.__init__(self.screen)
        self.bird = Bird(self.screen.get_width()//2, self.screen.get_height()//2)
        self.pipeList = [Pipe(self.screen.get_width())]

        self.isRunning = True
        self.start = False
        self.gameOver = False