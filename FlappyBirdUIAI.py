import pygame
import os
from settings import *
import math

class FlappyBirdUIAI:
    """
        UI class for the Flappy Bird game AI training
    """
    def __init__(self, game) -> None:
        self.game = game

        self.loadImages()

        ## Identify the number of tiles needed for the background and ground image
        self.backgroundTiles = math.ceil(self.game.screen.get_width()/ self.backgroundImg.get_width()) + 1
        self.groundTiles = math.ceil(self.game.screen.get_width()/ self.groundImg.get_width()) + 1

        #Score
        self.scoreSize = 50
        self.scoreFont = pygame.font.Font(os.path.join(FONTS_FOLDER, "flappy-font.ttf"), self.scoreSize)

        #Generation
        self.generationTextSize = 20
        self.generationFont = pygame.font.Font(os.path.join(FONTS_FOLDER, "flappy-font.ttf"), self.generationTextSize)
        pass

    def draw(self):
        # Draw the background
        self.drawBackground()
        
        # Draw the objects
        self.drawBirds()
        self.drawPipes(self.game.pipeList)

        self.drawGround()

        self.drawScore()   
        self.drawGeneration()

        pygame.display.update()

    
    def drawBackground(self):
        for i in range(self.backgroundTiles):
            self.game.screen.blit(self.backgroundImg, (i * self.backgroundImg.get_width() + self.game.scroll, 0))
    
    def drawGround(self):
        for i in range(self.groundTiles):
            self.game.screen.blit(self.groundImg, 
                             (i * self.groundImg.get_width() + self.game.scroll,
                              self.backgroundImg.get_height()))
    
    def drawBirds(self):
        for bird in self.game.birdList:
            bird.draw(self.game.screen)
            try:
                pygame.draw.line(self.game.screen, (255,0,0), 
                                    (bird.x + bird.width//2, bird.y + bird.height//2), \
                                    (self.game.pipeList[self.game.pipeInd].x + self.game.pipeList[self.game.pipeInd].width//2, self.game.pipeList[self.game.pipeInd].height), 5)
                pygame.draw.line(self.game.screen, (255,0,0), 
                                    (bird.x + bird.width//2, bird.y + bird.height//2), \
                                    (self.game.pipeList[self.game.pipeInd].x + self.game.pipeList[self.game.pipeInd].width//2, self.game.pipeList[self.game.pipeInd].bottom), 5)
            except:
                pass

    def drawGeneration(self):
        textObj = self.generationFont.render(f"Gen: {self.game.generation}", 1, (255,255,255)).convert_alpha()  
        aliveObj = self.generationFont.render(f"Alive: {len(self.game.birdList)}", 1, (255,255,255)).convert_alpha()       
        self.game.screen.blit(textObj, (10,10))
        self.game.screen.blit(aliveObj, (10,20 + textObj.get_height()))

    def drawPipes(self, pipeList):
        for pipe in pipeList:
            pipe.draw(self.game.screen)
    
    def drawScore(self):
        digits = [int(x) for x in str(self.game.score)]

        totalWidth = 0
        for digit in digits:
            totalWidth += self.numberImages[digit].get_width()

        xLoc = self.game.screen.get_width()//2 - totalWidth//2

        for digit in digits:
            numImage = self.numberImages[digit]
            self.game.screen.blit(numImage, 
                            (xLoc, SCREEN_HEIGHT*0.1 - numImage.get_height()//2),
                            )
            xLoc += self.numberImages[digit].get_width()

    def loadImages(self):
        self.backgroundImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "bg1.png")).convert_alpha()
        self.backgroundImg = pygame.transform.smoothscale(self.backgroundImg, (self.backgroundImg.get_width(), BACKGROUND_HEIGHT))

        self.groundImg = pygame.image.load(os.path.join(IMAGES_FOLDER, "ground.png")).convert_alpha()
        self.groundImg = pygame.transform.smoothscale(self.groundImg, (self.groundImg.get_width(), GROUND_HEIGHT))

        self.numberImages = {}
        for i in range(10):
            self.numberImages[i] = pygame.image.load(os.path.join(IMAGES_FOLDER, f"{i}.png")).convert_alpha()